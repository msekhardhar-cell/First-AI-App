"""OmniChat AI - Dynamic Free Models Scanner for Nous Portal & Open Endpoints."""
import json
import urllib.request
from typing import List, Dict, Any

DEFAULT_ENDPOINTS = [
    {
        "name": "Nous Portal / Inference API",
        "url": "https://inference-api.nousresearch.com/v1/models"
    },
    {
        "name": "OpenRouter Public Free Models",
        "url": "https://openrouter.ai/api/v1/models"
    }
]

# Fallback curated list in case of network timeout
FALLBACK_FREE_MODELS = [
    {"id": "qwen/qwen4-max:free", "name": "Qwen: Qwen4 Max (free)", "context_length": 1000000, "provider": "Nous/Open API"},
    {"id": "tencent/hy4-flash:free", "name": "Tencent: Hy4 flash (free)", "context_length": 1048576, "provider": "Nous/Open API"},
    {"id": "stepfun/step-3.7-flash:free", "name": "StepFun: Step 3.7 Flash (free)", "context_length": 262144, "provider": "Nous/Open API"},
    {"id": "upstage/solar-mini4:free", "name": "Upstage: Solar Mini 4 (free)", "context_length": 524288, "provider": "Nous/Open API"},
    {"id": "meituan/longcat-2.5:free", "name": "LongCat-2.5:Free", "context_length": 1048576, "provider": "Nous/Open API"},
    {"id": "google/gemma-4-26b-a4b-it:free", "name": "Google: Gemma 4 (free)", "context_length": 128000, "provider": "OpenRouter"},
    {"id": "nvidia/nemotron-3.5-lightning:free", "name": "NVIDIA: Nemotron 3.5 Lightning (free)", "context_length": 131072, "provider": "OpenRouter"},
    {"id": "hermes-3-llama-3.1-8b:free", "name": "Nous Research: Hermes 3 8B (Free Sandbox)", "context_length": 128000, "provider": "Nous Portal"}
]

def scan_free_models() -> List[Dict[str, Any]]:
    """Dynamically queries the API endpoints and returns all discovered free models."""
    free_models = []
    seen_ids = set()

    for endpoint in DEFAULT_ENDPOINTS:
        try:
            req = urllib.request.Request(
                endpoint["url"],
                headers={"User-Agent": "OmniChat-AI/1.0", "Accept": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                models = data.get("data", [])
                
                for m in models:
                    mid = m.get("id", "")
                    if mid in seen_ids:
                        continue
                        
                    pricing = m.get("pricing", {})
                    try:
                        p_prompt = float(pricing.get("prompt", 1))
                        p_comp = float(pricing.get("completion", 1))
                        is_zero_cost = (p_prompt == 0.0 and p_comp == 0.0)
                    except (ValueError, TypeError):
                        is_zero_cost = False
                        
                    is_marked_free = ":free" in mid or ":free" in m.get("name", "").lower()
                    
                    if is_zero_cost or is_marked_free:
                        seen_ids.add(mid)
                        free_models.append({
                            "id": mid,
                            "name": m.get("name", mid),
                            "context_length": m.get("context_length", 32000),
                            "provider": endpoint["name"]
                        })
        except Exception:
            continue

    if not free_models:
        return FALLBACK_FREE_MODELS

    return free_models
