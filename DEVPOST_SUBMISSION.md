# Devpost Submission - OmniChat

Project submission for the Build Your First AI App Hackathon on Devpost.
Hosted by Yasir Insights.
Category: AI Chatbots / Study & Productivity Tools.
Repo: https://github.com/msekhardhar-cell/First-AI-App
Developer: msekhardhar-cell (msekhar.dhar@gmail.com)

---

## Submission Details

### Project Title
OmniChat: Dual-Model Comparison, Artifact Canvas, and Free Model Scanner

### Elevator Pitch
A fast chat interface with side-by-side model comparison, an artifact canvas for code and diagrams, interactive quizzes, and an auto-scanner for free models.

### Track
- Primary: AI Chatbots
- Secondary: AI Study Assistants / Productivity Tools

### Built With
Python, Streamlit, Google Gemini API, Nous Research API, Groq, PyPDF, CSS, Mermaid.js

---

## Project Story

### Inspiration
Most simple chat interfaces dump long paragraphs of text into a single scroll window. When you ask for code or system architecture, reading raw text gets messy fast. You cannot preview the diagram, you cannot easily test whether you actually understood the concept, and you have no clean way to compare how different models answer the same question.

I wanted to build a workspace that handles these problems directly:
1. Keep the chat clean and put diagrams and code into a side canvas.
2. Allow quick side-by-side comparison between two models so you can check speed and answer quality.
3. Turn study notes into interactive multiple-choice questions right on screen.
4. Auto-detect free models available on open endpoints so anyone can run it without paying for API credits.

### What It Does
OmniChat provides four main tools:

- Side-by-side Model Battle: Pick two models (for example, Gemini Flash and an open-weights model from Nous Portal), send a prompt, and watch both stream responses at the same time. The app tracks completion time and lets you vote on the better answer.
- Artifact Canvas: When a response includes a system architecture diagram or code block, the canvas extracts it into a dedicated side panel, renders interactive Mermaid.js SVG diagrams with one-click export, and allows live in-canvas Python code execution with terminal output.
- Free Model Scanner: The app queries open inference endpoints (including Nous Portal) to find currently active zero-cost models and lists their context windows and IDs.
- Interactive Study Quiz: Click a button on any topic to generate a self-grading multiple-choice quiz with immediate answer feedback and score tracking.
- Context Ingestion: Upload code files, markdown, text, or PDFs to chat directly against your documents.
- Personas: Switch between general assistance, software architecture reviews, study tutoring, and brief summaries.
- Offline Sandbox: Pre-loaded responses and context-aware fallback so evaluators can test the entire interface and feature set without needing their own API keys.

### How I Built It
- Interface: Python with Streamlit. I used custom CSS for an obsidian dark theme, card borders, and responsive split columns matching the project Figma design tokens.
- Model Layer: A unified streaming handler supporting Google Gemini 2.5 Flash (`google-genai`), Groq LPUs (`qwen/qwen3.8-27b` and `openai/gpt-oss-120b`), and Nous Portal models (`httpx` streaming SSE).
- Document Parsing: PyPDF for PDF extraction, plus standard UTF-8 file readers for code and text files.
- Diagrams & Execution: Mermaid.js parsing to extract diagram code blocks and render interactive SVGs directly in the canvas, plus sandboxed Python subprocess execution.

### Challenges
- Dual Streaming in Streamlit: Running two live token streams side-by-side in real time required careful container management so both response boxes updated smoothly.
- Model Filtering: Parsing hundreds of models from open API catalogs to isolate genuinely free tiers without triggering rate limits.
- Clean Artifact Extraction: Parsing partial markdown streams so the diagram canvas updates cleanly as soon as the code block finishes.

### What I Learned
- Managing Server-Sent Events (SSE) streaming connections reliably across different API providers.
- Structuring modular Python applications that degrade gracefully to offline modes when keys are missing.
- Designing practical educational tools (instant quiz grading) that fit into everyday study routines.

### What Is Next
- Local SQLite caching for conversation search and history management.
- Multi-file workspace project exports.
- Speech-to-text input integration.

---

## Instructions for Evaluators
1. Clone the repo: `git clone https://github.com/msekhardhar-cell/First-AI-App.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch: `streamlit run app.py`
4. By default, the app starts in Sandbox Mode. You can click any prompt chip, test the model comparison, launch the interactive quiz, and inspect the artifact canvas without entering any API key.
