"""OmniChat AI - Modern Multimodal AI Chatbot with Artifact Canvas, Battle Mode & Free Model Radar."""
import streamlit as st
import time
import json
import re
from src.config import AVAILABLE_MODELS, GEMINI_API_KEY, GROQ_API_KEY, NOUS_API_KEY, DEFAULT_PROVIDER
from src.design_tokens import inject_design_tokens
from src.personas import PERSONAS
from src.file_parser import parse_uploaded_file, format_context_for_prompt
from src.quiz_generator import render_interactive_quiz
from src.ai_engine import stream_ai_response
from src.model_scanner import scan_free_models

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
if "battle_messages" not in st.session_state:
    st.session_state.battle_messages = []
if "uploaded_files_data" not in st.session_state:
    st.session_state.uploaded_files_data = []
if "show_quiz" not in st.session_state:
    st.session_state.show_quiz = False
if "show_scanner" not in st.session_state:
    st.session_state.show_scanner = False
if "active_artifact" not in st.session_state:
    st.session_state.active_artifact = None
if "last_latency" not in st.session_state:
    st.session_state.last_latency = 0.0
if "discovered_free_models" not in st.session_state:
    st.session_state.discovered_free_models = scan_free_models()
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "Chat"  # "Chat" or "Battle"
if "battle_votes" not in st.session_state:
    st.session_state.battle_votes = {"Model A": 0, "Model B": 0, "Tie": 0}

# 4. Sidebar Controls
with st.sidebar:
    st.markdown("### ⚡ OmniChat Controls")
    
    # App Mode Switcher
    st.session_state.app_mode = st.radio(
        "Application Mode:",
        ["Standard Chat 💬", "Model Battle / Compare ⚔️"],
        index=0 if st.session_state.app_mode == "Chat" else 1
    )
    is_battle = "Battle" in st.session_state.app_mode
    
    st.divider()

    # Free Models Radar Quick Action
    st.markdown("### 📡 Free Models Radar")
    st.caption(f"**{len(st.session_state.discovered_free_models)}** free zero-cost models discovered.")
    if st.button("🔍 View / Rescan Free Models", use_container_width=True):
        st.session_state.discovered_free_models = scan_free_models()
        st.session_state.show_scanner = not st.session_state.show_scanner
        st.rerun()

    st.divider()

    if not is_battle:
        # Standard Single-Model Mode
        st.markdown("### 🧠 AI Model Provider")
        provider_options = list(AVAILABLE_MODELS.keys())
        selected_provider = st.selectbox(
            "Primary Provider:",
            options=provider_options,
            format_func=lambda k: f"{AVAILABLE_MODELS[k]['icon']} {AVAILABLE_MODELS[k]['name']}",
            index=0
        )
        
        # API Key Input
        api_key = ""
        if selected_provider == "gemini":
            api_key = st.text_input("Gemini API Key:", value=GEMINI_API_KEY, type="password")
            if not api_key:
                st.info("💡 Running in **Judge Sandbox Mode** (No key required).")
        elif selected_provider == "nous":
            api_key = st.text_input("Nous Portal API Key:", value=NOUS_API_KEY, type="password")
            if not api_key:
                st.info("💡 Running in **Nous Hermes Sandbox Synthesis**.")
        elif selected_provider == "groq":
            api_key = st.text_input("Groq API Key:", value=GROQ_API_KEY, type="password")
            if not api_key:
                st.info("💡 Running in **Judge Sandbox Mode**.")
        else:
            st.success("✅ **Sandbox Active**: Zero API key required.")
    else:
        # Battle Mode Controls
        st.markdown("### ⚔️ Battle Contenders")
        model_a_provider = st.selectbox(
            "Model A (Challenger 1):",
            ["gemini", "groq", "sandbox"],
            format_func=lambda k: f"{AVAILABLE_MODELS[k]['icon']} {AVAILABLE_MODELS[k]['name']}",
            index=0
        )
        
        free_model_names = [f"{m['name']} ({m['id']})" for m in st.session_state.discovered_free_models]
        selected_free_choice = st.selectbox(
            "Model B (Challenger 2 - Free Model Radar):",
            free_model_names,
            index=0
        )
        selected_free_model_id = selected_free_choice.split("(")[-1].replace(")", "").strip()
        selected_provider = model_a_provider
        api_key = GEMINI_API_KEY

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

    # Actions
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.battle_messages = []
        st.session_state.active_artifact = None
        st.rerun()

