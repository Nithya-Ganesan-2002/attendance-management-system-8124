from typing import List, Optional
from src.repositories.memory import db, ClassRecord
from src.schemas.clazz import ClassCreate, ClassOut, ClassUpdate

class ClassesService:
    def __init__(self):
        self.db = db

    # PUBLIC_INTERFACE
    def create(self, payload: ClassCreate) -> ClassOut:
        """Create a class record."""
        cid = self.db.gen_id()
        rec = ClassRecord(
            id=cid,
            name=payload.name,
            teacher_id=payload.teacher_id,
            student_ids=payload.student_ids or [],
        )
        self.db.classes[cid] = rec
        return ClassOut(id=rec.id, name=rec.name, teacher_id=rec.teacher_id, student_ids=rec.student_ids)

    # PUBLIC_INTERFACE
    def list(self) -> List[ClassOut]:
        """List classes."""
        return [
            ClassOut(id=c.id, name=c.name, teacher_id=c.teacher_id, student_ids=c.student_ids)
            for c in self.db.classes.values()
        ]

    # PUBLIC_INTERFACE
    def get(self, class_id: str) -> Optional[ClassOut]:
        """Get class by id."""
        c = self.db.classes.get(class_id)
        if not c:
            return None
        return ClassOut(id=c.id, name=c.name, teacher_id=c.teacher_id, student_ids=c.student_ids)

    # PUBLIC_INTERFACE
    def update(self, class_id: str, payload: ClassUpdate) -> Optional[ClassOut]:
        """Update class."""
        c = self.db.classes.get(class_id)
        if not c:
            return None
        if payload.name is not None:
            c.name = payload.name
        if payload.teacher_id is not None:
            c.teacher_id = payload.teacher_id
        if payload.student_ids is not None:
            c.student_ids = payload.student_ids
        self.db.classes[class_id] = c
        return ClassOut(id=c.id, name=c.name, teacher_id=c.teacher_id, student_ids=c.student_ids)
