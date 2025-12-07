import os
import json
import asyncio
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from app.agent.client import AgentClient
from app.services.storage import (
    create_contract,
    list_contracts,
    activate_contract,
    list_events,
    init_db,
    shutdown_db,
    list_events_range,
    record_event,
    get_contract,
    delete_contract,
)
from app.services.monitoring_service import start_monitoring_background, monitor_once
from app.services.evm_monitoring_service import start_evm_monitoring_background
from app.services.metrics_service import load_metrics_once, start_metrics_background
from app.utils.metrics import snapshot as metrics_snapshot
from app.services.legal_service import analyze_legal
from app.services.tx_service import send_raw_transaction
from app.services.abi_service import analyze_neo_abi
from test_contract_reader_agent import RealNeoContractTool
from app.utils.log_stream import sse_event_generator, emit as emit_log

app = FastAPI()
load_dotenv()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for audio alerts
alerts_dir = os.path.join(os.path.dirname(__file__), "alerts")
os.makedirs(alerts_dir, exist_ok=True)
app.mount("/audio", StaticFiles(directory=alerts_dir), name="audio")

agent = AgentClient()

@app.get("/")
def health():
    return {"status": "backend alive"}

class RunAgentRequest(BaseModel):
    prompt: str


@app.post("/run-agent")
async def run_agent(req: RunAgentRequest):
    meta = agent.metadata()
    if agent.is_spoon_available():
        result = await agent.arun(req.prompt)
        return {
            "response": result,
            "source": "spoonos",
            "provider": meta.get("provider"),
            "model": meta.get("model"),
            "spoon_available": True,
            "required_key": meta.get("required_key"),
            "init_error": meta.get("init_error"),
        }
    try:
        from spoon_ai.chat import ChatBot
        from spoon_ai.agents.toolcall import ToolCallAgent
        from spoon_ai.tools import ToolManager
        provider = os.getenv("DEFAULT_LLM_PROVIDER", "gemini").lower()
        model = os.getenv("DEFAULT_MODEL", "gemini-2.5-pro")
        class MinimalAgent(ToolCallAgent):
            name: str = "backend_minimal_agent"
            description: str = "Minimal SpoonOS agent"
            system_prompt: str = "You are an AOL backend AI agent."
            available_tools: ToolManager = ToolManager([])
        try:
            llm = ChatBot(llm_provider=provider, model_name=model)
        except Exception:
            llm = ChatBot(llm_provider=provider)
        a = MinimalAgent(llm=llm)
        result = await a.run(req.prompt)
        return {
            "response": result,
            "source": "spoonos",
            "provider": provider,
            "model": model,
            "spoon_available": True,
            "required_key": meta.get("required_key"),
            "init_error": None,
        }
    except Exception as e:
        result = req.prompt
        return {
            "response": result,
            "source": "echo",
            "provider": meta.get("provider"),
            "model": meta.get("model"),
            "spoon_available": False,
            "required_key": meta.get("required_key"),
            "init_error": str(e),
        }


class RegisterContractRequest(BaseModel):
    contract_hash: str | None = None
    abi: dict | None = None
    network: str = "testnet"
    owner_email: str | None = None
    raw_tx_hex: str | None = None
    chain: str = "neo"