# 5. Top Header Banner
header_mode_badge = "⚔️ Model Battle Mode" if is_battle else f"● {AVAILABLE_MODELS[selected_provider]['badge']}"
st.markdown(f"""
<div class="omni-header">
    <div>
        <h1 class="omni-title">⚡ OmniChat AI</h1>
        <p style="margin: 0.2rem 0 0 0; color: #94a3b8; font-size: 0.9rem;">
            Devpost Challenge Edition • Multimodal Intelligence, Artifact Canvas & Free Model Radar
        </p>
    </div>
    <div style="display: flex; gap: 0.5rem; align-items: center;">
        <span class="omni-badge {'sandbox' if selected_provider == 'sandbox' or not api_key else ''}">
            {header_mode_badge}
        </span>
        <span class="omni-badge">
            {current_persona['icon']} {current_persona['name']}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. Top Action Row
col_head_left, col_head_right = st.columns([3, 1])
with col_head_left:
    st.markdown("""
    <span class="metric-pill">🎨 Figma Tokens</span>
    <span class="metric-pill">⚔️ Battle Mode</span>
    <span class="metric-pill">📡 Free Model Radar</span>
    <span class="metric-pill">📊 Interactive Quiz</span>
    """, unsafe_allow_html=True)
with col_head_right:
    quiz_button_label = "❌ Close Quiz" if st.session_state.show_quiz else "🎯 Launch Quiz"
    if st.button(quiz_button_label, use_container_width=True):
        st.session_state.show_quiz = not st.session_state.show_quiz
        st.rerun()

# 7. Discovered Free Models Drawer (if opened)
if st.session_state.show_scanner:
    with st.container():
        st.markdown("### 📡 Free Models Radar (Nous Portal & Open Endpoints)")
        st.caption("Live zero-cost models automatically scanned and ready for comparison.")
        
        # Display as an interactive cards table
        cols = st.columns(3)
        for i, m in enumerate(st.session_state.discovered_free_models[:9]):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="omni-card" style="padding: 0.9rem; margin-bottom: 0.6rem;">
                    <strong style="color: #c4b5fd;">{m['name']}</strong><br/>
                    <code style="font-size: 0.75rem; color: #06b6d4;">{m['id']}</code><br/>
                    <span style="font-size: 0.8rem; color: #94a3b8;">Context: {m['context_length']:,} tokens • {m['provider']}</span>
                </div>
                """, unsafe_allow_html=True)
        st.divider()

# 8. Interactive Quiz Drawer (if toggled)
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

