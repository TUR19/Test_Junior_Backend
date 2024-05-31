from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base


DB = declarative_base()


class Student(DB):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    grade = Column(String)

    scores = relationship("Score", back_populates="student")


class Score(DB):
    __tablename__ = 'scores'

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject = Column(String, index=True)
    score = Column(Integer)

    student = relationship("Student", back_populates="scores")
