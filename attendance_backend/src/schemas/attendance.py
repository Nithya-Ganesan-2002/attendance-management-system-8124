from pydantic import BaseModel, Field
from datetime import date

class AttendanceMarkIn(BaseModel):
    class_id: str = Field(..., description="Class id")
    student_id: str = Field(..., description="Student id")
    day: date = Field(..., description="Attendance date")
    status: str = Field(..., description="present|absent|late")

class AttendanceOut(BaseModel):
    id: str = Field(..., description="Record id")
    class_id: str
    student_id: str
    day: date
    status: str

class AttendanceQuery(BaseModel):
    class_id: str | None = Field(None, description="Filter by class id")
    student_id: str | None = Field(None, description="Filter by student id")
    start: date | None = Field(None, description="Start date")
    end: date | None = Field(None, description="End date")

class AttendanceSummary(BaseModel):
    class_id: str
    total: int
    present: int
    absent: int
    late: int
