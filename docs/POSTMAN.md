# AOL Backend API — Postman Testing Guide

This guide gives you complete, up-to-date steps to test every endpoint and diagnose why metrics or event lists may show zero.

**Base URL**
- `http://localhost:8000` (server: `uvicorn app.main:app --reload`)

**Environment Variables**
- Database (Prisma/Postgres)
  - Prefer `DATABASE_URL` (e.g., `postgresql://user:pass@host:5432/aol`)
  - Or components: `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- Neo
  - `NEO_RPC_URL` (default `https://testnet1.neo.coz.io:443`)
  - `MONITOR_INTERVAL_SECONDS` (default `30`)
  - `MONITOR_SCAN_BACK_BLOCKS` (default `20`)
  - `NEO_RPC_URL_TESTNET` (optional; overrides testnet RPC)
  - `NEO_RPC_URL_MAINNET` (optional; set to your mainnet RPC)
- EVM
  - `WEB3_PROVIDER_URL` (required for EVM monitoring)
  - `EVM_MONITOR_INTERVAL_SECONDS` (optional)
  - `EVM_SCAN_BACK_BLOCKS` (default `100`)
- LLM (optional)
  - `GEMINI_API_KEY` or `GOOGLE_API_KEY`
  - Defaults loaded automatically from `.env` at backend startup

**Schema Setup**
- Ensure the Postgres schema is applied per `prisma/schema.prisma`; without tables, events won’t persist.
  - CLI example: `prisma db push --skip-generate`

## Postman Setup
- Create environment "AOL Local" with `baseUrl = http://localhost:8000`.
- Use `{{baseUrl}}` in all requests.

## Endpoints

**Health**
- Method: `GET`
- URL: `{{baseUrl}}/`
- Response: `{ "status": "backend alive" }`

**Health Detail**
- Method: `GET`
- URL: `{{baseUrl}}/health/detail`
- Response: `{ spoon_available, gemini_configured, elevenlabs_configured }`

**Metrics**
- Method: `GET`
- URL: `{{baseUrl}}/metrics`
- Response: `{ "metrics": { events_recorded, breaches_detected, spoon_calls, gemini_calls, heuristic_calls, ... } }`
- Note: Metrics are in-memory and reset on restart; they only increase when monitors or LLMs run.

**Run Agent**
- Method: `POST`
- URL: `{{baseUrl}}/run-agent`
- Body: `{ "prompt": "hello" }`
- Response:
  - `{ "response": "...", "source": "spoonos|echo", "provider": "gemini|openai|...", "model": "gemini-2.5-pro|...", "spoon_available": true|false, "required_key": "GOOGLE_API_KEY|OPENAI_API_KEY|...", "init_error": "...optional..." }`
- Notes: When SpoonOS is enabled and a provider key is set, `source` is `spoonos` and provider/model reflect the active configuration; otherwise `source` is `echo`.

Enable SpoonOS
- Install: `pip install spoon_ai`
- Configure provider API key (one of): `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`
- Optional defaults: `DEFAULT_LLM_PROVIDER` (e.g., `gemini`), `DEFAULT_MODEL` (e.g., `gemini-2.5-pro`)
- Verify: `GET {{baseUrl}}/health/detail` should return `{ "spoon_available": true, "openai_configured"|"gemini_configured": true }`
- Call: `POST {{baseUrl}}/run-agent` and confirm `{ "source": "spoonos" }` in the response when configured, otherwise `{ "source": "echo" }`.

**Register Contract (Neo address)**
- Method: `POST`
- URL: `{{baseUrl}}/register-contract`
- Body example:
```
{
  "contract_hash": "0xd2a4cff31913016155e38e474a2c06d08be276cf",
  "network": "testnet",
  "owner_email": "founder@example.com",
  "chain": "neo"
}
```
- Response: `{ "contract": { ... }, "analysis": { ... }, "exit_broadcast": null }`

**Register Contract (ABI)**
- Method: `POST`
- URL: `{{baseUrl}}/register-contract`
- Body example:
```
{
  "abi": { "methods": [{"name": "mint"}], "events": [{"name": "Transfer"}] },
  "network": "testnet",
  "owner_email": "founder@example.com",
  "chain": "neo"
}
```
- Response includes computed `monitoring_events`, `risk_level`, `breach_vectors`, `formatted_report`.

