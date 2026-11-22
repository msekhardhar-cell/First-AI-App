"""OmniChat AI - Multi-Model Router & Streaming Engine."""
import time
import json
from typing import Generator, List, Dict, Any
from src.sandbox_data import get_sandbox_response
from src.personas import PERSONAS
from src.config import NOUS_BASE_URL

def stream_ai_response(
    provider: str,
    messages: List[Dict[str, str]],
    persona_id: str = "omni",
    api_key: str = "",
    file_context: str = "",
    model_name: str = ""
) -> Generator[str, None, None]:
    """Streams responses from the selected provider (Gemini, Nous Portal Hermes, Groq, or Judge Sandbox)."""
    
    # 1. Retrieve persona system prompt
    persona = PERSONAS.get(persona_id, PERSONAS["omni"])
    system_instruction = persona["system_prompt"]
    if file_context:
        system_instruction += f"\n\nActive Ingested Context:\n{file_context}"
        
    last_user_query = messages[-1]["content"] if messages else ""

    # 2. Judge Sandbox Mode (Zero-key demo)
    if provider == "sandbox" or not api_key:
        full_text = get_sandbox_response(last_user_query, persona_id, model_hint=provider or model_name)
        # Simulate realistic word-by-word streaming typing effect
        words = full_text.split(" ")
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
            time.sleep(0.016)
        return

    # 3. Google Gemini Mode
    if provider == "gemini":
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            
            contents = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg["content"]}]})
                
            response_stream = client.models.generate_content_stream(
                model=model_name or "gemini-2.5-flash",
                contents=contents,
                config={"system_instruction": system_instruction}
            )
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
            return
        except Exception as e:
            err_msg = str(e)
            yield f"⚠️ **Gemini API Notice:** {err_msg}\n\n*Falling back to Sandbox Mode:*\n\n"
            full_text = get_sandbox_response(last_user_query, persona_id, model_hint="gemini")
            for word in full_text.split(" "):
                yield word + " "
                time.sleep(0.015)
            return

    # 4. Nous Portal (Hermes 3) OpenAI-Compatible Mode
    if provider == "nous":
        try:
            import httpx
            headers = {
                "Authorization": f"Bearer {api_key}",
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
                    if response.status_code != 200:
                        raise ValueError(f"HTTP {response.status_code}: {response.read().decode('utf-8', errors='ignore')}")
                    for line in response.iter_lines():
                        if line.startswith("data: ") and not line.strip() == "data: [DONE]":
                            data_str = line[6:].strip()
                            if data_str:
                                chunk = json.loads(data_str)
                                delta = chunk.get("choices", [{}])[0].get("delta", {}).get("content", "")
                                if delta:
                                    yield delta
            return
        except Exception as e:
            err_msg = str(e)
            yield f"⚠️ **Nous Portal API Notice:** {err_msg}\n\n*Falling back to Nous Hermes Sandbox Synthesis:*\n\n"
            full_text = get_sandbox_response(last_user_query, persona_id, model_hint="nous")
            for word in full_text.split(" "):
                yield word + " "
                time.sleep(0.015)
            return

    # 5. Groq Mode
    if provider == "groq":
        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            
            groq_messages = [{"role": "system", "content": system_instruction}]
            for msg in messages:
                groq_messages.append({"role": msg["role"], "content": msg["content"]})
                
            stream = client.chat.completions.create(
                model=model_name or "llama-3.3-70b-versatile",
                messages=groq_messages,
                stream=True
            )
            for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                if content:
                    yield content
            return
        except Exception as e:
            err_msg = str(e)
            yield f"⚠️ **Groq API Notice:** {err_msg}\n\n*Falling back to Sandbox Mode:*\n\n"
            full_text = get_sandbox_response(last_user_query, persona_id, model_hint="groq")
            for word in full_text.split(" "):
                yield word + " "
                time.sleep(0.015)
            return

    # Fallback default
    yield "Unrecognized model provider. Running in Sandbox mode."
