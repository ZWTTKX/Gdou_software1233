# 学业预警相关DTO
# 学业预警相关DTO
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class WarningLevel(str, Enum):
    LEVEL_1 = "一级预警（挂科≥3门）"
    LEVEL_2 = "二级预警（挂科2门）"
    LEVEL_3 = "三级预警（挂科1门）"


class FailedCourseSchema(BaseModel):
    """挂科课程信息"""
    course_id: str
    course_name: str
    score: float
    semester: str


class WarningStudentListSchema(BaseModel):
    """预警学生列表项"""
    student_id: str
    student_name: str
    class_id: str
    warning_level: WarningLevel
    failed_courses_count: int
    latest_warning_time: datetime


class WarningDetailSchema(BaseModel):
    """预警详情"""
    student_id: str
    student_name: str
    class_id: str
    counselor_name: str
    head_teacher_name: str
    warning_level: WarningLevel
    current_semester_failed: List[FailedCourseSchema]
    historical_failed: List[FailedCourseSchema]
    is_continuous: bool
    continuous_semesters: int
    warning_records: List[dict]  # 历史预警记录


class WarningListResponse(BaseModel):
    """预警列表响应"""
    total: int
    students: List[WarningStudentListSchema]


class ExportWarningRequest(BaseModel):
    """导出预警名单请求"""
    class_id: Optional[str] = None
    warning_level: Optional[WarningLevel] = None
