import asyncio
import random
import time
from asyncio.log import logger
from typing import Optional

import jwt
from app.schemas.quiz import Attempt, GameState, GetGameSchema, RedisGameData
from app.services.quiz import QuizService
from app.services.user import UserService
from async_timeout import timeout
from bson import ObjectId
from core.db import attempts_db_client, games_db_client  # quiz_db_client
from core.helpers.cache import redis, redis_lock
from core.utils.token_helper import TokenHelper
from fastapi import Depends, Query, WebSocket, status


async def check_token(
    websocket: WebSocket,
    token: Optional[str] = Query(None),
):
    if token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    try:
        payload = TokenHelper.decode(token)
        user_id = payload.get("user_id")
    except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return user_id


def get_game(game_id: str) -> GetGameSchema:
    game = games_db_client.find({"_id": ObjectId(game_id)})
    if not game:
        raise Exception("game not found")
    return GetGameSchema(**game[0])


async def single_player_session(
    websocket: WebSocket,
    user_id: str = Depends(check_token),
    quiz_id: str = Query(None),
):
    """
    Websocket endpoint for single player quiz game.
    """
    await websocket.accept()

    user = UserService().get_user(user_id)  # Validate Users existence
    quiz = QuizService().get_quiz(quiz_id)
    question_per_session = quiz.question_per_session
    question_index = 0
    questions_indexes = list(range(len(quiz.questions)))
    random.seed(time.time())
    random.shuffle(questions_indexes)
    questions = []

    for i in questions_indexes[:question_per_session]:
        questions.append(quiz.questions[i])

    data = await websocket.receive_json()
    if data["type"] != "start":
        await websocket.send_json({"type": "error", "message": "Game not started"})
        await websocket.close(status.WS_1008_POLICY_VIOLATION)
    await websocket.send_json(
        {
            "type": "metadata",
            "data": {
                **quiz.dict(exclude={"questions", "timestamp"}),
                "created": time.asctime(time.gmtime(quiz.timestamp)),
                "questions": len(questions),
            },
        }
    )

    corrects = 0
    start_game = time.time()
    while True:
        start = time.time()
        curr_question = questions[question_index]
        await websocket.send_json(
            {
                "type": "question",
                "question": curr_question.question,
                "answers": curr_question.answers,
            }
        )
        data = await websocket.receive_json()
        type_ = data["type"]  # Answer type
        if type_ == "next":
            question_index = question_index + 1

        if type_ == "answer":
            answer = data["answer"]
            why = "incorrect"
            if time.time() - start > quiz.timed_per_question:
                # If user answers after timeout.
                answer = ""
                why = "timeout"

            if answer == curr_question.correct:
                corrects += 1
                await websocket.send_json(
                    {"type": "answer-status", "status": True, "corrects": corrects}
                )
            else:
                await websocket.send_json(
                    {
                        "type": "answer-status",
                        "status": False,
                        "why": why,
                        "corrects": corrects,
                    }
                )
            question_index = question_index + 1
        if question_index > len(questions) - 1:  # All questions answered
            break
    score = corrects * 100 // len(questions)
    attempt = Attempt(
        quiz_id=quiz.id,
        taker_name=user.nickname,
        taker_id=user_id,
        score=score,
        timestamp=time.time(),
    )
    attempts_db_client.insert(attempt.dict(exclude_none=True))

    await websocket.send_json(
        {
            "type": "finished",
            "data": {
                "correct": corrects,
                "score": score,
                "total_time": time.time() - start_game,
            },
        }
    )


