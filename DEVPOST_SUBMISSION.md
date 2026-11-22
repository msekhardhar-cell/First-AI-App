# Devpost Submission Package — OmniChat AI

> **Ready-to-Submit Form Content for the [Build Your First AI App](https://build-your-first-ai-app.devpost.com/) Hackathon**  
> **Host / Sponsor:** Yasir Insights  
> **Track:** AI Chatbots & Intelligent Productivity / Study Assistants  
> **Public Repository:** [https://github.com/msekhardhar-cell/First-AI-App](https://github.com/msekhardhar-cell/First-AI-App)  
> **Author:** `msekhardhar-cell` (`msekhar.dhar@gmail.com`)  

---

## 📋 Field-by-Field Submission Details

### 1. Project Title
```text
OmniChat AI — Multimodal Assistant with Artifact Canvas, Model Battle & Free Model Radar
```

### 2. Elevator Pitch (Short Description / Tagline — under 200 chars)
```text
A modern, Figma-styled multimodal AI chatbot with an interactive Artifact Canvas, dual-model Battle Arena, automated Study Quiz engine, and real-time Free Model Radar.
```

### 3. Track Selection
- **Primary Track:** AI Chatbots
- **Secondary Track:** AI Study Assistants / Productivity Tools

### 4. Built With (Tags for Devpost)
```text
python, streamlit, google-gemini, nous-research, openrouter, groq, pypdf, figma-design-tokens, css, mermaid-js, markdown
```

---

## 📝 The Project Story (Exact Form Text)

### 💡 Inspiration
Most entry-level conversational AI applications are simple wrappers around a single API: they output plain text blocks into a basic chat box without visual hierarchy, provide no way to preview or interact with generated artifacts, and break immediately if a hackathon judge doesn't enter an active personal API key.

As students and engineers, we noticed that conversations are only the starting point. When an AI explains an architecture or writes code, users need to *see* the system diagrams, inspect the code in a dedicated workspace, test their comprehension with active-recall quizzes, and compare different model viewpoints. We built **OmniChat AI** to transform conversational AI into a complete, visual, and educational workspace.

---

### 🚀 What It Does
**OmniChat AI** is a production-grade, multimodal AI chatbot crafted with high-fidelity Figma design tokens. Key capabilities include:

1. **🎨 Interactive Artifact Canvas & Diagram Inspector:**
   - Detects structured deliverables (code, architecture blueprints, study guides) in the conversation and displays them in a dedicated split-screen workspace.
   - Auto-renders live **Mermaid.js flowcharts and system architecture diagrams** with one-click `.mmd` and code file exports.

2. **⚔️ Multi-Model "Battle / Compare" Mode:**
   - Evaluators can pit two models side-by-side (e.g., Google Gemini 2.5 Flash vs. an open-weights free model from Nous Portal).
   - Both models stream responses simultaneously on the exact same prompt, with live latency tracking and judge voting buttons.

3. **📡 Free Models Radar:**
   - Dynamically scans Nous Portal (`https://inference-api.nousresearch.com/v1/models`) and open endpoints to discover active zero-cost models in real-time (e.g., Qwen4 Max, Tencent Hy4 Flash, Solar Mini 4, LongCat, Gemma 4).

4. **🎯 Interactive Study Quiz Engine:**
   - Converts conversational context or uploaded notes into an interactive multiple-choice quiz with immediate green/red feedback, explanations, and final score reporting.

5. **⚡ Zero-Key Judge Sandbox Mode:**
   - Evaluators don't need an API key or credit card to test the app. Pre-packaged simulated scenarios allow instant verification of streaming, persona switching, quiz generation, and canvas rendering.

6. **📁 Multimodal Document Ingestion:**
   - Ingests `.pdf`, `.py`, `.js`, `.md`, `.txt`, `.csv`, and `.json` files, tracks token count overhead, and augments the conversational prompt.

7. **🎭 Adaptive Personas:**
   - Four distinct personas: *Omni Assistant* (General), *Senior Code Architect* (Tech Lead), *Academic Study Partner* (Socratic Tutor), and *Executive Summarizer* (High-Density Briefs).

---

### 🛠️ How We Built It
- **Frontend & UX:** Built using **Python** and **Streamlit**, heavily customized via custom CSS design tokens matching modern Figma systems (obsidian dark palette `#090d16`, glassmorphism, responsive grid layout, and accessible contrast).
- **Model Orchestration:** A modular multi-provider router supporting:
  - **Google Gemini 2.5 Flash** via the official `google-genai` SDK.
  - **Nous Portal Hermes 3 & Free Models** via an OpenAI-compatible HTTP streaming architecture.
  - **Groq LPU Inference** for ultra-low latency token generation.
  - **Judge Sandbox Engine** for zero-dependency offline evaluations.
- **Context & Parsing:** Integrated **PyPDF** and standard text decoders to extract text from multi-page documents and calculate estimated tokens.
- **Diagrams & Visuals:** Embedded **Mermaid.js** syntax detection and rendering directly in the Artifact Canvas.

---

### 🧗 Challenges We Ran Into
1. **Synchronizing Dual Real-Time Streams in Battle Mode:** Running two distinct LLM streams side-by-side in Streamlit required careful placeholder state management so that tokens from Model A and Model B rendered cleanly without interfering with each other.
2. **Dynamic Zero-Cost Model Discovery:** Filtering through over 400 models on the Nous Portal inference endpoint to dynamically isolate true zero-price (`prompt: 0, completion: 0`) and `:free` models without hitting rate limits.
3. **Artifact Boundary Detection:** Extracting code blocks and Mermaid diagrams from streaming Markdown in real-time without glitching intermediate partial tags.

---

### 🎉 Accomplishments That We're Proud Of
- A stunning, obsidian dark-mode interface that feels like a polished commercial developer tool (Linear / Vercel style).
- The dual-model Battle Arena that lets users observe different reasoning paradigms in real time.
- A dynamic Free Model Radar discovering 19+ zero-cost models on the fly.
- Zero barrier to entry: hackathon judges can stress-test every feature without entering a single API key.
- Complete adherence to security best practices (no leaked credentials, `.env.example`, MIT open-source license).

---

### 📚 What We Learned
- How to implement and enforce Figma-derived design token systems in Streamlit web apps.
- Building resilient OpenAI-compatible SSE streaming clients using Python's `httpx`.
- Developing educational pedagogical flows (interactive multiple-choice scoring with live feedback loops).

---

### 🔮 What's Next for OmniChat AI
- **Voice In / Voice Out:** Adding Web Speech API microphone input and speech synthesis for accessibility.
- **In-Browser Code Execution (WASM/Pyodide):** Allowing users to execute Python code directly in the Artifact Canvas.
- **Persistent Semantic Knowledge Base:** Integrating local vector embeddings for long-term document search across sessions.

---

## 🔗 Submission Links Checklist
- [x] **Public GitHub Repo:** [https://github.com/msekhardhar-cell/First-AI-App](https://github.com/msekhardhar-cell/First-AI-App)
- [x] **Video Demo Script:** Included in repository as `DEMO_VIDEO_SCRIPT.md`
- [x] **Testing Instructions:** Run locally with 2 commands or test online.
