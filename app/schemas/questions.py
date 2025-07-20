from pydantic import BaseModel
from typing import List
from ..db.database import SessionLocal


class ChoiceBase(BaseModel):
    choice_text : str
    is_correct : bool

class QuestionBase(BaseModel):
    question_text : str
    choices : List[ChoiceBase]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()