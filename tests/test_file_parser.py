"""Tests for document context parsing."""
import io
from src.file_parser import parse_uploaded_file, format_context_for_prompt

class MockUploadedFile:
    def __init__(self, name: str, content: bytes):
        self.name = name
        self._content = content
    def getvalue(self):
        return self._content

def test_parse_code_file():
    mock_file = MockUploadedFile("test.py", b"def add(a, b):\n    return a + b\n")
    data = parse_uploaded_file(mock_file)
    assert data["filename"] == "test.py"
    assert data["extension"] == "py"
    assert "def add" in data["content"]
    assert data["est_tokens"] > 0

def test_format_context():
    files = [{"filename": "notes.md", "content": "Sample content", "est_tokens": 10}]
    formatted = format_context_for_prompt(files)
    assert "ATTACHED FILE CONTEXT START" in formatted
    assert "Sample content" in formatted
