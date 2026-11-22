"""Tests for Free Model Scanner."""
from src.model_scanner import scan_free_models

def test_scan_free_models_returns_results():
    """Verify scanner discovers zero-cost models or uses verified fallback cache."""
    models = scan_free_models()
    assert isinstance(models, list)
    assert len(models) >= 5
    for m in models:
        assert "id" in m
        assert "name" in m
        assert "context_length" in m
        assert "provider" in m
