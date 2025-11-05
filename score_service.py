from app.repositories import score_repo
from app.utils.file_utils import export_to_excel

def list_scores(course_id: int):
    return score_repo.get_scores_by_course(course_id)

def update_scores(course_id: int, grade_list: list):
    for record in grade_list:
        score_repo.upsert_score(course_id, record["student_id"], record["score"])
    return {"message": "成绩更新成功"}

def export_scores(course_name: str, course_id: int):
    scores = list_scores(course_id)
    data = [["学生ID", "课程ID", "成绩"]]
    for s in scores:
        data.append([s.student_id, s.course_id, s.score])
    return export_to_excel(f"{course_name}_成绩表.xlsx", data)
# 成绩录入、计算、导出