Environment variables required by the Attendance Management Backend:

Required for auth and app:
- APP_ENV: Application environment (development|staging|production). Default: development
- SECRET_KEY: Secret key for signing JWTs. Must be strong and unique in production.
- ACCESS_TOKEN_EXPIRE_MINUTES: Access token lifetime in minutes. Default: 120
- CORS_ALLOW_ORIGINS: Comma-separated list of origins allowed by CORS. Example: http://localhost:3000,https://your.app

Optional Supabase (for realtime, storage, etc.):
- SUPABASE_URL: Supabase project URL
- SUPABASE_ANON_KEY: Supabase anon/public key
- SITE_URL: External site URL (used by email redirect flows if implemented)

Notes:
- This scaffold uses an in-memory repository for demo and CI. Replace with a database integration (see 'attendance_database') as needed.
- For production: replace sha256 password hashing with bcrypt/argon2 and possibly a full JWT library.
