"""
    Schemas for quizes (single and multiplayer)
"""
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class QuizAnswer(BaseModel):
    answer: str


class QuizQuestion(BaseModel):
    question: str
    answers: List[str]
    correct: str


class InviteType(str, Enum):
    anytime = "play_anytime"
    multiplayer = "invite_multiplayer"


class GameState(str, Enum):
    pending = "pending"
    started = "started"
    ended = "ended"
    expired = "expired"


class QuizInvite(BaseModel):
    type: InviteType
    targetid: str
    timestamp: float


class GetQuizSchema(BaseModel):
    id: str
    creator_id: str
    title: str = "Ok"
    questions: List[QuizQuestion]
    public: bool = False
    invitations: List[QuizInvite] = []
    timestamp: float
    timed_per_question: int
    question_per_session: int = 10
    max_contestant: int = 4
    is_creator: bool = False


class CreateQuizSchema(BaseModel):
    creator_id: str
    title: str = "Ok"
    questions: List[QuizQuestion]
    public: bool = False
    timed_per_question: int = 5
    public_leaderboard: Optional[bool]
    max_contestant: int = 4
    question_per_session: int = 10
    timestamp: float = 0


class Attempt(BaseModel):
    type: str = "single"
    id: Optional[str]
    quiz_id: str
    taker_id: str
    taker_name: str = ""
    score: int
    timestamp: float


class GetQuizesPaginatedSchema(BaseModel):
    per_page: int
    page: int
    data: List[GetQuizSchema]
    has_next: bool


class InviteSchema(BaseModel):
    type: InviteType = InviteType.anytime
    target_id: str
    quiz_id: str
    seen: bool = False


class InviteMultiplayerRequestSchema(BaseModel):
    target_ids: List[str]
    game_id: str


class InviteMultiplayerSchema(BaseModel):
    type: InviteType = InviteType.multiplayer
    target_id: str
    # quiz_id: str
    game_id: str
    url: str
    seen: bool = False


class InviteNotificationSchema(BaseModel):
    type: InviteType = InviteType.multiplayer
    target_id: str
    # quiz_id: str
    url: str
    game_id: Optional[str]
    msg: str = "You've been invited to play a game"


class GameSchema(BaseModel):
    creator_id: str
    type: str = "multiplayer"
    timestamp: float
    questions_count: int = 10
    state: GameState = GameState.pending
    members: list = []
    questions: List[QuizQuestion] = []
    scores: dict = dict()


class GetGameSchema(BaseModel):
    id: str
    creator_id: str
    type: str = "multiplayer"
    timestamp: float
    questions_count: int = 10
    state: GameState = GameState.pending
    members: list = []
    questions: List[QuizQuestion] = []
    scores: Optional[dict]


class Last(BaseModel):
    by: Optional[str]
    index: Optional[int]


class RedisGameData(BaseModel):
    scores: dict = dict()
    lock: int = 0
    last: Last = {"by": None, "index": -1}


class GetAttemptsPaginatedSchema(BaseModel):
    per_page: int
    page: int
    data: List[Attempt]
    has_next: bool


class LaunchSchema(BaseModel):
    game_id: str
    quiz_id: str
    message: str
    creator_id: str
