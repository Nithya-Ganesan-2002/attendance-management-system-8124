from fastapi import APIRouter, Depends, HTTPException
from typing import List
from src.schemas.user import User, UserUpdate, UserRole
from src.services.users_service import UsersService, require_roles

router = APIRouter()

# PUBLIC_INTERFACE
@router.get("/", response_model=List[User], summary="List users")
def list_users(
    svc: UsersService = Depends(UsersService),
    _: None = Depends(require_roles([UserRole.admin])),
):
    """List all users (admin only)."""
    return svc.list_users()

# PUBLIC_INTERFACE
@router.get("/{user_id}", response_model=User, summary="Get user by ID")
def get_user(user_id: str, svc: UsersService = Depends(UsersService)):
    """Get a user by ID."""
    user = svc.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# PUBLIC_INTERFACE
@router.patch("/{user_id}", response_model=User, summary="Update user")
def update_user(
    user_id: str,
    payload: UserUpdate,
    svc: UsersService = Depends(UsersService),
    _: None = Depends(require_roles([UserRole.admin])),
):
    """Update user (admin only)."""
    user = svc.update(user_id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
