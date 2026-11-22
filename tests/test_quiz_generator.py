"""Tests for interactive quiz data and structures."""
from src.quiz_generator import DEFAULT_QUIZ

def test_default_quiz_structure():
    assert len(DEFAULT_QUIZ) >= 3
    for q in DEFAULT_QUIZ:
        assert "id" in q
        assert "question" in q
        assert "options" in q
        assert len(q["options"]) == 4
        assert "correct" in q
        assert 0 <= q["correct"] < 4
        assert "explanation" in q
