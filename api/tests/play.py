import queue
import threading
import time

from starlette.testclient import WebSocketTestSession


def receive_queue(ws: WebSocketTestSession, queue_: queue.Queue):
    """
    Get data from websocket server
    """
    while True:
        queue_.put(ws.receive_json())


def play_game(ws: WebSocketTestSession, questions: list, q_answer="ok"):
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
            assert time.time() - t_start < 3
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
