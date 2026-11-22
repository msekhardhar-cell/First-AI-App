"""OmniChat AI - Modern Multimodal AI Chatbot with Artifact Canvas & Quiz Engine."""
import streamlit as st
import time
import json
import re
from src.config import AVAILABLE_MODELS, GEMINI_API_KEY, GROQ_API_KEY, DEFAULT_PROVIDER
from src.design_tokens import inject_design_tokens
from src.personas import PERSONAS
from src.file_parser import parse_uploaded_file, format_context_for_prompt
from src.quiz_generator import render_interactive_quiz
from src.ai_engine import stream_ai_response

# 1. Page Configuration
st.set_page_config(
    page_title="OmniChat AI — Intelligent Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Figma Design Tokens & CSS
inject_design_tokens()

# 3. Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_files_data" not in st.session_state:
    st.session_state.uploaded_files_data = []
if "show_quiz" not in st.session_state:
    st.session_state.show_quiz = False
if "active_artifact" not in st.session_state:
    st.session_state.active_artifact = None
if "last_latency" not in st.session_state:
    st.session_state.last_latency = 0.0

# 4. Sidebar Controls
with st.sidebar:
    st.markdown("### ⚡ OmniChat Controls")
    
    # Model Provider Selector
    provider_options = list(AVAILABLE_MODELS.keys())
    selected_provider = st.selectbox(
        "🧠 AI Model Provider:",
        options=provider_options,
        format_func=lambda k: f"{AVAILABLE_MODELS[k]['icon']} {AVAILABLE_MODELS[k]['name']}",
        index=0
    )
    
    # API Key Input
    api_key = ""
    if selected_provider == "gemini":
        api_key = st.text_input(
            "Gemini API Key:",
            value=GEMINI_API_KEY,
            type="password",
            help="Get a free key at https://aistudio.google.com/"
        )
        if not api_key:
            st.info("💡 No key entered? The app will seamlessly run in **Judge Sandbox Mode**.")
    elif selected_provider == "groq":
        api_key = st.text_input(
            "Groq API Key:",
            value=GROQ_API_KEY,
            type="password",
            help="Get a free key at https://console.groq.com/"
        )
        if not api_key:
            st.info("💡 No key entered? The app will seamlessly run in **Judge Sandbox Mode**.")
    else:
        st.success("✅ **Sandbox Mode Active**: Zero API key required. Perfect for immediate evaluator testing.")

    st.divider()

    # Persona Selector
    st.markdown("### 🎭 Persona & Role")
    persona_keys = list(PERSONAS.keys())
    selected_persona_id = st.selectbox(
        "Active Persona:",
        options=persona_keys,
        format_func=lambda k: f"{PERSONAS[k]['icon']} {PERSONAS[k]['name']}",
        index=0
    )
    current_persona = PERSONAS[selected_persona_id]
    st.caption(f"*{current_persona['tagline']}*")

    st.divider()

    # File Ingestion
    st.markdown("### 📁 Context & Documents")
    uploaded_files = st.file_uploader(
        "Attach Files (PDF, Code, Markdown, TXT):",
        type=["pdf", "py", "js", "md", "txt", "csv", "json"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.session_state.uploaded_files_data = [parse_uploaded_file(f) for f in uploaded_files]
        total_tokens = sum(f["est_tokens"] for f in st.session_state.uploaded_files_data)
        st.caption(f"📎 {len(uploaded_files)} file(s) attached (~{total_tokens:,} tokens)")
    else:
        st.session_state.uploaded_files_data = []

    st.divider()

    # Session Stats & Actions
    st.markdown("### 📊 Session Stats")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Messages", len(st.session_state.messages))
    with col_stat2:
        st.metric("Latency", f"{st.session_state.last_latency:.2f}s")

    # Export & Reset
    st.markdown("#### Actions")
    if st.session_state.messages:
        chat_markdown = "# OmniChat AI Conversation\n\n" + "\n\n".join(
            [f"**{m['role'].upper()}:**\n{m['content']}" for m in st.session_state.messages]
        )
        st.download_button(
            "📥 Export Chat (Markdown)",
            data=chat_markdown,
            file_name="omnichat_export.md",
            mime="text/markdown",
            use_container_width=True
        )
    
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.active_artifact = None
        st.rerun()

# 5. Top Header Banner
st.markdown(f"""
<div class="omni-header">
    <div>
        <h1 class="omni-title">⚡ OmniChat AI</h1>
        <p style="margin: 0.2rem 0 0 0; color: #94a3b8; font-size: 0.9rem;">
            Devpost Challenge Edition • Multimodal Intelligence with Artifact Canvas
        </p>
    </div>
    <div style="display: flex; gap: 0.5rem; align-items: center;">
        <span class="omni-badge {'sandbox' if selected_provider == 'sandbox' or not api_key else ''}">
            ● {AVAILABLE_MODELS[selected_provider]['badge']}
        </span>
        <span class="omni-badge">
            {current_persona['icon']} {current_persona['name']}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. Top Action Row (Quiz Toggle & Metric Pills)
col_head_left, col_head_right = st.columns([3, 1])
with col_head_left:
    st.markdown("""
    <span class="metric-pill">🎨 Figma Design Tokens</span>
    <span class="metric-pill">🚀 Multi-Model Routing</span>
    <span class="metric-pill">📑 Context Ingestion</span>
    <span class="metric-pill">📊 Interactive Quiz</span>
    """, unsafe_allow_html=True)
with col_head_right:
    quiz_button_label = "❌ Close Quiz" if st.session_state.show_quiz else "🎯 Launch Quiz"
    if st.button(quiz_button_label, use_container_width=True):
        st.session_state.show_quiz = not st.session_state.show_quiz
        st.rerun()

# 7. Interactive Quiz Drawer (if toggled)
if st.session_state.show_quiz:
    with st.container():
        render_interactive_quiz()
        st.divider()

# Helper function to extract Mermaid or Code Artifacts
def extract_artifact(text: str):
    mermaid_match = re.search(r"```mermaid\n(.*?)```", text, re.DOTALL)
    if mermaid_match:
        return {"type": "mermaid", "content": mermaid_match.group(1).strip()}
    
    code_match = re.search(r"```([a-zA-Z0-9]+)?\n(.*?)```", text, re.DOTALL)
    if code_match:
        lang = code_match.group(1) or "text"
        return {"type": "code", "lang": lang, "content": code_match.group(2).strip()}
    
    return None

# 8. Main Split Layout: Left (Chat Thread) & Right (Artifact Canvas)
col_chat, col_canvas = st.columns([1.15, 0.85], gap="medium")

# --- RIGHT COLUMN: ARTIFACT CANVAS ---
with col_canvas:
    st.markdown("### 🎨 Artifact Canvas & Inspector")
    st.caption("Live code inspector, system architecture diagrams, and generated deliverables.")
    
    artifact = st.session_state.active_artifact
    if artifact:
        if artifact["type"] == "mermaid":
            st.markdown("#### 🗺️ Architecture / System Diagram")
            st.markdown(f"""
            ```mermaid
            {artifact['content']}
            ```
            """)
            st.download_button(
                "📥 Download Mermaid Code",
                data=artifact["content"],
                file_name="diagram.mmd",
                mime="text/plain",
                use_container_width=True
            )
        elif artifact["type"] == "code":
            st.markdown(f"#### 💻 Generated Code ({artifact.get('lang', 'text')})")
            st.code(artifact["content"], language=artifact.get("lang", "text"))
            st.download_button(
                "📥 Download Code File",
                data=artifact["content"],
                file_name=f"artifact.{artifact.get('lang', 'txt')}",
                mime="text/plain",
                use_container_width=True
            )
    else:
        st.info("💡 As you chat, generated code snippets, diagrams, and structured notes will automatically populate this interactive Canvas.")
        
        # Showcase preview in empty state
        st.markdown("##### 🔍 Preview Capabilities:")
        sample_mermaid = """flowchart TD
    Client[Client App] --> API[FastAPI / Gemini]
    API --> Canvas[Live Artifact Canvas]
    API --> Quiz[Dynamic Quiz Engine]"""
        st.markdown(f"```mermaid\n{sample_mermaid}\n```")

# --- LEFT COLUMN: CHAT INTERFACE ---
with col_chat:
    # Starter Prompt Chips Carousel (when chat is empty)
    if not st.session_state.messages:
        st.markdown("#### 💡 Quick Starter Prompts")
        chip1, chip2 = st.columns(2)
        with chip1:
            if st.button("💻 Architect: Monolith vs Microservices", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Explain Microservices vs Modular Monolith with an architectural Mermaid diagram."})
                st.rerun()
            if st.button("🎓 Study: Quantum Entanglement simply", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Explain Quantum Entanglement simply with analogies and check-in questions."})
                st.rerun()
        with chip2:
            if st.button("⚡ Exec Brief: Project ROI Matrix", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "Provide an executive briefing and readiness matrix for this AI application."})
                st.rerun()
            if st.button("🎯 Test: 4-Question Interactive Quiz", use_container_width=True):
                st.session_state.show_quiz = True
                st.rerun()
        st.divider()

    # Render Chat History
    for msg in st.session_state.messages:
        role = msg["role"]
        avatar = "👤" if role == "user" else current_persona["icon"]
        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["content"])

    # Chat Input
    user_input = st.chat_input("Ask OmniChat AI anything or type a prompt...")
    
    # Process user query or auto-trigger from chips
    trigger_response = False
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        trigger_response = True
    elif st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        # Case where a starter prompt was clicked
        trigger_response = True

    if trigger_response:
        # Display the user's latest message if it was just entered
        latest_user_msg = st.session_state.messages[-1]["content"]
        
        # Prepare context from attached files
        context_str = format_context_for_prompt(st.session_state.uploaded_files_data)
        
        # Stream Assistant Response
        with st.chat_message("assistant", avatar=current_persona["icon"]):
            response_placeholder = st.empty()
            full_response = ""
            start_time = time.time()
            
            stream = stream_ai_response(
                provider=selected_provider,
                messages=st.session_state.messages,
                persona_id=selected_persona_id,
                api_key=api_key,
                file_context=context_str
            )
            
            for chunk in stream:
                full_response += chunk
                response_placeholder.markdown(full_response + " ▌")
            
            response_placeholder.markdown(full_response)
            elapsed = time.time() - start_time
            st.session_state.last_latency = elapsed
            
        # Append assistant reply to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Extract and update active artifact for right canvas
        new_artifact = extract_artifact(full_response)
        if new_artifact:
            st.session_state.active_artifact = new_artifact
            
        st.rerun()
