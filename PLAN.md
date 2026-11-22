# Project Plan: OmniChat

Hackathon: Build Your First AI App (Devpost)  
Track: AI Chatbots & Study/Productivity Assistants  
Repository: msekhardhar-cell/First-AI-App  
Developer: msekhardhar-cell (msekhar.dhar@gmail.com)  

---

## 1. Goal

Build an interactive chat application that goes beyond simple text streaming by providing:
- A dedicated side canvas for system diagrams and generated code.
- A side-by-side battle mode for comparing two models on the same prompt.
- An automated scanner that finds zero-cost models on open endpoints.
- Self-grading quizzes generated directly from the conversation.
- A sandbox mode so judges can evaluate all features without supplying their own API credentials.

---

## 2. Architecture and Technical Choices

- Framework: Python with Streamlit. Allows fast development of interactive components and reliable session state management.
- Styling: Custom CSS with an obsidian dark theme, consistent 8px grid spacing, and card borders.
- Models:
  - Google Gemini 2.5 Flash for reasoning and multimodal tasks.
  - Nous Portal Hermes 3 and open community models for open-weights comparison.
  - Groq Llama 3.3 for low latency token generation.
  - Built-in Sandbox engine for offline evaluation.
- Document Ingestion: PyPDF for PDF extraction, plus standard file decoders for source code, markdown, and plain text.
- Diagrams: Mermaid.js integration within the artifact canvas to render architecture and sequence diagrams.

---

## 3. Core Requirements

1. Real-time streaming for individual and dual-model modes.
2. Clean separation between conversation history and rendered deliverables.
3. Interactive self-grading quiz with immediate answer validation.
4. Auto-scanner to discover active zero-cost models from inference endpoints.
5. Zero dependency on API keys for base evaluation.
