from time import time
from typing import Optional

from app.schemas.quiz import (
    CreateQuizSchema,
    GetGameSchema,
    GetQuizesPaginatedSchema,
    GetQuizSchema,
)
from bson.objectid import ObjectId
from core.db import games_db_client, quiz_db_client
from fastapi import HTTPException, Request


class QuizService:
    def __init__(self):
        pass

    def create_quiz(self, request: CreateQuizSchema, req: Request) -> GetQuizSchema:
        if len(request.questions) < 2:
            raise HTTPException(400, "you must provide atleast 10 questions")
        for question in request.questions:
            if len(question.answers) < 2:
                raise HTTPException(400, "All questions must have atleast 2 answers")
        request.timestamp = time()
        request.creator_id = str(req.user.id)
        res = quiz_db_client.insert(request.dict())
        quiz = quiz_db_client.find({"_id": res.inserted_id})[0]
        return GetQuizSchema(**quiz)

    def delete_quiz(self, quiz_id: str, req: Request) -> dict:
        quiz = quiz_db_client.find({"_id": ObjectId(quiz_id)})
        if not quiz:
            raise HTTPException(404, "quiz not found")
        quiz = quiz[0]
        if quiz["creator_id"] != req.user.id:
            raise HTTPException(401, "You are not quiz owner")
        quiz_db_client.delete({"_id": ObjectId(quiz_id)})
        return {"message": "successful"}

    def get_quiz(self, quiz_id: str) -> GetQuizSchema:
        quiz = quiz_db_client.find({"_id": ObjectId(quiz_id)})
        if not quiz:
            raise HTTPException(404, "quiz not found")
        return GetQuizSchema(**quiz[0])

    def get_quizes(
        self, limit: Optional[int] = -1, page: Optional[int] = None, public: bool = True
    ) -> GetQuizesPaginatedSchema:
        if not page:
            page = 1
        quizes = quiz_db_client.paginate_find({"public": True}, page, limit)
        return GetQuizesPaginatedSchema(**quizes)

    def get_game(self, game_id: str) -> GetGameSchema:
        res = games_db_client.find({"_id": ObjectId(game_id)})
        if not res:
            raise HTTPException(404)
        return GetGameSchema(**res[0])
