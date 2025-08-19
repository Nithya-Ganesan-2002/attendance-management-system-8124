from pydantic import BaseModel, Field

class ClassBase(BaseModel):
    name: str = Field(..., description="Class name")
    teacher_id: str = Field(..., description="Teacher user id")
    student_ids: list[str] = Field(default_factory=list, description="Student user ids")

class ClassCreate(ClassBase):
    pass

class ClassUpdate(BaseModel):
    name: str | None = Field(None, description="Class name")
    teacher_id: str | None = Field(None, description="Teacher user id")
    student_ids: list[str] | None = Field(None, description="Student user ids")

class ClassOut(ClassBase):
    id: str = Field(..., description="Class id")