# =====================================================================
# BATTLE MODE vs STANDARD CHAT MODE
# =====================================================================
if is_battle:
    st.markdown("### ⚔️ Model Battle Arena: Dual Response Comparison")
    st.caption("Submit a prompt to stream answers from two distinct models simultaneously and evaluate their reasoning, speed, and formatting.")
    
    battle_input = st.chat_input("Enter a challenge prompt for both models to answer...")
    
    # Render past battle turns
    for b_turn in st.session_state.battle_messages:
        st.markdown(f"**👤 Prompt:** {b_turn['prompt']}")
        col_res_a, col_res_b = st.columns(2)
        with col_res_a:
            st.markdown(f"#### 🅰️ {b_turn['model_a_name']}")
            st.markdown(f"<span class='metric-pill'>⏱️ {b_turn['latency_a']:.2f}s</span>", unsafe_allow_html=True)
            st.markdown(b_turn["response_a"])
        with col_res_b:
            st.markdown(f"#### 🅱️ {b_turn['model_b_name']}")
            st.markdown(f"<span class='metric-pill'>⏱️ {b_turn['latency_b']:.2f}s</span>", unsafe_allow_html=True)
            st.markdown(b_turn["response_b"])
        st.divider()

    # Trigger New Battle
    if battle_input:
        context_str = format_context_for_prompt(st.session_state.uploaded_files_data)
        history = [{"role": "user", "content": battle_input}]
        
        st.markdown(f"**👤 Prompt:** {battle_input}")
        col_stream_a, col_stream_b = st.columns(2)
        
        model_a_display = AVAILABLE_MODELS.get(model_a_provider, {}).get("name", "Model A")
        model_b_display = selected_free_choice.split("(")[0].strip()
        
        # Stream Model A
        with col_stream_a:
            st.markdown(f"#### 🅰️ {model_a_display}")
            holder_a = st.empty()
            text_a = ""
            t0_a = time.time()
            for chunk in stream_ai_response(model_a_provider, history, selected_persona_id, GEMINI_API_KEY, context_str):
                text_a += chunk
                holder_a.markdown(text_a + " ▌")
            holder_a.markdown(text_a)
            lat_a = time.time() - t0_a
            st.caption(f"⏱️ Finished in {lat_a:.2f}s")
            
        # Stream Model B (Nous / Free Model)
        with col_stream_b:
            st.markdown(f"#### 🅱️ {model_b_display}")
            holder_b = st.empty()
            text_b = ""
            t0_b = time.time()
            for chunk in stream_ai_response("nous", history, selected_persona_id, NOUS_API_KEY, context_str, model_name=selected_free_model_id):
                text_b += chunk
                holder_b.markdown(text_b + " ▌")
            holder_b.markdown(text_b)
            lat_b = time.time() - t0_b
            st.caption(f"⏱️ Finished in {lat_b:.2f}s")
            
        # Record Battle
        st.session_state.battle_messages.append({
            "prompt": battle_input,
            "model_a_name": model_a_display,
            "model_b_name": model_b_display,
            "response_a": text_a,
            "response_b": text_b,
            "latency_a": lat_a,
            "latency_b": lat_b
        })
        
        # Voting Row
        st.markdown("##### 🏆 Judge Vote:")
        col_v1, col_v2, col_v3 = st.columns(3)
        with col_v1:
            if st.button("👈 Model A was better"):
                st.session_state.battle_votes["Model A"] += 1
                st.success("Vote recorded for Model A!")
        with col_v2:
            if st.button("👉 Model B was better"):
                st.session_state.battle_votes["Model B"] += 1
                st.success("Vote recorded for Model B!")
        with col_v3:
            if st.button("🤝 It's a Tie"):
                st.session_state.battle_votes["Tie"] += 1
                st.info("Vote recorded as Tie!")
        st.rerun()

else:
    # --- STANDARD CHAT & ARTIFACT CANVAS MODE ---
    col_chat, col_canvas = st.columns([1.15, 0.85], gap="medium")

    # RIGHT COLUMN: ARTIFACT CANVAS
    with col_canvas:
        st.markdown("### 🎨 Artifact Canvas & Inspector")
        st.caption("Live code inspector, system architecture diagrams, and generated deliverables.")
        
        artifact = st.session_state.active_artifact
        if artifact:
            if artifact["type"] == "mermaid":
                st.markdown("#### 🗺️ Architecture / System Diagram")
                st.markdown(f"```mermaid\n{artifact['content']}\n```")
                st.download_button("📥 Download Mermaid Code", data=artifact["content"], file_name="diagram.mmd", use_container_width=True)
            elif artifact["type"] == "code":
                st.markdown(f"#### 💻 Generated Code ({artifact.get('lang', 'text')})")
                st.code(artifact["content"], language=artifact.get("lang", "text"))
                st.download_button("📥 Download Code File", data=artifact["content"], file_name=f"artifact.{artifact.get('lang', 'txt')}", use_container_width=True)
        else:
            st.info("💡 As you chat, generated code snippets, diagrams, and structured notes will automatically populate this interactive Canvas.")
            st.markdown("##### 🔍 Preview Capabilities:")
            sample_mermaid = """flowchart TD
    Client[Client App] --> API[FastAPI / Gemini]
    API --> Canvas[Live Artifact Canvas]
    API --> Quiz[Dynamic Quiz Engine]"""
            st.markdown(f"```mermaid\n{sample_mermaid}\n```")

    # LEFT COLUMN: CHAT INTERFACE
    with col_chat:
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

        user_input = st.chat_input("Ask OmniChat AI anything or type a prompt...")
        
        trigger_response = False
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            trigger_response = True
        elif st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            trigger_response = True

        if trigger_response:
            latest_user_msg = st.session_state.messages[-1]["content"]
            context_str = format_context_for_prompt(st.session_state.uploaded_files_data)
            
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
                
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            new_artifact = extract_artifact(full_response)
            if new_artifact:
                st.session_state.active_artifact = new_artifact
            st.rerun()