@app.post("/register-contract")
async def register_contract(req: RegisterContractRequest):
    combined_analysis: dict = {}
    monitoring_events: List[str] = []
    contract_name: Optional[str] = None
    risk_level: int = 0
    breach_vectors: List[str] = []
    formatted_report: Optional[str] = None
    contract_hash: Optional[str] = req.contract_hash

    if req.abi:
        abi_analysis = analyze_neo_abi(req.abi)
        legal = analyze_legal(req.abi)
        combined_analysis = {
            "success": True,
            "risk_level": abi_analysis.get("risk_level", 0),
            "breach_vectors": abi_analysis.get("breach_vectors", []),
            "monitoring_events": abi_analysis.get("monitoring_events", []),
            "formatted_report": abi_analysis.get("formatted_report"),
            "legal": legal,
        }
        monitoring_events = combined_analysis["monitoring_events"]
        risk_level = combined_analysis["risk_level"]
        breach_vectors = combined_analysis["breach_vectors"]
        formatted_report = combined_analysis["formatted_report"]
        contract_name = "ABI-Registered Contract"
    elif req.contract_hash and req.chain.lower() == "neo":
        tool = RealNeoContractTool()
        analysis_raw = await tool.execute(req.contract_hash)
        try:
            analysis = json.loads(analysis_raw)
        except Exception:
            analysis = {"success": False}
        combined_analysis = analysis
        monitoring_events = analysis.get("monitoring_events") or []
        contract_name = analysis.get("contract_name")
        risk_level = int(analysis.get("risk_level") or 0)
        breach_vectors = analysis.get("breach_vectors") or []
        formatted_report = analysis.get("formatted_report")
        # Add legal based on manifest ABI if present
        abi_obj = (analysis.get("contract_data") or {}).get("abi")
        if abi_obj:
            combined_analysis["legal"] = analyze_legal(abi_obj)
    elif req.contract_hash:
        # Non-NEO address provided; skip NEO-specific analysis
        combined_analysis = {"success": True}
        monitoring_events = []
        contract_name = "Address-Registered Contract"
        risk_level = 0
        breach_vectors = []
        formatted_report = None
    else:
        raise HTTPException(status_code=400, detail="Provide either contract_hash or abi")

    default_owner = os.getenv("DEFAULT_OWNER_EMAIL", "chimamekamicheal@gmail.com")
    saved = await create_contract(
        contract_hash=contract_hash or "",
        network=req.network,
        monitoring_events=monitoring_events,
        owner_email=(req.owner_email or default_owner),
        active=True,
        contract_name=contract_name,
        risk_level=risk_level,
        breach_vectors=breach_vectors,
        formatted_report=formatted_report,
        chain=req.chain.lower(),
    )

    exit_broadcast_result = None
    if req.raw_tx_hex:
        exit_broadcast_result = send_raw_transaction(req.raw_tx_hex)
        try:
            await record_event(
                saved["id"],
                "ExitBroadcast",
                int(__import__("time").time()),
                {"raw_tx_hex": req.raw_tx_hex},
                "info",
                False,
                "Exit broadcast submitted",
            )
        except Exception:
            pass

    return {"contract": saved, "analysis": combined_analysis, "exit_broadcast": exit_broadcast_result, "ai_generated": True}


@app.get("/contracts")
async def get_contracts():
    return {"contracts": await list_contracts()}


class ActivateContractRequest(BaseModel):
    active: bool


@app.post("/contracts/{contract_id}/activate")
async def set_contract_active(contract_id: str, req: ActivateContractRequest):
    updated = await activate_contract(contract_id, req.active)
    try:
        await record_event(
            contract_id,
            "ActivationChanged",
            int(__import__("time").time()),
            {"active": bool(req.active)},
            "info",
            False,
            "Contract activation toggled",
        )
        emit_log({"type": "activation", "contract_id": contract_id, "active": bool(req.active)})
    except Exception:
        pass
    try:
        asyncio.create_task(monitor_once())
    except Exception:
        pass
    return {"contract": updated}


@app.delete("/contracts/{contract_id}")
async def delete_contract_endpoint(contract_id: str):
    ok = await delete_contract(contract_id)
    try:
        emit_log({"type": "delete", "contract_id": contract_id, "ok": ok})
    except Exception:
        pass
    if not ok:
        raise HTTPException(status_code=404, detail="Contract not found")
    return {"deleted": True}


class NotifyRequest(BaseModel):
    contract_id: str
    message: str
    voice: bool = True


