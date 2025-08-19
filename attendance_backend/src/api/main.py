from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.api.v1 import router as api_v1_router

def create_app() -> FastAPI:
    """
    Factory to create and configure the FastAPI application.
    """
    app = FastAPI(
        title="Attendance Management API",
        description="APIs for authentication, attendance tracking, class management, reporting, and real-time updates.",
        version="0.1.0",
        openapi_tags=[
            {"name": "health", "description": "Health and metadata"},
            {"name": "auth", "description": "Authentication and user session"},
            {"name": "users", "description": "User management and roles"},
            {"name": "classes", "description": "Class and teacher management"},
            {"name": "attendance", "description": "Attendance recording and history"},
            {"name": "reports", "description": "Report generation and exports"},
            {"name": "realtime", "description": "WebSocket endpoints for real-time updates"},
        ],
        contact={"name": "Attendance Platform", "email": "support@example.com"},
        license_info={"name": "Proprietary"},
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Root/health
    @app.get("/", tags=["health"], summary="Health Check")
    def health_check():
        """
        Health endpoint to verify service readiness.
        Returns message and environment info.
        """
        return {"message": "Healthy", "env": settings.APP_ENV}

    # WebSocket usage notes
    @app.get(
        "/realtime",
        tags=["realtime"],
        summary="Real-time WebSocket usage",
        description="Connect to /ws for receiving real-time attendance updates. "
                    "The client should authenticate via the Authorization header (Bearer) "
                    "or provide a valid token query parameter if supported by your client.",
    )
    def realtime_docs():
        return {
            "ws_endpoint": "/ws",
            "auth": "Bearer token in headers",
            "notes": "Server broadcasts updates on new attendance events."
        }

    # Include API v1
    app.include_router(api_v1_router, prefix="/api/v1")

    return app

app = create_app()
