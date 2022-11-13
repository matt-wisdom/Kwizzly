from fastapi import APIRouter

from .quiz import quiz_router
from .user import user_router

sub_router = APIRouter()
sub_router.include_router(user_router, prefix="/users", tags=["User"])
sub_router.include_router(quiz_router, prefix="/quiz", tags=["Quiz"])


__all__ = ["sub_router"]
