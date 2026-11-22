"""OmniChat AI - Configuration and environment manager."""
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "sandbox")

AVAILABLE_MODELS = {
    "sandbox": {
        "name": "Judge Sandbox (Zero-Key Demo)",
        "badge": "Sandbox Mode",
        "desc": "Pre-packaged rich scenarios for instant testing without API keys.",
        "icon": "⚡"
    },
    "gemini": {
        "name": "Google Gemini 2.5 Flash",
        "badge": "Gemini 2.5",
        "desc": "Google's fast, high-reasoning multimodal model.",
        "icon": "✨"
    },
    "groq": {
        "name": "Groq Llama 3.3 (70B)",
        "badge": "Llama 3.3",
        "desc": "Ultra-fast low-latency inference on LPUs.",
        "icon": "🚀"
    }
}
