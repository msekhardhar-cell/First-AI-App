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
from src.floral_imprints import (
    CELESTIAL_LOTUS_SVG, 
    GEOMETRIC_ROSETTE_SVG, 
    BOTANICAL_FLOURISH_SVG, 
    ALL_3D_IMPRINTS
)

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
if "show_imprints" not in st.session_state:
    st.session_state.show_imprints = False
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
        elif selected_provider.startswith("groq"):
            api_key = st.text_input("Groq API Key:", value=GROQ_API_KEY, type="password")
            if not api_key:
                st.info("Running in Sandbox Mode.")
        else:
            st.success("Sandbox active: evaluate without an API key.")
    else:
        st.markdown("### Battle Setup")
        battle_options = list(AVAILABLE_MODELS.keys())
        model_a_provider = st.selectbox(
            "Model A:",
            battle_options,
            format_func=lambda k: AVAILABLE_MODELS[k]["name"],
            index=0
        )
        
        free_model_names = [f"Free: {m['name']} ({m['id']})" for m in st.session_state.discovered_free_models]
        model_b_choices = ["groq_gpt", "groq_qwen", "gemini"] + free_model_names
        selected_free_choice = st.selectbox(
            "Model B:",
            model_b_choices,
            format_func=lambda k: AVAILABLE_MODELS[k]["name"] if k in AVAILABLE_MODELS else k,
            index=0
        )
        selected_provider = model_a_provider
        api_key = GROQ_API_KEY if model_a_provider.startswith("groq") else GEMINI_API_KEY

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
header_mode_badge = "⚔️ Battle Arena" if is_battle else f"⚡ {AVAILABLE_MODELS[selected_provider]['badge']}"
is_sandbox_active = selected_provider == 'sandbox' or (selected_provider == 'gemini' and not api_key)
badge_class = 'sandbox' if is_sandbox_active else ''

