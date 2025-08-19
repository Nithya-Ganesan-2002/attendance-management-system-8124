from typing import List, Optional, Callable
from fastapi import Depends, HTTPException, status
from fastapi import WebSocket
from src.repositories.memory import db, UserRecord
from src.schemas.user import User, UserCreate, UserUpdate, UserRole
from src.core.security import get_password_hash, get_current_user_id
from src.core.security import _decode_token  # internal use for WS

class UsersService:
    def __init__(self):
        self.db = db

    # PUBLIC_INTERFACE
    def list_users(self) -> List[User]:
        """List all users."""
        return [User(id=u.id, name=u.name, email=u.email, role=u.role) for u in self.db.users.values()]

    # PUBLIC_INTERFACE
    def get(self, user_id: str) -> Optional[User]:
        """Get user by id."""
        u = self.db.users.get(user_id)
        if not u:
            return None
        return User(id=u.id, name=u.name, email=u.email, role=u.role)

    # PUBLIC_INTERFACE
    def get_by_email(self, email: str) -> Optional[UserRecord]:
        """Get internal user record by email."""
        for u in self.db.users.values():
            if u.email.lower() == email.lower():
                return u
        return None

    # PUBLIC_INTERFACE
    def create_user(self, payload: UserCreate) -> User:
        """Create user."""
        new_id = self.db.gen_id()
        rec = UserRecord(
            id=new_id,
            name=payload.name,
            email=payload.email,
            role=payload.role.value if isinstance(payload.role, UserRole) else payload.role,
            hashed_password=get_password_hash(payload.password),
        )
        self.db.users[new_id] = rec
        return User(id=rec.id, name=rec.name, email=rec.email, role=UserRole(rec.role))

    # PUBLIC_INTERFACE
    def update(self, user_id: str, payload: UserUpdate) -> Optional[User]:
        """Update user."""
        u = self.db.users.get(user_id)
        if not u:
            return None
        if payload.name is not None:
            u.name = payload.name
        if payload.role is not None:
            u.role = payload.role.value if isinstance(payload.role, UserRole) else payload.role
        self.db.users[user_id] = u
        return User(id=u.id, name=u.name, email=u.email, role=UserRole(u.role))

    # PUBLIC_INTERFACE
    def get_current_user(self, user_id: str = Depends(get_current_user_id)) -> User:
        """Resolve current user from Authorization header bearer token."""
        u = self.db.users.get(user_id)
        if not u:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return User(id=u.id, name=u.name, email=u.email, role=UserRole(u.role))

    # PUBLIC_INTERFACE
    async def get_current_user_ws(self, websocket: WebSocket) -> User:
        """
        Resolve current user for WebSocket connections using Authorization header.
        """
        auth = websocket.headers.get("Authorization")
        if not auth or not auth.lower().startswith("bearer "):
            await websocket.close(code=4401)  # Unauthorized
            raise HTTPException(status_code=401, detail="Missing token")
        token = auth.split(" ", 1)[1]
        payload = _decode_token(token)
        uid = payload.get("sub")
        u = self.db.users.get(uid)
        if not u:
            await websocket.close(code=4401)
            raise HTTPException(status_code=401, detail="Invalid user")
        return User(id=u.id, name=u.name, email=u.email, role=UserRole(u.role))

# PUBLIC_INTERFACE
def require_roles(roles: List[UserRole]) -> Callable[[User], None]:
    """Dependency to restrict access to specific roles."""
    def checker(current_user: User = Depends(UsersService().get_current_user)) -> None:
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
    return checker
