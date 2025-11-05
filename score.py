from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    score = Column(Float)

    student = relationship("Student", back_populates="scores")
    course = relationship("Course", back_populates="scores")
# 成绩相关（Score、ScoreFormula）