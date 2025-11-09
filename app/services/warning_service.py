# 预警名单生成、辅导记录
# 预警名单生成、辅导记录
from app.repositories.warning_repo import WarningRepository
from app.repositories.student_repo import StudentRepository
from app.schemas.warning_schema import (
    WarningListResponse, WarningDetailSchema, 
    WarningStudentListSchema, WarningLevel,
    ExportWarningRequest
)
from app.utils.file_util import export_to_excel
from sqlalchemy.orm import Session
from typing import List, Dict
import io


class WarningService:
    @staticmethod
    def get_counselor_warning_students(db: Session, counselor_id: str, 
                                      warning_level: str = None) -> WarningListResponse:
        """获取辅导员负责的预警学生列表"""
        warning_students = WarningRepository.get_warning_students_by_counselor(
            db, counselor_id, warning_level
        )
        
        return WarningListResponse(
            total=len(warning_students),
            students=[WarningStudentListSchema(**student) for student in warning_students]
        )

    @staticmethod
    def get_student_warning_detail(db: Session, student_id: str) -> WarningDetailSchema:
        """获取学生预警详情"""
        detail = WarningRepository.get_student_warning_detail(db, student_id)
        if not detail:
            return None
        return WarningDetailSchema(** detail)

    @staticmethod
    def export_warning_list(db: Session, counselor_id: str, 
                           params: ExportWarningRequest) -> io.BytesIO:
        """导出预警名单为Excel"""
        # 获取符合条件的预警学生
        warning_students = WarningRepository.get_warning_students_by_counselor(
            db, counselor_id, params.warning_level
        )
        
        # 过滤班级（如果指定）
        if params.class_id:
            warning_students = [s for s in warning_students if s["class_id"] == params.class_id]
        
        # 准备导出数据
        export_data = []
        for student in warning_students:
            # 获取挂科详情
            student_detail = WarningRepository.get_student_warning_detail(
                db, student["student_id"]
            )
            
            failed_courses = ", ".join([
                f"{c['course_name']}({c['score']})" 
                for c in student_detail["current_semester_failed"]
            ])
            
            export_data.append({
                "学号": student["student_id"],
                "姓名": student["student_name"],
                "班级": student["class_id"],
                "预警等级": student["warning_level"].value,
                "挂科数量": student["failed_courses_count"],
                "挂科科目及成绩": failed_courses,
                "是否连续挂科": "是" if student["is_continuous"] else "否",
                "连续挂科学期": student["continuous_semesters"]
            })
        
        # 导出为Excel
        return export_to_excel(export_data, "学业预警名单")
