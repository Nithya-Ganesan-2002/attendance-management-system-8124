from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.core.security import create_access_token, verify_password
from src.core.config import settings
from src.schemas.auth import Token
from src.schemas.user import User, UserCreate
from src.services.users_service import UsersService

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/register", response_model=User, summary="Register user")
def register_user(payload: UserCreate, svc: UsersService = Depends(UsersService)):
    """Register a new user (admin only can be enforced later)."""
    if svc.get_by_email(payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = svc.create_user(payload)
    return user

# PUBLIC_INTERFACE
@router.post("/login", response_model=Token, summary="Login and get access token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), svc: UsersService = Depends(UsersService)):
    """
    Authenticate user using email and password. Returns JWT access token.
    Note: OAuth2PasswordRequestForm uses 'username' field; pass email in 'username'.
    """
    user = svc.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token({"sub": str(user.id), "role": user.role}, expires_delta=access_token_expires)
    return Token(access_token=token, token_type="bearer")

# PUBLIC_INTERFACE
@router.get("/me", response_model=User, summary="Get current user")
def me(current_user: User = Depends(UsersService.get_current_user)):
    """Return the authenticated user's profile."""
    return current_user