async def multiplayer_session(
    websocket: WebSocket,
    user_id: str = Depends(check_token),
    quiz_id: str = Query(None),
    game_id: str = Query(None),
):
    """
    Websocket endpoint for multiplayer player quiz game.

    =================
        - When users join the room. Metadata is sent to them

        - The creators client sends a start message type
          which is broadcasted to the room with type started

        - Creator waits for 10 seconds

        - If participants are less than two, the creator closes its socket else it broadcasts a start message type.

        - For non creator members, on connecting they check if game has been finished or has started before their arrival. If so, they close their socket else game-data
          is sent to the client and they are add as members of the game.

        - They wait for 120 seconds for the started message from the creator, then wait 30 seconds for start message. If either of these aren't recieved. The socket is closed.

        - Questions and answer options are then sent to all participants.

        - whenever a participant answers a question, checks occur to ensure the time limit has not been exceeded and the question is correct.

        - if answer is wrong, current wrong answers counter for the question is incremented and that user cannot answer the question again. If all participants have given wrong answers, proceed to next question and zero the counter.

        - If the answer is correct, it is broadcasted using an other_answer message type to other participant. The first participant to recieve the message checks for timeout and increments the game score.
          An other-answer-status message is then broadcasted.

        - If all questions have been gone through. Send a finished message
          and close all tasks.
    """
    await websocket.accept()
    user = UserService().get_user(user_id)  # Validate user exists
    quiz = QuizService().get_quiz(quiz_id)
    game = get_game(game_id)
    if game.state == GameState.ended:
        await websocket.send_json(
            {
                "type": "ended",
            }
        )
        await websocket.close()
        return

    question_per_session = game.questions_count or quiz.question_per_session

    # Current question index is stored in redis with question_index_key key
    question_index = 0
    question_index_key = f"{game_id}_qid"
    curr_wrongs = f"{game_id}_wrongs"
    got_correct_while_waiting = False

    await redis.save(question_index, question_index_key)
    questions_indexes = list(range(len(quiz.questions)))
    random.shuffle(questions_indexes)
    questions = []
    # if len(questions_indexes) < question_per_session:
    #     raise Exception("Not enough q")
    for i in questions_indexes[:question_per_session]:
        try:
            questions.append(quiz.questions[i].dict())
        except IndexError:
            logger.exception("Not enough questions, using the current questions")
            raise Exception("Not enough questions")
    await websocket.send_json(
        {
            "type": "metadata",
            "data": {
                "created": time.asctime(time.gmtime(quiz.timestamp)),
                "questions": len(questions),
                "quiz": quiz.dict(exclude={"questions", "timestamp"}),
                "game": game.dict(),
            },
        }
    )

    is_creator = game.creator_id == user_id

    async def get_registers():
        """
        Get registered_users from redis pubsub
        """
        sub = redis.subscribe(game_id)
        while True:
            data = await sub.__anext__()
            if data["type"] == "register":
                if data["user"]["id"] != user_id:
                    await websocket.send_json(
                        {"type": "register", "user": data["user"]}
                    )
            await asyncio.sleep(0.5)

    get_regs = asyncio.create_task(get_registers())
    if is_creator:
        # Only creator sets questions
        if not game.questions:
            games_db_client.update(
                {"_id": ObjectId(game_id)}, {"$set": {"questions": questions}}
            )
        if game.state == GameState.pending:
            # Wait for creator to start the game
            with timeout(120):
                data = await websocket.receive_json()
            redis_state = RedisGameData()
            await redis.save(redis_state.dict(), game_id)
            # if cm.expired:
            #     websocket.send_json({"type": "status", "message": "Game expired."})
            #     games_db_client.update(
            #         {"_id": game_id}, {"$set": {"state": GameState.expired}}
            #     )
            #     await websocket.close(code=status.WS_1004_NO_STATUS_RCVD)
            for _ in range(60):
                game = get_game(game_id)
                if len(game.members) > 1:
                    break
                await asyncio.sleep(0.5)
            games_db_client.update(
                {"_id": ObjectId(game_id)}, {"$set": {"state": GameState.started}}
            )
            await websocket.send_json({"type": "self_started"})
            await asyncio.sleep(3.0)
            if data["type"] == "start":
                # Alert participant that the game will start
                await redis.publish(game_id, {"type": "started"})
            # Countdown to game start
            await asyncio.sleep(10.0)
            await websocket.send_json({"type": "self_start"})
            game = get_game(game_id)
            if len(game.members) < 2:
                await websocket.send_json({"type": "no_participant"})
                await websocket.close()
                return
            await redis.publish(game_id, {"type": "start"})
    else:
        if user_id not in game.members:
            if game.state != GameState.pending:
                # If game has already started, stop user from joining
                await websocket.send_json({"type": "already_started"})
                await websocket.close()
                return
            # Increment members count
            await websocket.send_json(
                {
                    "type": "game-data",
                    "data": {
                        "game": game.dict(),
                    },
                }
            )
            await redis.publish(game_id, {"type": "register", "user": user.dict()})
            games_db_client.update(
                {"_id": ObjectId(game_id)},
                {"$set": {"members": game.members + [user_id]}},
            )

        if game.state == GameState.pending:
            
            data = redis.subscribe(game_id)
            
            with timeout(120) as cm:
                async for msg in data:
                    
                    if msg["type"] == "started":
                        await websocket.send_json(
                            {"type": "started", "message": "Game started."}
                        )
                        break

            with timeout(30) as cm:
                async for msg in data:
                    if msg["type"] == "start":
                        await websocket.send_json(
                            {"type": "start", "message": "Game started."}
                        )
                        break
            if cm.expired:
                await websocket.send_json(
                    {"type": "timeout", "message": "Creator did not start the game."}
                )
                await websocket.close()
                return
    get_regs.cancel()
    game = get_game(game_id)
    state = game.state
    if state == GameState.started:
        logger.debug("Game started")
        questions = [i.dict() for i in game.questions]
    elif state in [GameState.expired, GameState.ended]:
        await websocket.close(code=status.WS_1000_NORMAL_CLOSURE)

    start_game = time.time()

    other_answers = redis.subscribe(game_id)

    # Queue for getting messages from other participants via redis pubsub
    redis_queue = asyncio.Queue(1000)

    # Queue for getting messages from self via websockets
    sock_queue = asyncio.Queue(1000)

    async def get_data():
        """
        Get data from redis pubsub
        """
        while True:
            data = await other_answers.__anext__()
            if data["type"] == "other_answer":
                await redis_queue.put(data)
            await asyncio.sleep(0.5)

    q_sent_when = time.time()

    async def get_sock_msg():
        """
        Get websocket data
        """
        while True:
            # 
            data = await websocket.receive_json()
            await sock_queue.put(data)
            await asyncio.sleep(0.5)

    # Run tasks to constantly check from messages
    get_data_task = asyncio.create_task(get_data())
    get_sock_task = asyncio.create_task(get_sock_msg())
    q_sent = -1
    timeout_key = game_id + "__timeout"
    one_more = False
    scores_data = await redis.get(game_id)
    scores = scores_data["scores"]
    scores_full = full_scores(scores, game)
    await websocket.send_json({"type": "score", "score": scores_full})
    while True:
        # Main loop
        question_index = int(await redis.get(question_index_key))
        start = time.time()
        if one_more:
            break
        if await redis.get(question_index_key) > len(questions) - 1:
            one_more = True
        try:
            curr_question = questions[question_index]
            if q_sent != question_index:
                q_sent_when = time.time()
                
                await websocket.send_json(
                    {
                        "type": "question",
                        "question": curr_question["question"],
                        "answers": [answer for answer in curr_question["answers"]],
                    }
                )
                q_sent = question_index
            # else:
            #     
        except IndexError as e:
            if not one_more:
                raise e
        try:
            res = sock_queue.get_nowait()
        except asyncio.QueueEmpty:
            res = {"type": "timeout"}
        type_ = res["type"]
        timedout = False
        if time.time() - q_sent_when > quiz.timed_per_question + 7:
            timedout = True
        c = 0
        if type_ == "my_answer" or timedout:
            if not timedout:
                
                answer = res["answer"]
                why = "incorrect"
            tm = time.time()
            if tm - start > quiz.timed_per_question + 7 or timedout:
                # Invalidate answer if timeout
                answer = ""
                why = "timeout"
                async with redis_lock(game_id):
                    scores_data = await redis.get(game_id)
                    scores = scores_data["scores"]
                    already_answered = (
                        int(scores_data["last"]["index"]) == question_index
                    )
                    already_timed = (await redis.get(timeout_key)) == question_index
                    # Publish answer to question
                    if not already_answered and not already_timed:
                        await redis.save(question_index, timeout_key, 5)
                        await redis.publish(
                            game_id,
                            {
                                "type": "timeout",
                                "by": user_id,
                                "time": tm,
                                "from": user_id,
                            },
                        )
                await websocket.send_json({"type": "timeout"})
            else:
                if answer == curr_question["correct"]:
                    async with redis_lock(game_id):
                        scores_data = await redis.get(game_id)
                        scores = scores_data["scores"]
                        already_answered = (
                            int(scores_data["last"]["index"]) == question_index
                        )

                        # Publish answer to question
                        if not already_answered:
                            await redis.publish(
                                game_id,
                                {
                                    "type": "other_answer",
                                    "by": user_id,
                                    "correct": True,
                                    "time": tm,
                                    "from": user_id,
                                },
                            )
                else:
                    await websocket.send_json(
                        {"type": "answer-status", "status": False, "why": why}
                    )
                    curr_wrongs_count = (await redis.get(curr_wrongs)) or 0
                    await redis.save(curr_wrongs_count + 1, curr_wrongs)
                    while curr_wrongs_count < len(game.members) and (
                        tm - start < quiz.timed_per_question
                    ):
                        tm = time.time()
                        curr_wrongs_count = await redis.get(curr_wrongs)
                        try:
                            res = redis_queue.get_nowait()
                            if res["type"] == "other_answer":
                                got_correct_while_waiting = res
                                break
                        except asyncio.QueueEmpty:
                            pass
            # question_index = (question_index + 1)
            c = await redis.get(curr_wrongs)
            if c == len(game.members):
                res = {"type": "timeout"}
                await redis.save(question_index, timeout_key)
                await redis.save(0, curr_wrongs)
        if got_correct_while_waiting:
            res = got_correct_while_waiting
            got_correct_while_waiting = False
        else:
            try:
                res = redis_queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
        type_ = res["type"]
        if type_ == "timeout" and (await redis.get(timeout_key)) == question_index:
            async with redis_lock(game_id):
                
                scores_data = await redis.get(game_id)
                scores = scores_data["scores"]
                already_answered = int(scores_data["last"]["index"]) == question_index
                by = "timeout"
                if already_answered:
                    by = scores_data["last"]["by"]
                else:
                    await websocket.send_json({"type": "other-timeout"})
                    scores_data["last"]["index"] = question_index
                    scores_data["last"]["by"] = by
                    await redis.save(scores_data, game_id)
                    await redis.save(question_index + 1, question_index_key)
        if type_ == "other_answer":
            if res["from"] != user_id:
                async with redis_lock(game_id):
                    
                    scores_data = await redis.get(game_id)
                    scores = scores_data["scores"]
                    already_answered = (
                        int(scores_data["last"]["index"]) == question_index
                    )

                    if already_answered:
                        by = scores_data["last"]["by"]
                    elif res["time"] - start > quiz.timed_per_question + 7:
                        # Timed out
                        pass
                    else:
                        # If question has not been answered, update scores
                        by = res["by"]
                        if scores.get(by):
                            scores[by] += 1
                        else:
                            scores[by] = 1

                        scores_data["scores"] = scores
                        scores_data["last"]["index"] = question_index
                        scores_data["last"]["by"] = by
                        await redis.save(scores_data, game_id)
                        await redis.save(question_index + 1, question_index_key)
                    await websocket.send_json(
                        {
                            "type": "other-answer-status",
                            "status": True,
                            "by": by,
                        }
                    )

        # Send current scores
        scores_data = await redis.get(game_id)
        scores = scores_data["scores"]
        scores_full = full_scores(scores, game)
        if game.scores != scores:
            await websocket.send_json({"type": "score", "score": scores_full})
            games_db_client.update(
                {"_id": ObjectId(game_id)}, {"$set": {"scores": scores}}
            )
            game = get_game(game_id)
        if (await redis.get(question_index_key) > len(questions) - 1) or scores_data[
            "last"
        ]["index"] > len(questions) - 1:
            break

    game = get_game(game_id)

    # update game score in db
    games_db_client.update({"_id": ObjectId(game_id)}, {"$set": {"scores": scores}})
    scores_full = full_scores(scores, game)
    
    games_db_client.update(
        {"_id": ObjectId(game_id)}, {"$set": {"state": GameState.ended}}
    )
    await websocket.send_json(
        {
            "type": "finished",
            "data": {"score": scores_full, "total_time": time.time() - start_game},
        }
    )

    # Stop listening for new messages
    get_sock_task.cancel()
    get_data_task.cancel()


def full_scores(scores, game: GetGameSchema):
    scores_full = {}
    for id in game.members:
        user = UserService().get_user(id)
        scores_full[id] = {"name": user.nickname, "score": scores.get(id, 0)}
    return scores_full
