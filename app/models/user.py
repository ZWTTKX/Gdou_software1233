# 用户相关（Student、Teacher、Counselor）


from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.config.database import Base


# 教师角色枚举
class TeacherRole(enum.Enum):
    NORMAL = "普通教师"
    HEAD_TEACHER = "班主任"

# 1. 辅导员模型
class Counselor(Base):
    __tablename__ = "counselor"
    counselor_id = Column(String(20), primary_key=True, comment="辅导员工号")
    counselor_name = Column(String(50), nullable=False, comment="辅导员姓名")
    department = Column(String(50), nullable=False, comment="所属院系")
    phone = Column(String(20), comment="联系电话")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")

    # 关联：负责的学生
    managed_students = relationship("Student", back_populates="counselor")

# 2. 教师模型（含班主任）
class Teacher(Base):
    __tablename__ = "teacher"
    teacher_id = Column(String(20), primary_key=True, comment="教师工号")
    teacher_name = Column(String(50), nullable=False, comment="教师姓名")
    role = Column(SQLEnum(TeacherRole), default=TeacherRole.NORMAL, comment="角色")
    class_id = Column(String(20), comment="班主任关联班级ID")
    phone = Column(String(20), comment="联系电话")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")

    # 关联：管理的学生（班主任）
    managed_students = relationship("Student", back_populates="head_teacher")

# 3. 学生模型（核心关联模型）
class Student(Base):
    __tablename__ = "student"
    student_id = Column(String(20), primary_key=True, comment="学号")
    student_name = Column(String(50), nullable=False, comment="学生姓名")
    class_id = Column(String(20), nullable=False, comment="班级ID")
    counselor_id = Column(String(20), nullable=False, comment="辅导员ID")
    head_teacher_id = Column(String(20), nullable=False, comment="班主任ID")
    phone = Column(String(20), nullable=False, comment="手机号")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")

    # 关联：辅导员（多对一）
    counselor = relationship("Counselor", back_populates="managed_students")
    # 关联：班主任（多对一）
    head_teacher = relationship("Teacher", back_populates="managed_students")
    # 关联：请假单（一对多）
    leave_applications = relationship("LeaveApplication", back_populates="student")
    # 关联：成绩（一对多）
    scores = relationship("Score", back_populates="student")
    # 关联：学业预警（一对多）
    warning_records = relationship("WarningRecord", back_populates="student")