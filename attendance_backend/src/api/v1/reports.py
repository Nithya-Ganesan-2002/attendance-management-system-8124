from fastapi import APIRouter, Depends, Response
from src.schemas.reports import ReportQuery
from src.services.reports_service import ReportsService
from src.services.users_service import require_roles
from src.schemas.user import UserRole

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/attendance/csv", summary="Export attendance CSV")
def export_attendance_csv(
    query: ReportQuery,
    svc: ReportsService = Depends(ReportsService),
    _: None = Depends(require_roles([UserRole.admin, UserRole.teacher])),
):
    """Generate a CSV export for attendance data filtered by class/date/student."""
    csv_text, filename = svc.attendance_csv(query)
    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