st.markdown(f"""
<div class="omni-header">
    <div style="display: flex; align-items: center; gap: 1rem;">
        <div style="width: 48px; height: 48px; filter: drop-shadow(0 0 10px rgba(99, 102, 241, 0.4));">
            {CELESTIAL_LOTUS_SVG}
        </div>
        <div>
            <h1 class="omni-title">
                <span style="background: linear-gradient(135deg, #6366F1, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">✦</span>
                OmniChat
                <span style="font-size: 11px; font-weight: 700; color: #818CF8; border: 1px solid rgba(99, 102, 241, 0.35); padding: 2px 8px; border-radius: 9999px; vertical-align: middle; background: rgba(99, 102, 241, 0.1);">AI STUDIO</span>
            </h1>
            <p style="margin: 0.25rem 0 0 0; color: #94A3B8; font-size: 0.85rem; font-weight: 500;">
                Next-Gen Multi-Model Battle Arena, Live Artifact Canvas & Free Open Inference Scanner
            </p>
        </div>
    </div>
    <div style="display: flex; gap: 0.6rem; align-items: center;">
        <span class="omni-badge {badge_class}">
            <span class="ai-pulse-dot"></span>
            {header_mode_badge}
        </span>
        <span class="omni-badge" style="background: rgba(255, 255, 255, 0.05); border-color: rgba(255, 255, 255, 0.1); color: #E2E8F0;">
            👤 {current_persona['name']}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Action Row
col_head_left, col_btn_imp, col_btn_quiz = st.columns([2.4, 1.1, 1.1])
with col_head_left:
    st.markdown("""
    <span class="metric-pill">🌸 3D Floral Imprints</span>
    <span class="metric-pill">✨ Figma AI Dark System</span>
    <span class="metric-pill">⚡ Dual Stream LPUs</span>
    <span class="metric-pill">📐 Live SVG Canvas</span>
    """, unsafe_allow_html=True)
with col_btn_imp:
    imprint_button_label = "Hide Imprints" if st.session_state.show_imprints else "🌸 3D Imprints"
    if st.button(imprint_button_label, use_container_width=True):
        st.session_state.show_imprints = not st.session_state.show_imprints
        st.rerun()
with col_btn_quiz:
    quiz_button_label = "Close Quiz" if st.session_state.show_quiz else "🎯 Launch Quiz"
    if st.button(quiz_button_label, use_container_width=True):
        st.session_state.show_quiz = not st.session_state.show_quiz
        st.rerun()

# 3D Floral Imprint Showcase Drawer
if st.session_state.show_imprints:
    with st.container():
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem;">
            <h3 style="margin: 0; color: #F8FAFC; font-size: 1.25rem;">🌸 Sculptural 3D Flowery Imprint Showcase</h3>
            <span class="imprint-badge-3d">
                <span class="ai-pulse-dot"></span> 3 SCULPTED 3D EMBLEMS ACTIVE
            </span>
        </div>
        """, unsafe_allow_html=True)
        st.caption("Tactile 3D debossed and embossed floral imprints with specular highlights and dimensional bevels:")
        
        col_imp1, col_imp2, col_imp3 = st.columns(3)
        for col, imp in zip([col_imp1, col_imp2, col_imp3], ALL_3D_IMPRINTS):
            with col:
                st.markdown(f"""
                <div class="imprint-card-3d" style="text-align: center; border-top: 3px solid {imp['accent']};">
                    <span style="font-size: 10px; font-weight: 700; color: {imp['accent']}; letter-spacing: 0.05em; text-transform: uppercase;">{imp['tag']}</span>
                    <h4 style="margin: 0.35rem 0 0.75rem 0; color: #F8FAFC; font-size: 1.05rem;">{imp['name']}</h4>
                    <div style="width: 140px; height: 140px; margin: 0 auto 0.75rem auto;">
                        {imp['svg']}
                    </div>
                    <p style="font-size: 0.8rem; color: #94A3B8; margin: 0; line-height: 1.4;">{imp['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
        st.divider()

# Free Models Drawer
if st.session_state.show_scanner:
    with st.container():
        st.markdown("### Discovered Free Models")
        st.caption("Active zero-cost models scanned from open endpoints:")
        
        cols = st.columns(3)
        for i, m in enumerate(st.session_state.discovered_free_models[:9]):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="omni-card" style="padding: 1rem; margin-bottom: 0.75rem; border-left: 3px solid #818CF8;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.35rem;">
                        <strong style="color: #F8FAFC; font-size: 0.95rem;">{m['name']}</strong>
                        <span style="font-size: 10px; background: rgba(99, 102, 241, 0.15); color: #818CF8; border: 1px solid rgba(99, 102, 241, 0.3); padding: 1px 6px; border-radius: 9999px; font-weight: 700;">FREE</span>
                    </div>
                    <code style="font-size: 0.75rem; color: #94A3B8; background: rgba(0, 0, 0, 0.35); padding: 2px 6px; border-radius: 6px; display: inline-block; margin-bottom: 0.4rem;">{m['id']}</code><br/>
                    <span style="font-size: 0.75rem; color: #64748B;">Context: <span style="color: #38BDF8; font-weight: 600;">{m['context_length']:,}</span> tokens &bull; {m['provider']}</span>
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
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; padding: 0.85rem 1.25rem; background: rgba(16, 20, 32, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; margin-bottom: 1.25rem;">
        <div style="display: flex; align-items: center; gap: 0.85rem;">
            <div style="width: 38px; height: 38px; filter: drop-shadow(0 0 8px rgba(244, 63, 94, 0.4));">
                {BOTANICAL_FLOURISH_SVG}
            </div>
            <div>
                <h3 style="margin: 0; color: #F8FAFC; font-size: 1.15rem;">⚔️ Dual-Model Battle Arena</h3>
                <p style="margin: 0; color: #94A3B8; font-size: 0.8rem;">Parallel token streaming with dimensional 3D evaluation</p>
            </div>
        </div>
        <span class="imprint-badge-3d" style="background: rgba(244, 63, 94, 0.12); border-color: rgba(244, 63, 94, 0.3); color: #FDA4AF;">
            <span class="ai-pulse-dot" style="background-color: #F43F5E; box-shadow: 0 0 8px #F43F5E;"></span> 3D BOTANICAL CREST
        </span>
    </div>
    """, unsafe_allow_html=True)
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
        key_a = GROQ_API_KEY if model_a_provider.startswith("groq") else (GEMINI_API_KEY if model_a_provider == "gemini" else NOUS_API_KEY)
        model_a_target = AVAILABLE_MODELS.get(model_a_provider, {}).get("model", "")
        
        if selected_free_choice in AVAILABLE_MODELS:
            model_b_display = AVAILABLE_MODELS[selected_free_choice]["name"]
            provider_b = selected_free_choice
            model_b_target = AVAILABLE_MODELS[selected_free_choice]["model"]
            key_b = GROQ_API_KEY if selected_free_choice.startswith("groq") else (GEMINI_API_KEY if selected_free_choice == "gemini" else NOUS_API_KEY)
        else:
            model_b_display = selected_free_choice.split("(")[0].replace("Free:", "").strip()
            provider_b = "nous"
            model_b_target = selected_free_choice.split("(")[-1].replace(")", "").strip()
            key_b = NOUS_API_KEY
        
        with col_stream_a:
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 0.5rem; margin-bottom: 0.75rem; border-bottom: 1px solid rgba(129, 140, 248, 0.25);">
                <h4 style="margin: 0; color: #818CF8; font-size: 1.05rem;">⚡ {model_a_display}</h4>
                <span class='metric-pill latency'>Inference Stream</span>
            </div>
            """, unsafe_allow_html=True)
            holder_a = st.empty()
            text_a = ""
            t0_a = time.time()
            for chunk in stream_ai_response(model_a_provider, history, selected_persona_id, key_a, context_str, model_name=model_a_target):
                text_a += chunk
                holder_a.markdown(text_a + " ▌")
            holder_a.markdown(text_a)
            lat_a = time.time() - t0_a
            st.caption(f"⚡ Completed in {lat_a:.2f}s")
            
        with col_stream_b:
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 0.5rem; margin-bottom: 0.75rem; border-bottom: 1px solid rgba(34, 211, 238, 0.25);">
                <h4 style="margin: 0; color: #22D3EE; font-size: 1.05rem;">🚀 {model_b_display}</h4>
                <span class='metric-pill latency' style="border-color: rgba(6, 182, 212, 0.35); color: #67E8F9;">Inference Stream</span>
            </div>
            """, unsafe_allow_html=True)
            holder_b = st.empty()
            text_b = ""
            t0_b = time.time()
            for chunk in stream_ai_response(provider_b, history, selected_persona_id, key_b, context_str, model_name=model_b_target):
                text_b += chunk
                holder_b.markdown(text_b + " ▌")
            holder_b.markdown(text_b)
            lat_b = time.time() - t0_b
            st.caption(f"🚀 Completed in {lat_b:.2f}s")
            
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
        st.markdown("""
        <div class="artifact-studio-header">
            <div class="artifact-studio-window-dots">
                <span class="dot-red"></span>
                <span class="dot-yellow"></span>
                <span class="dot-green"></span>
            </div>
            <span>STUDIO ARTIFACT CANVAS</span>
            <span style="font-size: 10px; color: #818CF8; background: rgba(99, 102, 241, 0.15); padding: 1px 6px; border-radius: 9999px;">LIVE</span>
        </div>
        """, unsafe_allow_html=True)
        
        artifact = st.session_state.active_artifact
        if artifact:
            if artifact["type"] == "mermaid":
                st.markdown("<p style='font-size: 0.85rem; color: #94A3B8; margin: 0.5rem 0;'>📐 <strong>Interactive System Diagram</strong></p>", unsafe_allow_html=True)
                render_mermaid_svg(artifact["content"], height=320)
                st.download_button("Download Mermaid (.mmd)", data=artifact["content"], file_name="diagram.mmd", use_container_width=True)
            elif artifact["type"] == "code":
                st.markdown(f"<p style='font-size: 0.85rem; color: #94A3B8; margin: 0.5rem 0;'>💻 <strong>Executable Code ({artifact.get('lang', 'text')})</strong></p>", unsafe_allow_html=True)
                st.code(artifact["content"], language=artifact.get("lang", "text"))
                
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    st.download_button("Download Code File", data=artifact["content"], file_name=f"artifact.{artifact.get('lang', 'txt')}", use_container_width=True)
                with col_c2:
                    if artifact.get("lang") in ["python", "py"]:
                        if st.button("▶ Run Code", use_container_width=True):
                            res = execute_python_code(artifact["content"])
                            st.session_state.code_run_result = res
                            st.rerun()
                
                # Show Code Execution Result if active
                if st.session_state.code_run_result:
                    res = st.session_state.code_run_result
                    exit_color = "#10B981" if res["success"] else "#EF4444"
                    status_label = "EXIT 0 (SUCCESS)" if res["success"] else f"EXIT {res['returncode']} (ERROR)"
                    terminal_text = res["stdout"] if res["stdout"] else (res["stderr"] if res["stderr"] else "[Process finished with no output]")
                    st.markdown(f"""
                    <div class="artifact-studio-header" style="margin-top: 1rem;">
                        <div class="artifact-studio-window-dots">
                            <span class="dot-red"></span>
                            <span class="dot-yellow"></span>
                            <span class="dot-green"></span>
                        </div>
                        <span>TERMINAL OUTPUT</span>
                        <span style="font-size: 10px; color: {exit_color}; font-weight: 700;">{status_label}</span>
                    </div>
                    <div class="terminal-box">
                        <pre style="margin: 0; white-space: pre-wrap; color: {'#34D399' if res['success'] else '#F87171'};">{terminal_text}</pre>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="text-align: center; padding: 1.25rem 0.5rem; background: rgba(16, 20, 32, 0.4); border: 1px dashed rgba(255, 255, 255, 0.1); border-radius: 16px; margin-bottom: 1rem;">
                <div style="width: 120px; height: 120px; margin: 0 auto 0.75rem auto; filter: drop-shadow(0 4px 14px rgba(6, 182, 212, 0.35));">
                    {GEOMETRIC_ROSETTE_SVG}
                </div>
                <strong style="color: #F8FAFC; font-size: 0.95rem;">3D Guilloché Floral Rosette</strong>
                <p style="color: #94A3B8; font-size: 0.8rem; margin: 0.25rem 0 0 0;">Interactive system diagrams and executable code will render here live as you chat.</p>
            </div>
            """, unsafe_allow_html=True)
            sample_mermaid = """flowchart TD
    Client[Web Client] --> API[FastAPI / Gemini]
    API --> Canvas[Artifact Canvas]
    API --> Quiz[Quiz Engine]"""
            render_mermaid_svg(sample_mermaid, height=180)

    # Chat Thread
    with col_chat:
        if not st.session_state.messages:
            st.markdown("#### ✨ Suggested Prompts")
            chip1, chip2 = st.columns(2)
            with chip1:
                if st.button("⚡ Microservices vs Monolith Architecture", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Explain Microservices vs Modular Monolith with an architectural Mermaid diagram."})
                    st.rerun()
                if st.button("⚛️ Explain Quantum Entanglement simply", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Explain Quantum Entanglement simply with analogies and check-in questions."})
                    st.rerun()
            with chip2:
                if st.button("📊 Executive Project Briefing", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Provide an executive briefing and readiness matrix for this AI application."})
                    st.rerun()
                if st.button("🎯 Launch Adaptive Study Quiz", use_container_width=True):
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
                
                model_target = AVAILABLE_MODELS.get(selected_provider, {}).get("model", "")
                stream = stream_ai_response(
                    provider=selected_provider,
                    messages=st.session_state.messages,
                    persona_id=selected_persona_id,
                    api_key=api_key,
                    file_context=context_str,
                    model_name=model_target
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
