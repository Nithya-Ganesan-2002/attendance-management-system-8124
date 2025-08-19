from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict
import uuid
from datetime import date

@dataclass
class UserRecord:
    id: str
    name: str
    email: str
    role: str
    hashed_password: str

@dataclass
class ClassRecord:
    id: str
    name: str
    teacher_id: str
    student_ids: list[str] = field(default_factory=list)

@dataclass
class AttendanceRecord:
    id: str
    student_id: str
    class_id: str
    status: str  # "present" | "absent" | "late"
    day: date

class MemoryDB:
    def __init__(self):
        self.users: Dict[str, UserRecord] = {}
        self.classes: Dict[str, ClassRecord] = {}
        self.attendance: Dict[str, AttendanceRecord] = {}

    def gen_id(self) -> str:
        return str(uuid.uuid4())

# Singleton memory database for demo purposes
db = MemoryDB()
