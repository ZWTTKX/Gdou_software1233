# 学业预警相关（WarningRecord、GuidanceRecord）
# 学业预警相关（WarningRecord、GuidanceRecord）
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.config.database import Base


# 预警等级枚举
class WarningLevel(enum.Enum):
    LEVEL_1 = "一级预警（挂科≥3门）"
    LEVEL_2 = "二级预警（挂科2门）"
    LEVEL_3 = "三级预警（挂科1门）"


# 学业预警记录
class WarningRecord(Base):
    __tablename__ = "warning_record"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="预警记录ID")
    student_id = Column(String(20), ForeignKey("student.student_id"), nullable=False, comment="学生ID")
    warning_level = Column(Enum(WarningLevel), nullable=False, comment="预警等级")
    warning_semester = Column(String(20), nullable=False, comment="预警学期")
    failed_courses_count = Column(Integer, nullable=False, comment="挂科数量")
    failed_courses = Column(String(500), comment="挂科科目，用逗号分隔")
    is_continuous = Column(Integer, default=0, comment="是否连续挂科：0-否，1-是")
    continuous_semesters = Column(Integer, default=0, comment="连续挂科学期数")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    # 关联学生
    student = relationship("Student", back_populates="warning_records")
    # 关联辅导记录
    guidance_records = relationship("GuidanceRecord", back_populates="warning_record")


# 辅导记录
class GuidanceRecord(Base):
    __tablename__ = "guidance_record"
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment="辅导记录ID")
    warning_id = Column(Integer, ForeignKey("warning_record.id"), nullable=False, comment="预警记录ID")
    counselor_id = Column(String(20), ForeignKey("counselor.counselor_id"), nullable=False, comment="辅导员ID")
    guidance_time = Column(DateTime, nullable=False, comment="辅导时间")
    guidance_content = Column(String(1000), comment="辅导内容")
    follow_up_plan = Column(String(1000), comment="跟进计划")
    created_at = Column(DateTime, default=datetime.now, comment="记录创建时间")
    
    # 关联预警记录
    warning_record = relationship("WarningRecord", back_populates="guidance_records")
    # 关联辅导员
    counselor = relationship("Counselor")
