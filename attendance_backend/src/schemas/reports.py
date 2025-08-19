from pydantic import BaseModel, Field
from datetime import date

class ReportQuery(BaseModel):
    class_id: str | None = Field(None, description="Filter by class id")
    student_id: str | None = Field(None, description="Filter by student id")
    start: date | None = Field(None, description="Start date")
    end: date | None = Field(None, description="End date")
