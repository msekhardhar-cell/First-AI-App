"""OmniChat - Multi-Model Router & Streaming Engine."""
import time
import json
from typing import Generator, List, Dict, Any
from src.sandbox_data import get_sandbox_response
from src.personas import PERSONAS
from src.config import NOUS_BASE_URL, GROQ_API_KEY, GEMINI_API_KEY, NOUS_API_KEY

def stream_ai_response(
    provider: str,
    messages: List[Dict[str, str]],
    persona_id: str = "omni",
    api_key: str = "",
    file_context: str = "",
    model_name: str = ""
) -> Generator[str, None, None]:
    """Streams responses from the selected provider (Groq, Gemini, Nous, or Sandbox)."""
    
    persona = PERSONAS.get(persona_id, PERSONAS["omni"])
    system_instruction = persona["system_prompt"]
    if file_context:
        system_instruction += f"\n\nActive Ingested Context:\n{file_context}"
        
    last_user_query = messages[-1]["content"] if messages else ""

    # 1. Groq Mode (Primary high-speed live provider)
    active_groq_key = api_key if (api_key and provider.startswith("groq")) else GROQ_API_KEY
    if (provider in ["groq", "groq_qwen", "groq_gpt"] or "groq" in provider) and active_groq_key:
        try:
            from groq import Groq
            client = Groq(api_key=active_groq_key)
            
            target_model = model_name
            if not target_model:
                if provider == "groq_gpt":
                    target_model = "openai/gpt-oss-120b"
                else:
                    target_model = "qwen/qwen3.8-27b"
            
            # If target model is GPT-OSS and query involves prediction/astrology, fallback to Qwen
            # because GPT-OSS has a policy filter against fortune telling / prediction queries
            is_prediction_query = any(k in last_user_query.lower() for k in ["predict", "horoscope", "kundali", "astrology", "birth", "day"])
            if "gpt-oss" in target_model and is_prediction_query:
                target_model = "qwen/qwen3.8-27b"
                    
            groq_messages = [{"role": "system", "content": system_instruction}]
            for msg in messages:
                groq_messages.append({"role": msg["role"], "content": msg["content"]})
                
            stream = client.chat.completions.create(
                model=target_model,
                messages=groq_messages,
                stream=True,
                temperature=0.7
            )
            yielded_any = False
            for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                if content:
                    yielded_any = True
                    yield content
                    
            if yielded_any:
                return
        except Exception:
            # On transient failure, fall through to prompt-aware synthesis
            pass

    # 2. Google Gemini Mode
    active_gemini_key = api_key if (api_key and provider == "gemini") else GEMINI_API_KEY
    if provider == "gemini" and active_gemini_key:
        try:
            from google import genai
            client = genai.Client(api_key=active_gemini_key)
            
            contents = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg["content"]}]})
                
            response_stream = client.models.generate_content_stream(
                model=model_name or "gemini-2.5-flash",
                contents=contents,
                config={"system_instruction": system_instruction}
            )
            yielded_any = False
            for chunk in response_stream:
                if chunk.text:
                    yielded_any = True
                    yield chunk.text
            if yielded_any:
                return
        except Exception:
            # On quota exhaustion or failure, fall through to prompt-aware synthesis
            pass

    # 3. Nous Portal (OpenAI-compatible) Mode
    active_nous_key = api_key if (api_key and provider == "nous") else NOUS_API_KEY
    if provider == "nous" and active_nous_key:
        try:
            import httpx
            headers = {
                "Authorization": f"Bearer {active_nous_key}",
                "Content-Type": "application/json"
            }
            nous_messages = [{"role": "system", "content": system_instruction}]
            for msg in messages:
                nous_messages.append({"role": msg["role"], "content": msg["content"]})
                
            payload = {
                "model": model_name or "Hermes-3-Llama-3.1-8B",
                "messages": nous_messages,
                "stream": True,
                "temperature": 0.7
            }
            with httpx.Client(timeout=30.0) as client:
                with client.stream("POST", f"{NOUS_BASE_URL}/chat/completions", headers=headers, json=payload) as response:
                    if response.status_code == 200:
                        yielded_any = False
                        for line in response.iter_lines():
                            if line.startswith("data: ") and not line.strip() == "data: [DONE]":
                                data_str = line[6:].strip()
                                if data_str:
                                    chunk = json.loads(data_str)
                                    delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                    if delta:
                                        yielded_any = True
                                        yield delta
                        if yielded_any:
                            return
        except Exception:
            pass

    # 4. Prompt-Aware Dynamic Synthesis (Zero-key or fallback)
    hint = model_name or provider
    full_text = get_sandbox_response(last_user_query, persona_id, model_hint=hint)
    words = full_text.split(" ")
    for i, word in enumerate(words):
        yield word + (" " if i < len(words) - 1 else "")
        time.sleep(0.012)
