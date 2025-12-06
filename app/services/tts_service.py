import os
import time
import requests


def synthesize(text: str, voice_id: str | None = None, model_id: str | None = None) -> str | None:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        return None
    vid = voice_id or os.getenv("ELEVENLABS_VOICE_ID") or "21m00Tcm4TlvDq8ikWAM"
    mid = model_id or os.getenv("ELEVENLABS_MODEL_ID") or "eleven_multilingual_v2"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}"
    headers = {"xi-api-key": api_key, "Accept": "audio/mpeg", "Content-Type": "application/json"}
    body = {"text": text, "model_id": mid, "voice_settings": {"stability": 0.4, "similarity_boost": 0.7}}
    try:
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if resp.status_code != 200:
            return None
        out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "alerts")
        os.makedirs(out_dir, exist_ok=True)
        fname = f"alert_{int(time.time())}.mp3"
        fpath = os.path.join(out_dir, fname)
        with open(fpath, "wb") as f:
            f.write(resp.content)
        return fpath
    except Exception:
        return None