**Register Contract + ExitBroadcast (forces an event)**
- Method: `POST`
- URL: `{{baseUrl}}/register-contract`
- Body example:
```
{
  "contract_hash": "0xd2a4cff31913016155e38e474a2c06d08be276cf",
  "network": "testnet",
  "owner_email": "founder@example.com",
  "chain": "neo",
  "raw_tx_hex": "deadbeef"
}
```
- Notes: This records an `ExitBroadcast` event for the saved contract to validate persistence.

**List Contracts**
- Method: `GET`
- URL: `{{baseUrl}}/contracts`
- Response: `{ "contracts": [ { id, contract_hash, chain, active, ... }, ... ] }`

**Activate/Deactivate Contract**
- Method: `POST`
- URL: `{{baseUrl}}/contracts/{id}/activate`
- Body: `{ "active": true }`
- Response: `{ "contract": { ... } }`

**List Events (all or by contract)**
- Method: `GET`
- URL: `{{baseUrl}}/events`
- Query: `contract_id` (optional), `limit` (optional)
- Response: `{ "events": [ ... ] }`

**Contract Events With Range**
- Method: `GET`
- URL: `{{baseUrl}}/contracts/{contract_id}/events`
- Query: `range` (one of `1w`, `1m`, `3m`) or `from_ts`, `to_ts`, `limit`
- Response: `{ "events": [ ... ] }`

**Trigger One Scan**
- Method: `POST`
- URL: `{{baseUrl}}/monitor-once`
- Response: `{ "monitoring": { "scanned_blocks": N, "events_recorded": M } }` (scans testnet and mainnet when configured)

**Legal Analyze**
- Method: `POST`
- URL: `{{baseUrl}}/legal-analyze`
- Body example: `{ "abi": { ... }, "voice": false }`
- Response: `{ "report": { unfair, severity, reasons, recommendation }, "voice_path": null }`

**Exit Broadcast (Neo)**
- Method: `POST`
- URL: `{{baseUrl}}/exit`
- Body: `{ "raw_tx_hex": "00" }`
- Response: `{ "broadcast": { success, result|error } }`

**Analyze ABI**
- Method: `POST`
- URL: `{{baseUrl}}/analyze-abi`
- Body: `{ "abi": { ... } }`
- Response: `{ "analysis": { risk_level, monitoring_events, ... } }`

## Sample cURL
```
curl -s {{baseUrl}}/
curl -s {{baseUrl}}/health/detail
curl -s {{baseUrl}}/metrics

curl -s -X POST {{baseUrl}}/register-contract \
  -H "Content-Type: application/json" \
  -d '{
    "contract_hash": "0xd2a4cff31913016155e38e474a2c06d08be276cf",
    "network": "testnet",
    "owner_email": "founder@example.com",
    "chain": "neo"
  }'

curl -s {{baseUrl}}/contracts
curl -s -X POST {{baseUrl}}/contracts/<id>/activate -H "Content-Type: application/json" -d '{"active": false}'
curl -s "{{baseUrl}}/events?contract_id=<id>&limit=50"
curl -s "{{baseUrl}}/contracts/<id>/events?range=1w"
curl -s -X POST {{baseUrl}}/monitor-once
```

## Diagnosing "0 Metrics" and "No Events"
- Metrics are in-memory; they reset on backend restart.
- `events_recorded` increases only when `record_event` succeeds. Ensure:
  - DB schema applied and `DATABASE_URL` is set.
  - RPC endpoints (`NEO_RPC_URL`/`WEB3_PROVIDER_URL`) are reachable.
  - The contract hash and `chain` are correct (`neo` vs `evm`).
  - The scan-back window includes recent activity (`MONITOR_SCAN_BACK_BLOCKS`, `EVM_SCAN_BACK_BLOCKS`).
- To force an event for validation, register with `raw_tx_hex` (see above) and then:
  - `GET {{baseUrl}}/contracts/<id>/events?range=1w`
- LLM counters (`spoon_calls`, `gemini_calls`) increase only when those providers are configured and used; otherwise decisions use heuristics.
  - Ensure `GEMINI_API_KEY` is set for provider `gemini`.

## Troubleshooting
- `400 Provide either contract_hash or abi`: pass one of those in `POST /register-contract`.
- `RPC Error` or `No result`: verify your RPC env and network.
- `invalid project id`: update `WEB3_PROVIDER_URL` with a valid Infura project ID or alternative EVM RPC.
- No events: expand scan windows or confirm the contract is emitting events on the selected chain/network.
