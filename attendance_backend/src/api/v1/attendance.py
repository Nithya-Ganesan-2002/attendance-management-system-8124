from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.schemas.attendance import (
    AttendanceMarkIn,
    AttendanceOut,
    AttendanceQuery,
    AttendanceSummary,
)
from src.services.attendance_service import AttendanceService
from src.services.users_service import require_roles
from src.schemas.user import UserRole

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/mark", response_model=AttendanceOut, summary="Mark attendance")
def mark_attendance(
    payload: AttendanceMarkIn,
    svc: AttendanceService = Depends(AttendanceService),
    _: None = Depends(require_roles([UserRole.teacher])),
):
    """Mark attendance for a student in a class (teacher only)."""
    res = svc.mark(payload)
    if not res:
        raise HTTPException(status_code=400, detail="Unable to mark attendance")
    return res

# PUBLIC_INTERFACE
@router.post("/query", response_model=List[AttendanceOut], summary="Query attendance records")
def query_attendance(
    query: AttendanceQuery,
    svc: AttendanceService = Depends(AttendanceService),
):
    """
    Query attendance by date/class/student.
    """
    return svc.query(query)

# PUBLIC_INTERFACE
@router.get("/summary/{class_id}", response_model=AttendanceSummary, summary="Get class attendance summary")
def class_summary(
    class_id: str,
    svc: AttendanceService = Depends(AttendanceService),
):
    """Get summarized attendance stats for a class."""
    return svc.summary(class_id)
