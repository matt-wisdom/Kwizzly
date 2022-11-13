import asyncio
import time

import async_timeout
from helper.redis import RedisBackend
from quizly_tg import messages
from quizly_tg.api import QuizlyAPI
from quizly_tg.database import User
from quizly_tg.utils import get_resp_msg, send_with_action
from rfc3986 import is_valid_uri
from telethon import TelegramClient
from telethon.tl.custom.conversation import Conversation

redis = RedisBackend()


async def read_pubsub(queue: asyncio.Queue, game_id: str):
    other_answers = redis.subscribe(f"telegram_{game_id}_server_msg")
    while True:
        try:
            data = await other_answers.__anext__()
            print(data)
            await queue.put(data)
        except Exception as e:
            print(e)


async def game_session(convo: Conversation, game_id: str):
    await convo.send_message("Launching")
    queue = asyncio.Queue(100)
    asyncio.create_task(read_pubsub(queue, game_id))
    got_data_while_waiting = False
    sent_score = False
    while True:
        if not got_data_while_waiting:
            data = await queue.get()
        else:
            got_data_while_waiting = False
        type = data["type"]
        time_per_question = 10
        if type == "message":
            await convo.send_message(data["data"])
        elif type == "answer-status":
            pass
            # msg = "wrong answer" if data["data"]["why"] == "incorrect" else "Timeout"
            # await convo.send_message(msg)
        elif type == "metadata":
            # time_per_question = data["data"]["quiz"]["timed_per_question"]
            msg = "**Starting Soon:**\n"
            print(data)
            msg += f"Number of participants: {len(data['data']['data']['game']['members'])}"
            await convo.send_message(msg)
        elif type == "no_participant":
            await convo.send_message("No participants")
            break
        elif type == "ended":
            await convo.send_message(data["data"])
            break
        elif type == "already_started":
            await convo.send_message(data["data"])
            break
        elif type == "start":
            await convo.send_message("Game starts soon.")
        elif type == "started":
            await convo.send_message("Game Started")
        elif type == "question":
            question = data["data"]["question"]
            qa_msg = f"**{question.upper()}**\n\n"
            answers = data["data"]["answers"]
            for i, answer in enumerate(answers):
                qa_msg += f"__{i+1}. {answer}__\n"
            qa_msg += "\n**answer:**"
            await convo.send_message(qa_msg)
            t = time.time()
            while time.time() - t < time_per_question:
                print("waiting Q")
                p = time.time()
                try:
                    try:
                        select = await convo.get_response(timeout=0.05)
                    except Exception as e:  # asyncio.exceptions.TimeoutError:
                        print("Type", e)
                        pass
                    try:
                        print("getting")
                        data = queue.get_nowait()
                        print("\n\n\nQueue data")
                        got_data_while_waiting = True
                        # if data["type"] == "question":
                        break
                    except asyncio.QueueEmpty:
                        print("Queue empty")
                    selected = select.text
                    print("Selected", selected)
                    if not selected.isdecimal():
                        continue
                    selected = int(selected) - 1
                    if selected not in range(len(answers)):
                        continue
                    await redis.publish(
                        f"telegram_{game_id}_actions",
                        {"type": "my_answer", "answer": answers[selected]},
                    )
                    select = None
                    break
                except UnboundLocalError:
                    pass
                except Exception as e:
                    print("ERRR", e)
        elif type == "score":
            if not sent_score:
                msg = "**scores**\n\n"
                for _, score in data["data"]["score"].items():
                    msg += f"    `{score['name'].upper()} - {score['score']}`\n"
                await convo.send_message(msg)
                sent_score = True
        elif type == "game-data":
            pass
        elif type == "finished":
            msg = "**Game Finished.**\n\n"
            msg += "**scores:**\n"
            for _, score in data["data"]["score"].items():
                msg += f"    `{score['name'].upper()} - {score['score']}`\n"
            await convo.send_message(msg)
            break
    await convo.send_message("Finished")


async def play_multi_player(
    bot: TelegramClient, sender_id: str, sender: User, api_client: QuizlyAPI
):
    async with bot.conversation(sender_id, exclusive=False) as conv:
        game_url = await get_resp_msg(
            conv, messages.get_game.format(url=f"{FRONTEND_BASE_URL.strip('/')}/quizes")
        )
        if not is_valid_uri(game_url):
            await send_with_action(sender, messages.invalid_data, bot)
            return
        split = game_url.split("/view-quiz/")
        quiz_id = split[1].strip(" /")
        origin = split[0].strip()
        token = await api_client.get_auth_token(sender_id)
        token = token["access_token"]
        try:
            join_url, game_id = await api_client.launch_multiplayer(
                quiz_id, origin, auth_token=token
            )
        except Exception as e:
            await conv.send_message(f"Could not authenticate: {str(e)}")
            return
        token = await api_client.get_auth_token(sender_id)
        token = token["access_token"]
        await redis.publish(
            "new_game_queue",
            {"quiz_id": quiz_id, "game_id": game_id, "token": token},
        )
        await asyncio.sleep(2)
        await conv.send_message(messages.join_game.format(join_url=join_url))
        invite = await get_resp_msg(conv, messages.invite_manual)
        if invite.lower() != "no":
            pass
        start = await get_resp_msg(conv, messages.start_msg)
        if start == "/begingame":
            await game_session(conv, game_id)


async def join_game(bot: TelegramClient, sender_id: str, api_client: QuizlyAPI):
    async with bot.conversation(sender_id) as conv:
        join_url = await get_resp_msg(conv, messages.get_join_game)
        game_id = join_url.split("join-multi/")[1].split("?")[0].strip(" /")
        quiz_id = join_url.split("?quiz_id=")[1].split("?")[0].strip(" /")
        token = await api_client.get_auth_token(sender_id)
        token = token["access_token"]
        await conv.send_message("Joining game")
        await redis.publish(
            "new_game_queue",
            {"quiz_id": quiz_id, "game_id": game_id, "token": token},
        )
        await asyncio.sleep(3)
        await game_session(conv, game_id)
