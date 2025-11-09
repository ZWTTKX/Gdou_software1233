# 学业预警数据操作
from app.repositories.student_repo import StudentRepository
from app.repositories.score_repo import ScoreRepository

class WarningRepository:
    @staticmethod
    def get_warning_students_by_class(class_name, filter_grade=None):
        """查询指定班级的预警学生（结合学生和成绩数据）"""
        students = StudentRepository.get_by_class(class_name)
        warning_students = []
        for student in students:
            # 调用成绩仓库获取挂科数据（业务逻辑在service层处理）
            failed_courses = ScoreRepository.get_failed_courses(student.student_id)
            warning_students.append({
                "student": student,
                "failed_courses": failed_courses
            })
        return warning_students
