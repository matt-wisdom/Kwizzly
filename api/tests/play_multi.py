import queue
import threading
import time

from fastapi.testclient import TestClient
from starlette.testclient import WebSocketTestSession


def receive_queue(ws: WebSocketTestSession, queue_: queue.Queue):
    """
    Get data from websocket server
    """
    while True:
        queue_.put(ws.receive_json())


def play_game(ws: WebSocketTestSession, q_answer="ok", creator=False, can_answer=False):
    """
    Manage gameplay.
    Recieve user actions and send responses.
    """
    t_start = time.time()
    finished = None
    try:

        def send_start():
            time.sleep(10)
            for i in range(4):
                ws.send_json({"type": "start"})
                time.sleep(0.5)
            print("Sent start")

        threading.Thread(target=send_start).start()
        g_queue = queue.Queue(1000)
        t = threading.Thread(target=receive_queue, args=(ws, g_queue))
        # t.daemon = True
        t.start()
        q_index = 0
        answer_statuses = 0
        all_questions = []
        print("Starting", creator)
        while True:
            time.sleep(0.3)
            # if not can_answer:
            #     print("IN", can_answer)
            ws.send_json({"type": "start"})
            try:
                msg = g_queue.get_nowait()
            except queue.Empty:
                ws.send_json({"type": "start"})
                continue
            assert time.time() - t_start < 3
            type = msg["type"]
            print(msg, can_answer)
            if type == "question":
                print("Question", msg)
                q_index += 1
                ans = (
                    q_answer[q_index % len(q_answer)]
                    if isinstance(q_answer, list)
                    else q_answer
                )
                all_questions.append(
                    {
                        "question": msg["question"],
                        "answers": msg["answers"],
                        "correct": q_answer,
                    }
                )
                if can_answer:
                    print("Sending answer", can_answer)
                    ws.send_json({"type": "my_answer", "answer": ans})
            elif type == "register":
                print("\n\n\nRegister")
            elif type == "no_participant":
                raise ValueError("No participant")
            elif type == "already_started":
                raise ValueError("Already Started")
            elif type == "ended":
                raise ValueError("Already finished")
            elif type == "finished":
                # assert msg["data"]["correct"] == q_index
                assert answer_statuses == q_index
                finished = msg
                # assert msg["data"]["score"] == 100
                # assert set(all_questions) == set(questions)
                break
            elif type == "answer-status":
                answer_statuses += 1
            else:
                print("Typed", msg["type"], can_answer)
                ws.send_json({"type": "start"})
    except Exception as e:
        print(e)
    finally:
        ws.close()
        return finished


def play_game_slow(ws: WebSocketTestSession, questions: list, q_answer="ok"):
    """
    Manage gameplay.
    Recieve user actions and send responses.
    """
    t_start = time.time()
    finished = None
    try:
        ws.send_json({"type": "start"})
        g_queue = queue.Queue(1000)
        t = threading.Thread(target=receive_queue, args=(ws, g_queue))
        t.daemon = True
        t.start()
        q_index = 0
        answer_statuses = 0
        all_questions = []
        while True:
            try:
                msg = g_queue.get_nowait()
            except queue.Empty:
                continue

            type = msg["type"]
            if type == "question":
                q_index += 1
                ans = (
                    q_answer[q_index % len(q_answer)]
                    if isinstance(q_answer, list)
                    else q_answer
                )
                all_questions.append(
                    {
                        "question": msg["question"],
                        "answers": msg["answers"],
                        "correct": q_answer,
                    }
                )
                if q_index < 3:
                    time.sleep(10)
                ws.send_json({"type": "answer", "answer": ans})
            elif type == "finished":
                # assert msg["data"]["correct"] == q_index
                assert answer_statuses == q_index
                finished = msg
                # assert msg["data"]["score"] == 100
                # assert set(all_questions) == set(questions)
                break
            elif type == "answer-status":
                answer_statuses += 1
            else:
                print(msg)
    finally:
        ws.close()
        return finished


def play_as(
    app: TestClient,
    game_id: str,
    token: str,
    quiz_id: str,
    questions: list,
    q_answer="ok",
    slow=False,
    creator=False,
    can_answer=False,
):
    """
    Listen for new game request and create websocket session
    for each request.
    """
    with app.websocket_connect(
        f"/game/multiplayer?token={token}&quiz_id={quiz_id}&game_id={game_id}"
    ) as ws:
        if slow:
            return play_game_slow(ws, questions, q_answer)
        else:
            return play_game(ws, q_answer, creator, can_answer)
