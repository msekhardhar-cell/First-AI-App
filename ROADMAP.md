# Development Roadmap: OmniChat

Repository: msekhardhar-cell/First-AI-App  
Tracking: Atomic Task Breakdown  

---

## 1. Repository & Environment Setup

- [x] **Task 1.1: Local Git Identity**  
  Configure repo-specific `user.name` and `user.email` to `msekhardhar-cell` and `msekhar.dhar@gmail.com`.
- [x] **Task 1.2: Dedicated SSH Key Configuration**  
  Generate `~/.ssh/id_ed25519_msekhardhar`, link in `~/.ssh/config` under `github.com-msekhardhar`, and point origin to the SSH alias.
- [x] **Task 1.3: Secret & Dependency Git Hygiene**  
  Create `.gitignore` covering virtual environments, temporary cache files, `.env`, and Streamlit secrets.
- [x] **Task 1.4: Environment Template**  
  Write `.env.example` defining `GEMINI_API_KEY`, `NOUS_API_KEY`, `GROQ_API_KEY`, and `DEFAULT_PROVIDER`.
- [x] **Task 1.5: Dependency Manifest**  
  Specify pinned requirements in `requirements.txt` (`streamlit`, `google-genai`, `groq`, `pypdf`, `python-dotenv`, `pillow`, `httpx`).
- [x] **Task 1.6: Virtual Environment Initialization**  
  Provision Python 3.12 virtual environment using `uv venv` and install all dependencies.

---

## 2. Design System & Base UI Layout

- [x] **Task 2.1: Design Token Variables Specification**  
  Define core colors, card elevations, border radii, and spacing grid in `src/design_tokens.py`.
- [x] **Task 2.2: Global Obsidian Dark Theme Stylesheet**  
  Implement `assets/style.css` covering dark backgrounds, glassmorphic card borders, and custom scrollbars.
- [x] **Task 2.3: Streamlit CSS Injection Hook**  
  Build `inject_design_tokens()` function to inject custom CSS directly into Streamlit's container.
- [x] **Task 2.4: Header & Status Bar**  
  Build top sticky bar with application title, active provider pill, and persona badge.
- [x] **Task 2.5: Collapsible Control Sidebar**  
  Implement sidebar sections for mode toggles, API keys, persona selection, file upload, and history actions.
- [x] **Task 2.6: Sample Prompt Chips**  
  Add clickable starter cards in empty chat state to trigger immediate sample questions.

---

## 3. Core Model Routing & Streaming Engine

- [x] **Task 3.1: Model Provider Registry**  
  Create `src/config.py` mapping provider identifiers to display names, context lengths, and default parameters.
- [x] **Task 3.2: Persona System Prompts**  
  Implement `src/personas.py` with tailored instructions for general, architecture, study, and summary roles.
- [x] **Task 3.3: Offline Judge Sandbox Module**  
  Build `src/sandbox_data.py` with pre-computed technical scenarios for keyless evaluator testing.
- [x] **Task 3.4: Sandbox Streaming Simulator**  
  Implement word-by-word streaming generator in `src/ai_engine.py` simulating typing latency without network calls.
- [x] **Task 3.5: Google Gemini 2.5 Flash Integration**  
  Implement `client.models.generate_content_stream` via the `google-genai` SDK with system instruction injection.
- [x] **Task 3.6: Nous Portal / OpenAI-Compatible SSE Client**  
  Implement streaming HTTP POST client using `httpx` to parse Server-Sent Events (`data: {...}`) from `https://inference-api.nousresearch.com/v1`.
- [x] **Task 3.7: Groq LPU Integration**  
  Implement streaming client via official `groq` SDK targeting `llama-3.3-70b-versatile`.
- [x] **Task 3.8: Failover & Graceful Error Boundary**  
  Add try/except wraps around API calls that display clear notices and seamlessly fall back to sandbox mode.

---

## 4. Multi-Model Battle Arena

- [x] **Task 4.1: Battle Mode State Storage**  
  Initialize `st.session_state.battle_messages` and `battle_votes` dictionary.
- [x] **Task 4.2: Contender Selector Controls**  
  Add dropdowns in sidebar to choose Model A (primary) and Model B (discovered free model).
- [x] **Task 4.3: Parallel Streaming Display**  
  Implement dual-column rendering (`col_stream_a`, `col_stream_b`) updating both placeholders during generation.
- [x] **Task 4.4: Execution Latency Timer**  
  Calculate elapsed time for each contender and display latency badges beneath outputs.
- [x] **Task 4.5: Interactive Judge Voting**  
  Add voting buttons ("Model A", "Model B", "Tie") with live vote counters stored in session state.

---

## 5. Artifact Canvas & Mermaid Diagram Pipeline

- [x] **Task 5.1: Artifact Regex Extractor**  
  Implement `extract_artifact()` in `app.py` parsing code fences for `mermaid` and programming languages.
