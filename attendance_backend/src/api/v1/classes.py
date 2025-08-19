from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.schemas.clazz import ClassCreate, ClassOut, ClassUpdate
from src.services.classes_service import ClassesService
from src.services.users_service import require_roles
from src.schemas.user import UserRole

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/", response_model=ClassOut, summary="Create class")
def create_class(
    payload: ClassCreate,
    svc: ClassesService = Depends(ClassesService),
    _: None = Depends(require_roles([UserRole.admin])),
):
    """Create a class (admin)."""
    return svc.create(payload)

# PUBLIC_INTERFACE
@router.get("/", response_model=List[ClassOut], summary="List classes")
def list_classes(svc: ClassesService = Depends(ClassesService)):
    """List all classes."""
    return svc.list()

# PUBLIC_INTERFACE
@router.get("/{class_id}", response_model=ClassOut, summary="Get class")
def get_class(class_id: str, svc: ClassesService = Depends(ClassesService)):
    """Get class by id."""
    c = svc.get(class_id)
    if not c:
        raise HTTPException(status_code=404, detail="Class not found")
    return c

# PUBLIC_INTERFACE
@router.patch("/{class_id}", response_model=ClassOut, summary="Update class")
def update_class(
    class_id: str,
    payload: ClassUpdate,
    svc: ClassesService = Depends(ClassesService),
    _: None = Depends(require_roles([UserRole.admin])),
):
    """Update class (admin)."""
    c = svc.update(class_id, payload)
    if not c:
        raise HTTPException(status_code=404, detail="Class not found")
    return c
