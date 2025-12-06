## Current State
- FastAPI app with global `app` and inline routes in `app/main.py`.
- Background monitors for NEO and EVM start on startup; Prisma/Postgres used for persistence via `app/services/prisma_service.py`.
- Endpoints implemented and located as:
  - `GET /` → `app/main.py:36`
  - `POST /run-agent` → `app/main.py:44`
  - `POST /register-contract` → `app/main.py:59`
  - `GET /contracts` → `app/main.py:145`
  - `POST /contracts/{contract_id}/activate` → `app/main.py:154`
  - `GET /events` → `app/main.py:160`
  - `GET /contracts/{contract_id}/events` → `app/main.py:165`
  - `POST /monitor-once` → `app/main.py:186`
  - `GET /metrics` → `app/main.py:192`
  - `GET /health/detail` → `app/main.py:197`
  - `POST /legal-analyze` → `app/main.py:220`
  - `POST /exit` → `app/main.py:242`
  - `POST /analyze-abi` → `app/main.py:252`

## Issues To Fix
- Missing import causes silent failure to record `ExitBroadcast` events:
  - `await record_event(...)` in `app/main.py:130` is not imported; exception is swallowed.
- No shutdown hook to disconnect Prisma; may leak connections on reload.
- Startup event uses `get_event_loop()` and `call_soon` for monitors; modernizing to `get_running_loop()` improves reliability.
- Env loading relies on process env; `.env` is not loaded by the app. Tests and scripts do, but app should document required envs clearly.

## Implementation Plan
1. Fix event recording in `/register-contract`:
   - Import `record_event` from `app.services.storage` in `app/main.py` and keep `await` call.
2. Add Prisma shutdown hook:
   - Implement `@app.on_event("shutdown")` to `await prisma.disconnect()` via a small helper in `prisma_service.py`.
3. Harden startup and background tasks:
   - Switch to `asyncio.get_running_loop()` and wrap monitor starts defensively.
   - Optionally make `startup_event` async and `await init_db()` to ensure DB readiness before handling requests.
4. Validate endpoint inputs and responses:
   - Ensure all async paths `await` storage calls (already correct elsewhere).
   - Return consistent JSON shapes and meaningful HTTP status codes for error cases (use `HTTPException`).
5. Environment configuration:
   - Document required envs and defaults; ensure Prisma config builds `DATABASE_URL` when not set (already implemented).
6. Tests to guarantee seamless behavior:
   - Add integration tests for every endpoint, including a new test for `ExitBroadcast` event when `raw_tx_hex` is provided in `/register-contract`.
   - Add tests for EVM/NEO monitors with mocked RPC to validate persistence and metrics.
7. Verification:
   - Run `pytest` to confirm all tests pass.
   - Launch the app with `uvicorn app.main:app --reload` and manually hit endpoints; verify `GET /metrics` updates and `GET /events` shows recorded items.

## Environment Checklist
- DB: `DATABASE_URL` or `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`.
- NEO: `NEO_RPC_URL`, `MONITOR_INTERVAL_SECONDS`, `MONITOR_SCAN_BACK_BLOCKS`.
- EVM: `WEB3_PROVIDER_URL`, `EVM_MONITOR_INTERVAL_SECONDS`, `EVM_SCAN_BACK_BLOCKS`.
- LLM: `GEMINI_API_KEY` or `GOOGLE_API_KEY`.
- Optional: `ELEVENLABS_API_KEY` and voice settings, SMTP settings.

## Deliverables
- Code fixes for imports and lifecycle.
- Updated startup/shutdown for Prisma and monitors.
- Endpoint integration tests with 100% coverage of the listed routes.
- A short README section documenting env requirements and how to run/verify.

Please confirm and I will implement the fixes, add tests, and verify all endpoints end-to-end.