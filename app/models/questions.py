from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..db.database import Base


class Questions(Base):
    __tablename__ ="questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    choices = relationship("Choices", backref="question", passive_deletes=True)


class Choices(Base):
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, index=True)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"))