# Thorax

**AI-Powered Smart Contract Security for Neo Blockchain**

Thorax is an intelligent blockchain security platform that combines SpoonOS AI agents with Neo blockchain infrastructure to provide real-time monitoring, risk analysis, and automated threat detection for smart contracts.

> 🏆 Built for the SpoonOS & Neo Hackathon - AI Agent with Web3 Track

## Features

- 🤖 **AI-Powered Analysis**: SpoonOS agents + Google Gemini for contract risk assessment
- 🔍 **Real-Time Monitoring**: Continuous blockchain scanning for suspicious events
- 🚨 **Automated Alerts**: Email notifications with optional AI voice synthesis
- ⚖️ **Legal Compliance**: Automated contract fairness and regulatory analysis
- 🌐 **Multi-Chain Support**: Neo (primary) and EVM chain compatibility
- 📊 **Risk Scoring**: 0-10 scale vulnerability assessment with breach vector detection

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL
- Neo RPC access (testnet/mainnet)

### Backend Setup

## Structure

- `app/main.py` defines the FastAPI `app` and all routes.
- `app/services/` contains storage, monitoring, Prisma, and utility services.
- `prisma/schema.prisma` defines the Postgres schema and Prisma client config.
- `tests/` contains API and service tests.

## Environment

Set via process environment (the app does not load `.env` automatically). Defaults exist where noted.

- Database
  - `DATABASE_URL` (postgres URL) or components:
    - `POSTGRES_HOST` (default `localhost`)
    - `POSTGRES_PORT` (default `5432`)
    - `POSTGRES_DB`   (default `aol`)
    - `POSTGRES_USER` (default `postgres`)
    - `POSTGRES_PASSWORD` (default `postgres`)
- NEO
  - `NEO_RPC_URL` (default `https://testnet1.neo.coz.io:443`)
  - `MONITOR_INTERVAL_SECONDS` (default `30`)
  - `MONITOR_SCAN_BACK_BLOCKS` (default `20`)
- EVM
  - `WEB3_PROVIDER_URL` (required for EVM monitoring)
  - `EVM_MONITOR_INTERVAL_SECONDS` (default fallback to `MONITOR_INTERVAL_SECONDS`)
  - `EVM_SCAN_BACK_BLOCKS` (default `100`)
- LLM
  - `GEMINI_API_KEY` or `GOOGLE_API_KEY`
- Optional
  - `ELEVENLABS_API_KEY`, `ELEVENLABS_VOICE_ID`, `ELEVENLABS_MODEL_ID`
  - SMTP settings: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM`

## Run Backend

1. Create a virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Unix)
3. Install dependencies: `pip install -r requirements.txt`
4. Set environment variables (see above)
5. Run Prisma migrations: `prisma generate && prisma db push`
6. Start the server: `uvicorn app.main:app --reload`

Backend runs at: `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend: `cd frontend`
2. Install dependencies: `npm install`
3. Create `.env.local`:
   ```
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
   ```
4. Start dev server: `npm run dev`

Frontend runs at: `http://localhost:3000`

## API Endpoints

### Core Endpoints
- `GET /` - Health check
- `GET /health/detail` - Runtime capabilities (SpoonOS, Gemini, ElevenLabs status)
- `GET /metrics` - System metrics (events, breaches, API calls)

### Contract Management
- `POST /register-contract` - Register new contract for monitoring
- `GET /contracts` - List all registered contracts
- `GET /contracts/{id}` - Get contract details
- `POST /contracts/{id}/activate` - Activate/deactivate monitoring
- `DELETE /contracts/{id}` - Delete contract

### Monitoring & Events
- `POST /monitor-once` - Trigger immediate blockchain scan
- `GET /events` - Get all events
- `GET /contracts/{id}/events` - Get events for specific contract
- `GET /logs/stream` - Real-time event stream (SSE)

### Analysis
- `POST /analyze-abi` - Analyze contract ABI for risks
- `POST /legal-analyze` - Legal compliance analysis
- `POST /notify` - Send manual alert to contract owner
- `POST /exit` - Broadcast raw transaction

## Test

- Run all tests: `pytest -q`
- Run specific test: `pytest tests/test_api.py -v`
- Run with coverage: `pytest --cov=app tests/`

## Architecture

```
aol-backend/
├── app/
│   ├── main.py              # FastAPI app & routes
│   ├── config.py            # Configuration
│   ├── services/            # Business logic
│   │   ├── storage.py       # Prisma database operations
│   │   ├── monitor.py       # Neo blockchain monitoring
│   │   ├── evm_monitor.py   # EVM chain monitoring
│   │   └── utils.py         # Helper functions
│   ├── tools/               # SpoonOS agent tools
│   └── agent/               # AI agent implementations
├── frontend/
│   ├── app/                 # Next.js pages
│   ├── components/          # React components
│   └── lib/                 # Utilities
├── prisma/
│   └── schema.prisma        # Database schema
└── tests/                   # Test suite
```

## SpoonOS Integration

AOL Guardian uses SpoonOS AI agents for:
- **Contract Analysis**: Autonomous agents analyze ABIs for security risks
- **Breach Detection**: Real-time event analysis to identify threats
- **Decision Making**: AI determines severity and recommended actions
- **Report Generation**: Formatted security reports with natural language explanations

## Neo Blockchain Integration

- **RPC Integration**: Direct connection to Neo nodes (testnet/mainnet)
- **Contract Notifications**: Monitors Neo's native notification system
- **Multi-Language Support**: Compatible with C#, Python, and other Neo languages
- **Fast Finality**: Leverages Neo's deterministic finality for reliable monitoring

## Use Cases

1. **DeFi Protocol Security**: Monitor for suspicious withdrawals and exploits
2. **NFT Marketplace Protection**: Track fraudulent minting and transfers
3. **DAO Governance Oversight**: Detect voting anomalies and treasury violations
4. **Token Contract Auditing**: Continuous monitoring of mint/burn events

## Contributing

This is a hackathon project. For issues or suggestions, please open a GitHub issue.

## License

MIT License

## Hackathon

Built for the **SpoonOS & Neo Hackathon** at Encode Hub. See [HACKATHON.md](./HACKATHON.md) for detailed submission information.

