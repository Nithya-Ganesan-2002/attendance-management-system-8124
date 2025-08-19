from typing import List, Optional
from src.repositories.memory import db, AttendanceRecord
from src.schemas.attendance import AttendanceMarkIn, AttendanceOut, AttendanceQuery, AttendanceSummary

class AttendanceService:
    def __init__(self):
        self.db = db

    # PUBLIC_INTERFACE
    def mark(self, payload: AttendanceMarkIn) -> Optional[AttendanceOut]:
        """Create or update an attendance record."""
        # idempotent per (student_id, class_id, day)
        existing_id = None
        for aid, rec in self.db.attendance.items():
            if rec.student_id == payload.student_id and rec.class_id == payload.class_id and rec.day == payload.day:
                existing_id = aid
                break

        if existing_id:
            rec = self.db.attendance[existing_id]
            rec.status = payload.status
            self.db.attendance[existing_id] = rec
            out = AttendanceOut(id=rec.id, student_id=rec.student_id, class_id=rec.class_id, day=rec.day, status=rec.status)
        else:
            aid = self.db.gen_id()
            rec = AttendanceRecord(
                id=aid,
                student_id=payload.student_id,
                class_id=payload.class_id,
                day=payload.day,
                status=payload.status,
            )
            self.db.attendance[aid] = rec
            out = AttendanceOut(id=rec.id, student_id=rec.student_id, class_id=rec.class_id, day=rec.day, status=rec.status)

        # Hook: broadcast to websocket listeners (no-op placeholder)
        # In a real deployment, inject a broadcaster or Supabase client here.
        return out

    # PUBLIC_INTERFACE
    def query(self, q: AttendanceQuery) -> List[AttendanceOut]:
        """Query attendance by filters."""
        res: List[AttendanceOut] = []
        for rec in self.db.attendance.values():
            if q.class_id and rec.class_id != q.class_id:
                continue
            if q.student_id and rec.student_id != q.student_id:
                continue
            if q.start and rec.day < q.start:
                continue
            if q.end and rec.day > q.end:
                continue
            res.append(AttendanceOut(id=rec.id, student_id=rec.student_id, class_id=rec.class_id, day=rec.day, status=rec.status))
        return res

    # PUBLIC_INTERFACE
    def summary(self, class_id: str) -> AttendanceSummary:
        """Summarize attendance for a class."""
        total = present = absent = late = 0
        for rec in self.db.attendance.values():
            if rec.class_id != class_id:
                continue
            total += 1
            if rec.status == "present":
                present += 1
            elif rec.status == "absent":
                absent += 1
            elif rec.status == "late":
                late += 1
        return AttendanceSummary(class_id=class_id, total=total, present=present, absent=absent, late=late)
