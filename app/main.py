from fastapi import FastAPI, HTTPException, Depends 
from sqlalchemy.orm import Session
from typing import List, Annotated
import uvicorn

from .db.database import Base
from .models.questions import Questions, Choices
from .schemas.questions import QuestionBase, ChoiceBase, get_db
from .db.database import engine


app = FastAPI()
Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/questions/{question_id}")
async def resd_question(question_id:int, db:db_dependency):
    result = db.query(Questions).filter(Questions.id==question_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Question does not exist.")
    return result



@app.post("/questions/")
async def create_questions(question:QuestionBase, db:db_dependency):
    db_question = Questions(question_text = question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = Choices(choice_text = choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)
        db.add(db_choice)
    
    db.commit()

@app.get("/choices/{question_id}")
async def resd_question(question_id:int, db:db_dependency):
    results = db.query(Choices).filter(Choices.question_id==question_id).all()
    if not results:
        raise HTTPException(status_code=404, detail="Question does not exist.")
    return results

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
