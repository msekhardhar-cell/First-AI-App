"""OmniChat AI - Multi-Model Router & Streaming Engine."""
import time
from typing import Generator, List, Dict, Any
from src.sandbox_data import get_sandbox_response
from src.personas import PERSONAS

def stream_ai_response(
    provider: str,
    messages: List[Dict[str, str]],
    persona_id: str = "omni",
    api_key: str = "",
    file_context: str = ""
) -> Generator[str, None, None]:
    """Streams responses from the selected provider (Gemini, Groq, or Judge Sandbox)."""
    
    # 1. Retrieve persona system prompt
    persona = PERSONAS.get(persona_id, PERSONAS["omni"])
    system_instruction = persona["system_prompt"]
    if file_context:
        system_instruction += f"\n\nActive Ingested Context:\n{file_context}"
        
    last_user_query = messages[-1]["content"] if messages else ""

    # 2. Judge Sandbox Mode (Zero-key demo)
    if provider == "sandbox" or not api_key:
        full_text = get_sandbox_response(last_user_query, persona_id)
        # Simulate realistic word-by-word streaming typing effect
        words = full_text.split(" ")
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
            time.sleep(0.018)
        return

    # 3. Google Gemini Mode
    if provider == "gemini":
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            
            # Build conversation contents
            contents = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg["content"]}]})
                
            response_stream = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=contents,
                config={"system_instruction": system_instruction}
            )
            for chunk in response_stream:
                if chunk.text:
                    yield chunk.text
            return
        except Exception as e:
            err_msg = str(e)
            yield f"⚠️ **Gemini API Error:** {err_msg}\n\n*Falling back to Judge Sandbox Mode below:*\n\n"
            full_text = get_sandbox_response(last_user_query, persona_id)
            for word in full_text.split(" "):
                yield word + " "
                time.sleep(0.015)
            return

    # 4. Groq Mode
    if provider == "groq":
        try:
            from groq import Groq
            client = Groq(api_key=api_key)
            
            groq_messages = [{"role": "system", "content": system_instruction}]
            for msg in messages:
                groq_messages.append({"role": msg["role"], "content": msg["content"]})
                
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
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
            yield f"⚠️ **Groq API Error:** {err_msg}\n\n*Falling back to Judge Sandbox Mode below:*\n\n"
            full_text = get_sandbox_response(last_user_query, persona_id)
            for word in full_text.split(" "):
                yield word + " "
                time.sleep(0.015)
            return

    # Fallback default
    yield "Unrecognized model provider. Running in Sandbox mode."
