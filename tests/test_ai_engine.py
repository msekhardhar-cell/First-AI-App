"""Tests for AI Engine and streaming logic."""
import pytest
from src.ai_engine import stream_ai_response
from src.personas import PERSONAS

def test_sandbox_streaming():
    """Verify that sandbox mode returns tokens without needing an API key."""
    messages = [{"role": "user", "content": "Explain microservices vs monolith"}]
    stream = stream_ai_response(
        provider="sandbox",
        messages=messages,
        persona_id="architect"
    )
    tokens = list(stream)
    full_text = "".join(tokens)
    assert len(tokens) > 10
    assert "Modular Monolith" in full_text
    assert "Mermaid" in full_text or "flowchart" in full_text

def test_persona_system_prompt_retrieval():
    """Verify all personas have valid system instructions."""
    for pid, persona in PERSONAS.items():
        assert "name" in persona
        assert "system_prompt" in persona
        assert len(persona["system_prompt"]) > 20