@app.post("/notify")
async def notify(req: NotifyRequest):
    c = await get_contract(req.contract_id)
    if not c:
        raise HTTPException(status_code=404, detail="Contract not found")
    try:
        from app.services.email_service import EmailService
        mailer = EmailService()
        subject = f"Thorax Manual Alert: {c.get('contract_name') or c['contract_hash']}"
        body = req.message
        voice_path = None
        voice_url = None
        if req.voice:
            try:
                from app.services.tts_service import synthesize
                voice_path = synthesize(req.message)
                if voice_path:
                    # Convert file path to URL path
                    import os
                    filename = os.path.basename(voice_path)
                    voice_url = f"/audio/{filename}"
                    body += f"\nVoice alert generated"
            except Exception:
                voice_path = None
        mailer.send(c["owner_email"], subject, body)
        try:
            emit_log({"type": "notify", "contract_id": req.contract_id, "voice": bool(req.voice)})
        except Exception:
            pass
        return {"sent": True, "voice_url": voice_url, "voice_generated": bool(voice_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/events")
async def get_events(contract_id: Optional[str] = None, limit: int = 100):
    return {"events": await list_events(contract_id, limit)}


@app.get("/contracts/{contract_id}/events")
async def get_events_by_contract(contract_id: str, range: Optional[str] = None, from_ts: Optional[int] = None, to_ts: Optional[int] = None, limit: int = 200):
    presets = {"1w": 7 * 24 * 3600, "1m": 30 * 24 * 3600, "3m": 90 * 24 * 3600}
    now = int(__import__("time").time())
    if range in presets:
        from_ts = now - presets[range]
        to_ts = now
    events = await list_events_range(contract_id, from_ts, to_ts, limit)
    return {"events": events}


@app.on_event("startup")
async def startup_event():
    try:
        await init_db()
    except Exception:
        pass
    try:
        await load_metrics_once()
    except Exception:
        pass
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.get_event_loop()
    loop.call_soon(start_monitoring_background)
    loop.call_soon(start_evm_monitoring_background)
    loop.call_soon(start_metrics_background)


@app.on_event("shutdown")
async def shutdown_event():
    try:
        await shutdown_db()
    except Exception:
        pass


@app.post("/monitor-once")
async def monitor_once_endpoint():
    stats = await monitor_once()
    return {"monitoring": stats}


@app.get("/metrics")
def metrics():
    return {"metrics": metrics_snapshot()}


@app.get("/health/detail")
def health_detail():
    spoon_available = False
    try:
        import spoon_ai  # noqa: F401
        spoon_available = True
    except Exception:
        spoon_available = False
    gemini_configured = bool(os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))
    openai_configured = bool(os.getenv("OPENAI_API_KEY"))
    anthropic_configured = bool(os.getenv("ANTHROPIC_API_KEY"))
    deepseek_configured = bool(os.getenv("DEEPSEEK_API_KEY"))
    openrouter_configured = bool(os.getenv("OPENROUTER_API_KEY"))
    elevenlabs_configured = bool(os.getenv("ELEVENLABS_API_KEY"))
    return {
        "spoon_available": spoon_available,
        "gemini_configured": gemini_configured,
        "openai_configured": openai_configured,
        "anthropic_configured": anthropic_configured,
        "deepseek_configured": deepseek_configured,
        "openrouter_configured": openrouter_configured,
        "elevenlabs_configured": elevenlabs_configured,
    }


class LegalAnalyzeRequest(BaseModel):
    abi: dict
    source: Optional[str] = None
    voice: bool = False


@app.post("/legal-analyze")
def legal_analyze(req: LegalAnalyzeRequest):
    report = analyze_legal(req.abi, req.source)
    voice_path = None
    if req.voice:
        try:
            from app.services.tts_service import synthesize
            text = (
                f"Legal analysis: unfair={report.get('unfair')} severity={report.get('severity')}. "
                f"Reasons: {', '.join(report.get('reasons') or [])}. "
                f"Recommendation: {report.get('recommendation')}"
            )
            voice_path = synthesize(text)
        except Exception:
            voice_path = None
    return {"report": report, "voice_path": voice_path, "ai_generated": True}


class ExitRequest(BaseModel):
    raw_tx_hex: str


@app.post("/exit")
def exit_broadcast(req: ExitRequest):
    result = send_raw_transaction(req.raw_tx_hex)
    return {"broadcast": result}


class AbiAnalyzeRequest(BaseModel):
    abi: dict


@app.post("/analyze-abi")
def analyze_abi(req: AbiAnalyzeRequest):
    return {"analysis": analyze_neo_abi(req.abi), "ai_generated": True}
@app.get("/logs/stream")
async def logs_stream():
    return StreamingResponse(sse_event_generator(), media_type="text/event-stream")
