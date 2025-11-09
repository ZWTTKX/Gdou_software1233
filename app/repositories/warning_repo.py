# 学业预警数据操作
from app.repositories.student_repo import StudentRepository
from app.repositories.score_repo import ScoreRepository
from app.models.early_warning import WarningRecord, WarningLevel
from sqlalchemy.orm import Session
from datetime import datetime


class WarningRepository:
    @staticmethod
    def get_warning_students_by_counselor(db: Session, counselor_id: str, warning_level: str = None):
        """查询辅导员负责的预警学生"""
        # 获取辅导员负责的所有学生
        students = StudentRepository.get_by_counselor(db, counselor_id)
        warning_students = []
        
        for student in students:
            # 获取学生当前学期挂科情况
            current_semester = "2023-2024-2"  # 实际应从系统配置获取当前学期
            failed_courses = ScoreRepository.get_failed_courses_by_semester(
                db, student.student_id, current_semester
            )
            
            if not failed_courses:
                continue
                
            # 计算预警等级
            failed_count = len(failed_courses)
            level = WarningLevel.LEVEL_3
            if failed_count >= 3:
                level = WarningLevel.LEVEL_1
            elif failed_count == 2:
                level = WarningLevel.LEVEL_2
                
            # 筛选等级
            if warning_level and level.value != warning_level:
                continue
                
            # 检查是否连续挂科
            continuous_info = ScoreRepository.check_continuous_failed(
                db, student.student_id
            )
            
            # 构建返回数据
            warning_students.append({
                "student_id": student.student_id,
                "student_name": student.student_name,
                "class_id": student.class_id,
                "warning_level": level,
                "failed_courses_count": failed_count,
                "latest_warning_time": datetime.now(),
                "continuous_semesters": continuous_info["semesters"],
                "is_continuous": continuous_info["is_continuous"]
            })
            
        return warning_students

    @staticmethod
    def get_student_warning_detail(db: Session, student_id: str):
        """获取学生预警详情"""
        student = StudentRepository.get_by_id(db, student_id)
        if not student:
            return None
            
        # 获取当前学期挂科情况
        current_semester = "2023-2024-2"
        current_failed = ScoreRepository.get_failed_courses_by_semester(
            db, student_id, current_semester
        )
        
        # 获取历史挂科情况
        historical_failed = ScoreRepository.get_historical_failed_courses(
            db, student_id
        )
        
        # 获取连续挂科信息
        continuous_info = ScoreRepository.check_continuous_failed(
            db, student_id
        )
        
        # 获取历史预警记录
        warning_records = db.query(WarningRecord).filter(
            WarningRecord.student_id == student_id
        ).order_by(WarningRecord.created_at.desc()).all()
        
        return {
            "student_id": student.student_id,
            "student_name": student.student_name,
            "class_id": student.class_id,
            "counselor_name": student.counselor.counselor_name,
            "head_teacher_name": student.head_teacher.teacher_name,
            "current_semester_failed": current_failed,
            "historical_failed": historical_failed,
            "is_continuous": continuous_info["is_continuous"],
            "continuous_semesters": continuous_info["semesters"],
            "warning_records": [{"id": r.id, "warning_level": r.warning_level.value, 
                                "warning_semester": r.warning_semester, 
                                "created_at": r.created_at} 
                               for r in warning_records]
        }

    @staticmethod
    def generate_warning_level(failed_count: int) -> WarningLevel:
        """根据挂科数量生成预警等级"""
        if failed_count >= 3:
            return WarningLevel.LEVEL_1
        elif failed_count == 2:
            return WarningLevel.LEVEL_2
        return WarningLevel.LEVEL_3
