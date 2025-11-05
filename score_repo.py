from app.models.score import Score
from app.config.database import SessionLocal

db = SessionLocal()

def get_scores_by_course(course_id: int):
    return db.query(Score).filter(Score.course_id == course_id).all()

def upsert_score(course_id: int, student_id: int, score_value: float):
    score = db.query(Score).filter(
        Score.course_id == course_id, Score.student_id == student_id
    ).first()
    if not score:
        score = Score(course_id=course_id, student_id=student_id, score=score_value)
        db.add(score)
    else:
        score.score = score_value
    db.commit()
    return score
# 成绩数据操作