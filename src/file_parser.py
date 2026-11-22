"""OmniChat AI - Multi-format Document and Code File Ingestion."""
import io
from typing import Dict, Any, List

def parse_uploaded_file(uploaded_file) -> Dict[str, Any]:
    """Parses an uploaded file (txt, py, md, pdf, csv, json) and returns structured text context."""
    filename = uploaded_file.name
    file_bytes = uploaded_file.getvalue()
    extension = filename.split(".")[-1].lower() if "." in filename else ""
    
    content = ""
    error = None
    
    try:
        if extension in ["txt", "py", "js", "ts", "json", "md", "csv", "html", "css", "yaml", "yml", "sh"]:
            content = file_bytes.decode("utf-8", errors="replace")
        elif extension == "pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                pages_text = []
                for i, page in enumerate(reader.pages):
                    t = page.extract_text()
                    if t:
                        pages_text.append(f"--- Page {i+1} ---\n{t}")
                content = "\n\n".join(pages_text)
                if not content.strip():
                    content = "[PDF parsed, but no selectable text found. Scanned image PDF?]"
            except Exception as e:
                error = f"PDF parsing error: {str(e)}"
        else:
            content = file_bytes.decode("utf-8", errors="replace")
    except Exception as e:
        error = f"Unable to read file: {str(e)}"
        
    char_count = len(content)
    est_tokens = char_count // 4
    
    return {
        "filename": filename,
        "extension": extension,
        "char_count": char_count,
        "est_tokens": est_tokens,
        "content": content,
        "error": error
    }

def format_context_for_prompt(files_data: List[Dict[str, Any]]) -> str:
    """Formats ingested files into a structured prompt context block."""
    if not files_data:
        return ""
    
    parts = ["\n[ATTACHED FILE CONTEXT START]"]
    for f in files_data:
        if f.get("content"):
            parts.append(f"\n--- FILE: {f['filename']} (Estimated tokens: {f['est_tokens']}) ---\n{f['content']}")
    parts.append("\n[ATTACHED FILE CONTEXT END]\n")
    return "\n".join(parts)