- [x] **Task 5.2: Split-Screen Canvas Layout**  
  Configure two-column page grid allocating 58% width to chat thread and 42% width to the artifact canvas.
- [x] **Task 5.3: Mermaid.js Live Diagram Rendering**  
  Render extracted flowchart and sequence diagram syntax inside the canvas panel.
- [x] **Task 5.4: One-Click Diagram Export**  
  Add download button to export `.mmd` raw diagram files.
- [x] **Task 5.5: Syntax Highlighted Code Viewer**  
  Render programming code blocks with syntax highlighting and add file download button.
- [x] **Task 5.6: Canvas Empty-State Guide**  
  Display sample preview and guidance in the canvas when no artifact is active.

---

## 6. Document & Context Ingestion

- [x] **Task 6.1: Multi-File Ingestion Handler**  
  Implement file uploader supporting `.pdf`, `.py`, `.js`, `.md`, `.txt`, `.csv`, `.json`.
- [x] **Task 6.2: Plain Text File Parser**  
  Extract UTF-8 content from text and code files with replacement fallback for broken encodings.
- [x] **Task 6.3: PDF Extraction Pipeline**  
  Extract per-page text using `pypdf.PdfReader` with page-boundary markers.
- [x] **Task 6.4: Token Overhead Estimator**  
  Calculate character counts and estimate token overhead (`chars // 4`).
- [x] **Task 6.5: Context Injection Formatter**  
  Format parsed files into structured context blocks appended to the system instruction.

---

## 7. Interactive Study Quiz Engine

- [x] **Task 7.1: Quiz Question Schema**  
  Define structured format with question text, 4 choices, correct answer index, and explanation string.
- [x] **Task 7.2: Session State Quiz Manager**  
  Store user selections and answers in `st.session_state.quiz_answers`.
- [x] **Task 7.3: Interactive Radio Question Widget**  
  Render multiple choice questions with individual radio groups.
- [x] **Task 7.4: Immediate Answer Validation**  
  Display green success box on correct answer or red alert showing the correct answer and conceptual explanation.
- [x] **Task 7.5: Score Summary & Celebration Banner**  
  Tally total correct answers, calculate percentage score, and display completion banner.
- [x] **Task 7.6: Top-Bar Toggle Action**  
  Add button in header to toggle quiz drawer open and closed.

---

## 8. Free Model Scanner

- [x] **Task 8.1: Endpoint Discovery List**  
  Configure target model endpoints (Nous Portal inference API and OpenRouter catalog).
- [x] **Task 8.2: Network Fetch & Rate Handling**  
  Implement HTTP GET requests with short timeouts and user-agent headers.
- [x] **Task 8.3: Zero-Cost Model Filter**  
  Filter models by `:free` slug suffix and zero prompt/completion pricing values.
- [x] **Task 8.4: Fallback Catalog Cache**  
  Provide local fallback list of verified free models if external network calls fail.
- [x] **Task 8.5: Free Model Card Drawer**  
  Render 3-column card grid displaying model ID, name, context window, and provider.
- [x] **Task 8.6: Integration with Battle Mode**  
  Populate Model B dropdown directly with all discovered free models.

---

## 9. Quality Assurance & Edge Cases

- [x] **Task 9.1: Python Compilation Check**  
  Run `py_compile` across `app.py` and all modules in `src/`.
- [x] **Task 9.2: Local Streamlit Verification**  
  Verify local HTTP 200 response and headless launch on port 8505.
- [x] **Task 9.3: Missing Key Behavior**  
  Confirm app runs without throwing exceptions when all API keys are left blank.
- [x] **Task 9.4: Clean History Reset**  
  Confirm "Clear History" button wipes messages, artifacts, and reloads clean state.
- [x] **Task 9.5: Markdown Export Verification**  
  Verify "Export Chat" generates clean, valid Markdown file.

---

## 10. Documentation & Devpost Submission

- [x] **Task 10.1: Main Project README**  
  Write [README.md](README.md) with overview, architecture diagram, folder structure, and setup instructions.
- [x] **Task 10.2: Devpost Entry Form Package**  
  Write [DEVPOST_SUBMISSION.md](DEVPOST_SUBMISSION.md) with exact text for all submission fields.
- [x] **Task 10.3: Timed Video Walkthrough Script**  
  Write [DEMO_VIDEO_SCRIPT.md](DEMO_VIDEO_SCRIPT.md) with 2-minute step-by-step presentation script.
- [x] **Task 10.4: Clean Author Verification**  
  Ensure all git commits are authored by `msekhardhar-cell <msekhar.dhar@gmail.com>`.
- [x] **Task 10.5: Remote Git Synchronization**  
  Push all commits cleanly to `https://github.com/msekhardhar-cell/First-AI-App`.
