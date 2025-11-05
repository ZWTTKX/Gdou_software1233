# 成绩接口from fastapi import APIRouter, HTTPException
# from fastapi.responses import StreamingResponse
# from app.services import score_service
# import io
#
# router = APIRouter(prefix="/scores", tags=["成绩管理"])
#
# @router.get("/{course_id}")
# def list_scores(course_id: int):
#     data = score_service.list_scores(course_id)
#     return [{"student_id": s.student_id, "score": s.score} for s in data]
#
# @router.post("/{course_id}")
# def update_scores(course_id: int, payload: dict):
#     if "grades" not in payload:
#         raise HTTPException(status_code=400, detail="缺少成绩数据")
#     return score_service.update_scores(course_id, payload["grades"])
#
# @router.get("/{course_id}/export")
# def export_scores(course_id: int, course_name: str = "未命名课程"):
#     file_stream = score_service.export_scores(course_name, course_id)
#     return StreamingResponse(
#         io.BytesIO(file_stream.read()),
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         headers={"Content-Disposition": f"attachment; filename={course_name}_成绩表.xlsx"}
#     )