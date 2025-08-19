from io import StringIO
from datetime import date
from typing import Tuple
from src.schemas.reports import ReportQuery
from src.schemas.attendance import AttendanceQuery
from src.services.attendance_service import AttendanceService

class ReportsService:
    def __init__(self):
        self.attendance = AttendanceService()

    # PUBLIC_INTERFACE
    def attendance_csv(self, query: ReportQuery) -> Tuple[str, str]:
        """Generate CSV text and filename for attendance data."""
        rows = self.attendance.query(AttendanceQuery(
            class_id=query.class_id,
            student_id=query.student_id,
            start=query.start,
            end=query.end,
        ))
        buf = StringIO()
        buf.write("id,class_id,student_id,day,status\n")
        for r in rows:
            buf.write(f"{r.id},{r.class_id},{r.student_id},{r.day.isoformat()},{r.status}\n")
        filename = f"attendance_{date.today().isoformat()}.csv"
        return buf.getvalue(), filename
