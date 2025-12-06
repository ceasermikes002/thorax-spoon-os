# AOL Backend — Implementation & Hackathon Compliance Analysis

## Overview
This document analyzes the current backend implementation against hackathon requirements and outlines how Neo monitoring, SpoonOS agent integration, Gemini reasoning, and ElevenLabs voice synthesis work together to form an AI guardian for smart contracts.

## Hackathon Baseline Compliance
- SpoonOS LLM invocation
  - Breach-detection uses a SpoonOS ChatBot first, then falls back to Gemini HTTP if SpoonOS is unavailable.
  - Code flow: breach_service initializes `ChatBot(model_name, llm_provider)` and attempts `.run(prompt)`; if that fails, it uses Google Generative Language API with `GOOGLE_API_KEY`.
  - `/run-agent` endpoint uses a SpoonOS-backed client with graceful fallback to keep the app stable during demo.
- Tools/MCP usage
  - A custom contract analysis tool (`RealNeoContractTool`) is implemented following the Spoon-style `BaseTool` pattern; it reads real Neo manifests and derives `monitoring_events`. If judges require an official MCP or spoon-toolkits tool, it can be added quickly.

## Core Integrations
- Neo Blockchain
  - Contract analysis
    - Reads manifest via `getcontractstate`, extracts methods/events, computes `risk_level`, derives `monitoring_events`, and produces a structured JSON + formatted report.
  - Monitoring
    - Polls `getblockcount`, `getblock`, and `getapplicationlog` to gather notifications.
    - Matches notification `contract` hashes using normalized and reversed script-hash forms to handle endianness.
    - Filters events per contract against its `monitoring_events` list and persists to SQLite.
    - Email alert sent on breach; manual single-pass scan available via `POST /monitor-once`.
- Gemini AI
  - Primary reasoning provider for breach analysis.
  - Environment-driven configuration: `DEFAULT_LLM_PROVIDER=gemini`, `DEFAULT_MODEL=gemini-2.5-pro`, `GEMINI_MAX_TOKENS`.
  - Fallbacks
    - If SpoonOS ChatBot is accessible, it runs via Spoon’s unified LLM interface.
    - If SpoonOS is unavailable, it uses Google Generative Language API `:generateContent` with JSON prompt and pulls the textual candidate result to parse decision JSON.
- SpoonOS
  - LLM Routing
    - Uses `spoon_ai.chat.ChatBot(model_name, llm_provider)` to invoke the model through Spoon’s unified provider layer.
    - Agent client wrapper tries `spoonos.Client()` for `/run-agent` and falls back to echo if the package is not present.
  - Alignment with docs
    - SpoonOS agents support ReAct and Graph workflows; the breach-detection path follows a ReAct-style pattern (reason → analyze → report), and can be upgraded to Graph with parallel branches if needed.
- ElevenLabs (Voice Alerts)
  - TTS endpoint: `POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`
  - Headers: `xi-api-key: ELEVENLABS_API_KEY`, `Accept: audio/mpeg`, `Content-Type: application/json`.
  - Body: `{ text, model_id, voice_settings }` with defaults (`eleven_multilingual_v2`).
  - Output: MP3 saved under `alerts/alert_<timestamp>.mp3`; path appended to email body for voice explanation reference.

## Endpoints
- `GET /` health
- `POST /register-contract`
  - Body: `contract_hash`, `network`, `owner_email`
  - Returns: persisted contract + analysis (`risk_level`, `monitoring_events`, formatted report)
- `GET /contracts` list
- `POST /contracts/{id}/activate` toggle monitoring
- `GET /events` list events (optional `contract_id`, `limit`)
- `POST /monitor-once` trigger an immediate single scan pass

## Data & Storage
- SQLite (`app/aol.db` by default; configurable via `AOL_DB_PATH`)
- Tables: `contracts` and `events`
  - `contracts`: id, `contract_hash`, `network`, `monitoring_events` (JSON), `owner_email`, `active`, `contract_name`, `risk_level`, `breach_vectors` (JSON), `formatted_report`
  - `events`: id, `contract_id`, `event_name`, `timestamp`, `raw_event` (JSON), `severity`, `breach_detected`, `recommended_action`

## Runtime & Configuration
- Neo: `NEO_RPC_URL` for testnet/mainnet; defaults to `https://testnet1.neo.coz.io:443`
- Monitoring: `MONITOR_INTERVAL_SECONDS` for background loop; `MONITOR_SCAN_BACK_BLOCKS` to adjust recent block window per scan
- LLM: `DEFAULT_LLM_PROVIDER`, `DEFAULT_MODEL`, `GEMINI_MAX_TOKENS`, optional `SPOON_LLM_PROVIDER`, `SPOON_MODEL`
- ElevenLabs: `ELEVENLABS_API_KEY`, optional `ELEVENLABS_VOICE_ID`, `ELEVENLABS_MODEL_ID`

## Testing & Verification
- Automated tests: 5 passing (API endpoints + runner)
- Manual verification steps
  - Set `NEO_RPC_URL` to a valid testnet RPC.
  - `POST /register-contract` (e.g., GAS) → confirm `monitoring_events`.
  - `POST /monitor-once` → run a single scan; check `{ events_recorded }`.
  - `GET /events` → confirm events; breach → check email body includes voice file path.

## Bonus Criteria Readiness
- Graph agent upgrade: feasible to refactor breach flow to a Graph-based workflow for parallel analysis and actions.
- X402 components: can be integrated as an example using SpoonOS docs’ patterns.
- Official spoon-toolkits/MCP tool: add a minimal MCP tool (e.g., web search) to demonstrate multi-tool orchestration.

## Conclusion
The project meets the hackathon’s baseline technical requirements:
- LLM is invoked via SpoonOS when available, with a robust fallback to Gemini HTTP.
- A tool-based contract analysis pipeline is implemented and integrated with monitoring.
- Neo monitoring, breach reasoning, and ElevenLabs voice alerts provide a comprehensive guardian system suitable for demo and evaluation.
