from fastapi import APIRouter

from . import auth, users, classes, attendance, reports, websocket

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(classes.router, prefix="/classes", tags=["classes"])
router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
router.include_router(reports.router, prefix="/reports", tags=["reports"])
router.include_router(websocket.router, tags=["realtime"])
