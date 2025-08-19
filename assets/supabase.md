Supabase integration plan for Attendance Management System (backend)

Overview
- Supabase can be used for real-time broadcasting of attendance events and storing files (exports), as well as optionally user sync.

Backend usage points
1) Real-time broadcasts:
   - On new attendance mark/update, publish an event on a channel (e.g., "attendance:{class_id}").
   - Frontend subscribes to the channel to update live views.
   - Env vars used:
     - SUPABASE_URL
     - SUPABASE_ANON_KEY

2) Auth:
   - Current scaffold uses internal JWT. If using Supabase Auth, set SITE_URL for email redirect, and proxy verification.

Implementation notes
- Inject a broadcaster into AttendanceService.mark and call broadcaster.publish(...) after saving.
- Provide a supabase client in a module (lazy init using env vars) and handle errors gracefully.
- Do not hardcode env values—use ENV vars listed in attendance_backend/.env.example.

Security
- When enabling Supabase Auth, disable internal JWT or map Supabase JWT to internal roles carefully.
- Validate roles server-side.

Next steps
- Once Supabase config is finalized, update ENVIRONMENT.md and replace broadcast no-op with actual publish call.
