from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: str = None

    class Config:
        validate_assignment = True
