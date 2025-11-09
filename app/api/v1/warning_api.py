# 学业预警接口
# 学业预警接口
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.services.warning_service import WarningService
from app.schemas.warning_schema import (
    WarningListResponse, WarningDetailSchema,
    ExportWarningRequest, WarningLevel
)
from app.config.database import get_db
from app.api.dependencies import get_current_counselor
from fastapi.responses import StreamingResponse
import io

router = APIRouter(prefix="/warnings", tags=["学业预警"])


@router.get("/", response_model=WarningListResponse)
def get_warning_list(
    counselor_id: str = Depends(get_current_counselor),
    warning_level: WarningLevel = Query(None),
    db: Session = Depends(get_db)
):
    """获取辅导员负责的预警学生列表"""
    return WarningService.get_counselor_warning_students(
        db, counselor_id, warning_level.value if warning_level else None
    )


@router.get("/{student_id}", response_model=WarningDetailSchema)
def get_student_warning_detail(
    student_id: str,
    counselor_id: str = Depends(get_current_counselor),
    db: Session = Depends(get_db)
):
    """查看学生预警详情"""
    # 验证学生是否属于该辅导员
    student = WarningService.get_student_warning_detail(db, student_id)
    if not student or student.counselor_id != counselor_id:
        raise HTTPException(status_code=403, detail="无权访问该学生信息")
        
    return student


@router.post("/export")
def export_warning_list(
    params: ExportWarningRequest,
    counselor_id: str = Depends(get_current_counselor),
    db: Session = Depends(get_db)
):
    """导出预警名单"""
    excel_file = WarningService.export_warning_list(db, counselor_id, params)
    
    return StreamingResponse(
        io.BytesIO(excel_file.getvalue()),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=学业预警名单.xlsx"}
    )
