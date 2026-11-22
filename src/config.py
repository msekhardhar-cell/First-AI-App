"""OmniChat - Configuration and environment manager."""
import os
from dotenv import load_dotenv

load_dotenv()

# Automatically check local .env or fallback environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
NOUS_API_KEY = os.getenv("NOUS_API_KEY", "")
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "groq" if GROQ_API_KEY else "sandbox")

NOUS_BASE_URL = os.getenv("NOUS_BASE_URL", "https://inference-api.nousresearch.com/v1")

AVAILABLE_MODELS = {
    "groq_qwen": {
        "provider": "groq",
        "model": "qwen/qwen3.8-27b",
        "name": "Groq: Qwen 3.8 (27B)",
        "badge": "Qwen 3.8",
        "desc": "Fast reasoning and code generation on Groq LPUs.",
        "icon": "⚡"
    },
    "groq_gpt": {
        "provider": "groq",
        "model": "openai/gpt-oss-120b",
        "name": "Groq: GPT-OSS (120B)",
        "badge": "GPT-OSS 120B",
        "desc": "OpenAI flagship open-weights model on Groq LPUs.",
        "icon": "🚀"
    },
    "gemini": {
        "provider": "gemini",
        "model": "gemini-2.5-flash",
        "name": "Google Gemini 2.5 Flash",
        "badge": "Gemini 2.5",
        "desc": "Google's multimodal reasoning model.",
        "icon": "✨"
    },
    "nous": {
        "provider": "nous",
        "model": "Hermes-3-Llama-3.1-8B",
        "name": "Nous Portal Hermes 3",
        "badge": "Hermes 3",
        "desc": "Nous Research's open-weights model via OpenAI-compatible endpoint.",
        "icon": "🏛️"
    },
    "sandbox": {
        "provider": "sandbox",
        "model": "sandbox",
        "name": "Evaluator Sandbox (Offline)",
        "badge": "Sandbox Mode",
        "desc": "Simulated engine for testing features without API keys.",
        "icon": "🛡️"
    }
}
