"""OmniChat - Split-Screen Workspace with Model Battle, Artifact Canvas & Free Model Scanner."""
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
from src.mermaid_renderer import render_mermaid_svg
from src.code_runner import execute_python_code

# Page Configuration
st.set_page_config(
    page_title="OmniChat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
inject_design_tokens()

# Session State
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
if "code_run_result" not in st.session_state:
    st.session_state.code_run_result = None
if "last_latency" not in st.session_state:
    st.session_state.last_latency = 0.0
if "discovered_free_models" not in st.session_state:
    st.session_state.discovered_free_models = scan_free_models()
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "Chat"
if "battle_votes" not in st.session_state:
    st.session_state.battle_votes = {"Model A": 0, "Model B": 0, "Tie": 0}

# Sidebar Controls
with st.sidebar:
    st.markdown("### Settings")
    
    st.session_state.app_mode = st.radio(
        "Mode:",
        ["Standard Chat", "Model Battle & Compare"],
        index=0 if st.session_state.app_mode == "Chat" else 1
    )
    is_battle = "Battle" in st.session_state.app_mode
    
    st.divider()

    st.markdown("### Free Models Scanner")
    st.caption(f"**{len(st.session_state.discovered_free_models)}** free models detected on open endpoints.")
    if st.button("Scan / View Free Models", use_container_width=True):
        st.session_state.discovered_free_models = scan_free_models()
        st.session_state.show_scanner = not st.session_state.show_scanner
        st.rerun()

    st.divider()

    if not is_battle:
        st.markdown("### Model Selection")
        provider_options = list(AVAILABLE_MODELS.keys())
        selected_provider = st.selectbox(
            "Provider:",
            options=provider_options,
            format_func=lambda k: AVAILABLE_MODELS[k]["name"],
            index=0
        )
        
        api_key = ""
        if selected_provider == "gemini":
            api_key = st.text_input("Gemini API Key:", value=GEMINI_API_KEY, type="password")
            if not api_key:
                st.info("Running in Sandbox Mode (no key needed).")
        elif selected_provider == "nous":
            api_key = st.text_input("Nous Portal API Key:", value=NOUS_API_KEY, type="password")
            if not api_key:
                st.info("Running in Nous Hermes Sandbox.")
        elif selected_provider == "groq":
            api_key = st.text_input("Groq API Key:", value=GROQ_API_KEY, type="password")
            if not api_key:
                st.info("Running in Sandbox Mode.")
        else:
            st.success("Sandbox active: evaluate without an API key.")
    else:
        st.markdown("### Battle Setup")
        model_a_provider = st.selectbox(
            "Model A:",
            ["gemini", "groq", "sandbox"],
            format_func=lambda k: AVAILABLE_MODELS[k]["name"],
            index=0
        )
        
        free_model_names = [f"{m['name']} ({m['id']})" for m in st.session_state.discovered_free_models]
        selected_free_choice = st.selectbox(
            "Model B (Discovered Free Model):",
            free_model_names,
            index=0
        )
        selected_free_model_id = selected_free_choice.split("(")[-1].replace(")", "").strip()
        selected_provider = model_a_provider
        api_key = GEMINI_API_KEY

    st.divider()

    st.markdown("### Persona")
    persona_keys = list(PERSONAS.keys())
    selected_persona_id = st.selectbox(
        "Active Role:",
        options=persona_keys,
        format_func=lambda k: PERSONAS[k]["name"],
        index=0
    )
    current_persona = PERSONAS[selected_persona_id]

    st.divider()

    st.markdown("### Attach Files")
    uploaded_files = st.file_uploader(
        "Upload code, markdown, text, or PDF:",
        type=["pdf", "py", "js", "md", "txt", "csv", "json"],
        accept_multiple_files=True
    )
    if uploaded_files:
        st.session_state.uploaded_files_data = [parse_uploaded_file(f) for f in uploaded_files]
        total_tokens = sum(f["est_tokens"] for f in st.session_state.uploaded_files_data)
        st.caption(f"{len(uploaded_files)} file(s) attached (~{total_tokens:,} tokens)")
    else:
        st.session_state.uploaded_files_data = []

    st.divider()

    if st.button("Clear History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.battle_messages = []
        st.session_state.active_artifact = None
        st.session_state.code_run_result = None
        st.rerun()

# Top Header
header_mode_badge = "Battle Mode" if is_battle else AVAILABLE_MODELS[selected_provider]["badge"]
st.markdown(f"""
<div class="omni-header">
    <div>
        <h1 class="omni-title">OmniChat</h1>
        <p style="margin: 0.2rem 0 0 0; color: #94a3b8; font-size: 0.9rem;">
            Model Battle, Artifact Canvas & Free Model Scanner
        </p>
    </div>
    <div style="display: flex; gap: 0.5rem; align-items: center;">
        <span class="omni-badge {'sandbox' if selected_provider == 'sandbox' or not api_key else ''}">
            {header_mode_badge}
        </span>
        <span class="omni-badge">
            {current_persona['name']}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Action Row
col_head_left, col_head_right = st.columns([3, 1])
with col_head_left:
    st.markdown("""
    <span class="metric-pill">Figma Design Tokens</span>
    <span class="metric-pill">Model Battle</span>
    <span class="metric-pill">Free Model Scanner</span>
    <span class="metric-pill">Self-Grading Quiz</span>
    """, unsafe_allow_html=True)
with col_head_right:
    quiz_button_label = "Close Quiz" if st.session_state.show_quiz else "Launch Quiz"
    if st.button(quiz_button_label, use_container_width=True):
        st.session_state.show_quiz = not st.session_state.show_quiz
        st.rerun()

# Free Models Drawer
if st.session_state.show_scanner:
    with st.container():
        st.markdown("### Discovered Free Models")
        st.caption("Active zero-cost models scanned from open endpoints:")
        
        cols = st.columns(3)
        for i, m in enumerate(st.session_state.discovered_free_models[:9]):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="omni-card" style="padding: 0.9rem; margin-bottom: 0.6rem;">
                    <strong style="color: #65dbd0;">{m['name']}</strong><br/>
                    <code style="font-size: 0.75rem; color: #9bb3c7;">{m['id']}</code><br/>
                    <span style="font-size: 0.8rem; color: #94a3b8;">Context: {m['context_length']:,} tokens &bull; {m['provider']}</span>
                </div>
                """, unsafe_allow_html=True)
        st.divider()

# Quiz Drawer
if st.session_state.show_quiz:
    with st.container():
        render_interactive_quiz()
        st.divider()

def extract_artifact(text: str):
    mermaid_match = re.search(r"```mermaid\n(.*?)```", text, re.DOTALL)
    if mermaid_match:
        return {"type": "mermaid", "content": mermaid_match.group(1).strip()}
    code_match = re.search(r"```([a-zA-Z0-9]+)?\n(.*?)```", text, re.DOTALL)
    if code_match:
        lang = code_match.group(1) or "text"
        return {"type": "code", "lang": lang, "content": code_match.group(2).strip()}
    return None

# Workspace View
if is_battle:
    st.markdown("### Model Comparison Arena")
    st.caption("Submit a prompt to stream answers from both models in parallel:")
    
    battle_input = st.chat_input("Enter a prompt to compare both models...")
    
    for b_turn in st.session_state.battle_messages:
        st.markdown(f"**Prompt:** {b_turn['prompt']}")
        col_res_a, col_res_b = st.columns(2)
        with col_res_a:
            st.markdown(f"#### {b_turn['model_a_name']}")
            st.markdown(f"<span class='metric-pill'>Latency: {b_turn['latency_a']:.2f}s</span>", unsafe_allow_html=True)
            st.markdown(b_turn["response_a"])
        with col_res_b:
            st.markdown(f"#### {b_turn['model_b_name']}")
            st.markdown(f"<span class='metric-pill'>Latency: {b_turn['latency_b']:.2f}s</span>", unsafe_allow_html=True)
            st.markdown(b_turn["response_b"])
        st.divider()

    if battle_input:
        context_str = format_context_for_prompt(st.session_state.uploaded_files_data)
        history = [{"role": "user", "content": battle_input}]
        
        st.markdown(f"**Prompt:** {battle_input}")
        col_stream_a, col_stream_b = st.columns(2)
        
        model_a_display = AVAILABLE_MODELS.get(model_a_provider, {}).get("name", "Model A")
        model_b_display = selected_free_choice.split("(")[0].strip()
        
        with col_stream_a:
            st.markdown(f"#### {model_a_display}")
            holder_a = st.empty()
            text_a = ""
            t0_a = time.time()
            for chunk in stream_ai_response(model_a_provider, history, selected_persona_id, GEMINI_API_KEY, context_str):
                text_a += chunk
                holder_a.markdown(text_a + " ▌")
            holder_a.markdown(text_a)
            lat_a = time.time() - t0_a
            st.caption(f"Completed in {lat_a:.2f}s")
            
        with col_stream_b:
            st.markdown(f"#### {model_b_display}")
            holder_b = st.empty()
            text_b = ""
            t0_b = time.time()
            for chunk in stream_ai_response("nous", history, selected_persona_id, NOUS_API_KEY, context_str, model_name=selected_free_model_id):
                text_b += chunk
                holder_b.markdown(text_b + " ▌")
            holder_b.markdown(text_b)
            lat_b = time.time() - t0_b
            st.caption(f"Completed in {lat_b:.2f}s")
            
        st.session_state.battle_messages.append({
            "prompt": battle_input,
            "model_a_name": model_a_display,
            "model_b_name": model_b_display,
            "response_a": text_a,
            "response_b": text_b,
            "latency_a": lat_a,
            "latency_b": lat_b
        })
        
        st.markdown("##### Vote:")
        col_v1, col_v2, col_v3 = st.columns(3)
        with col_v1:
            if st.button("Model A was better"):
                st.session_state.battle_votes["Model A"] += 1
                st.success("Vote recorded.")
        with col_v2:
            if st.button("Model B was better"):
                st.session_state.battle_votes["Model B"] += 1
                st.success("Vote recorded.")
        with col_v3:
            if st.button("Equal / Tie"):
                st.session_state.battle_votes["Tie"] += 1
                st.info("Vote recorded.")
        st.rerun()

else:
    col_chat, col_canvas = st.columns([1.15, 0.85], gap="medium")

    # Artifact Canvas
    with col_canvas:
        st.markdown("### Artifact Canvas")
        st.caption("Extracted code blocks and system diagrams appear here:")
        
        artifact = st.session_state.active_artifact
        if artifact:
            if artifact["type"] == "mermaid":
                st.markdown("#### System Diagram (Interactive Visualizer)")
                # Interactive SVG rendering
                render_mermaid_svg(artifact["content"], height=320)
                st.download_button("Download Mermaid File", data=artifact["content"], file_name="diagram.mmd", use_container_width=True)
            elif artifact["type"] == "code":
                st.markdown(f"#### Code ({artifact.get('lang', 'text')})")
                st.code(artifact["content"], language=artifact.get("lang", "text"))
                
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    st.download_button("Download Code File", data=artifact["content"], file_name=f"artifact.{artifact.get('lang', 'txt')}", use_container_width=True)
                with col_c2:
                    if artifact.get("lang") in ["python", "py"]:
                        if st.button("Run Code", use_container_width=True):
                            res = execute_python_code(artifact["content"])
                            st.session_state.code_run_result = res
                            st.rerun()
                
                # Show Code Execution Result if active
                if st.session_state.code_run_result:
                    res = st.session_state.code_run_result
                    st.markdown("##### Execution Terminal Output:")
                    if res["success"]:
                        st.success("Process exited with code 0")
                        st.code(res["stdout"] if res["stdout"] else "[Process finished with no output]")
                    else:
                        st.error(f"Execution Error (Exit {res['returncode']}):")
                        st.code(res["stderr"])
        else:
            st.info("Generated code and system diagrams will automatically render here as you chat.")
            sample_mermaid = """flowchart TD
    Client[Web Client] --> API[FastAPI / Gemini]
    API --> Canvas[Artifact Canvas]
    API --> Quiz[Quiz Engine]"""
            render_mermaid_svg(sample_mermaid, height=220)

    # Chat Thread
    with col_chat:
        if not st.session_state.messages:
            st.markdown("#### Sample Prompts")
            chip1, chip2 = st.columns(2)
            with chip1:
                if st.button("Monolith vs Microservices Architecture", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Explain Microservices vs Modular Monolith with an architectural Mermaid diagram."})
                    st.rerun()
                if st.button("Explain Quantum Entanglement simply", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Explain Quantum Entanglement simply with analogies and check-in questions."})
                    st.rerun()
            with chip2:
                if st.button("Executive Project Briefing", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Provide an executive briefing and readiness matrix for this AI application."})
                    st.rerun()
                if st.button("Launch Interactive Quiz", use_container_width=True):
                    st.session_state.show_quiz = True
                    st.rerun()
            st.divider()

        for msg in st.session_state.messages:
            role = msg["role"]
            with st.chat_message(role):
                st.markdown(msg["content"])

        user_input = st.chat_input("Type your message here...")
        
        trigger_response = False
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            trigger_response = True
        elif st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            trigger_response = True

        if trigger_response:
            latest_user_msg = st.session_state.messages[-1]["content"]
            context_str = format_context_for_prompt(st.session_state.uploaded_files_data)
            
            with st.chat_message("assistant"):
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
                st.session_state.code_run_result = None
            st.rerun()
