# Attendance Management Backend (FastAPI)

This backend exposes REST APIs for:
- Authentication (JWT)
- Users and roles (admin, teacher, student)
- Classes management
- Attendance marking and querying
- Reporting (CSV export)
- Real-time WebSocket endpoint for updates

Run (dev):
- Install deps: pip install -r requirements.txt
- Start: uvicorn src.api.main:app --reload --host 0.0.0.0 --port 3001
- Generate OpenAPI file: python -m src.api.generate_openapi

Environment
See ENVIRONMENT.md and .env.example for all variables.

Notes
- This scaffold uses an in-memory store for demo. Replace with persistent DB or integrate with the attendance_database container.
- Replace simple hashing and custom JWT with hardened implementations for production.
