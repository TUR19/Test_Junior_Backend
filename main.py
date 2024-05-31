from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import DB, Student, Score
from pydantic import BaseModel


DATABASE_URL = "sqlite:///./students_scores.db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
DB.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class StudentCreate(BaseModel):
    name: str
    age: int
    grade: str


class ScoreCreate(BaseModel):
    student_id: int
    subject: str
    score: int


# CRUD for Students
@app.post("/students/", response_model=StudentCreate)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(name=student.name, age=student.age, grade=student.grade)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.patch("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student.name = student.name
    db_student.age = student.age
    db_student.grade = student.grade
    db.commit()
    db.refresh(db_student)
    return db_student


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"ok": True}


# CRUD for Scores
@app.post("/scores/", response_model=ScoreCreate)
def create_score(score: ScoreCreate, db: Session = Depends(get_db)):
    db_score = Score(student_id=score.student_id, subject=score.subject, score=score.score)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


@app.get("/scores/{score_id}")
def read_score(score_id: int, db: Session = Depends(get_db)):
    score = db.query(Score).filter(Score.id == score_id).first()
    if score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    return score


@app.patch("/scores/{score_id}")
def update_score(score_id: int, score: ScoreCreate, db: Session = Depends(get_db)):
    db_score = db.query(Score).filter(Score.id == score_id).first()
    if db_score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    db_score.subject = score.subject
    db_score.score = score.score
    db.commit()
    db.refresh(db_score)
    return db_score


@app.delete("/scores/{score_id}")
def delete_score(score_id: int, db: Session = Depends(get_db)):
    db_score = db.query(Score).filter(Score.id == score_id).first()
    if db_score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    db.delete(db_score)
    db.commit()
    return {"ok": True}
