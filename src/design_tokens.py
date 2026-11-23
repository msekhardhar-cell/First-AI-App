"""OmniChat - Advanced Figma AI Design System with 3D Floral Wallpaper.

Features deep obsidian glassmorphism, luminous ambient glows, and a subtle
3D floral background wallpaper providing tactile depth without layout distortion.
"""

import os
import base64

def _get_background_image_css() -> str:
    """Returns CSS background-image rule using the 3D floral wallpaper."""
    bg_path = os.path.join(os.path.dirname(__file__), "..", "assets", "bg_floral_3d.jpg")
    if os.path.exists(bg_path):
        try:
            with open(bg_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            return f"""
                linear-gradient(rgba(7, 9, 14, 0.82), rgba(7, 9, 14, 0.92)),
                url("data:image/jpeg;base64,{b64}")
            """
        except Exception:
            pass
    return """
        radial-gradient(1200px 500px at 50% -80px, rgba(99, 102, 241, 0.18), transparent 70%),
        radial-gradient(800px 400px at 80% 20%, rgba(6, 182, 212, 0.08), transparent 60%)
    """

def get_advanced_ai_css() -> str:
    """Constructs the complete CSS styling string."""
    bg_rule = _get_background_image_css()
    
    return f"""
<style>
/* --------------------------------------------------------------------------
   1. Deep Space Obsidian Canvas & 3D Floral Wallpaper
   -------------------------------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {{
    background-color: #07090E !important;
    background-image: {bg_rule} !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
    color: #F8FAFC !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    letter-spacing: -0.01em;
}}

[data-testid="stHeader"] {{
    background: rgba(7, 9, 14, 0.75) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
}}

[data-testid="stSidebar"] {{
    background-color: rgba(10, 13, 20, 0.85) !important;
    backdrop-filter: blur(24px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4) !important;
}}

[data-testid="stSidebar"] hr {{
    border-color: rgba(255, 255, 255, 0.06) !important;
}}

/* Custom Scrollbars */
::-webkit-scrollbar {{
    width: 6px;
    height: 6px;
}}
::-webkit-scrollbar-track {{
    background: transparent;
}}
::-webkit-scrollbar-thumb {{
    background: rgba(255, 255, 255, 0.12);
    border-radius: 9999px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: rgba(99, 102, 241, 0.5);
}}

/* --------------------------------------------------------------------------
   2. Glassmorphic Cards & Elevated Panels
   -------------------------------------------------------------------------- */
.omni-card {{
    background: rgba(16, 20, 32, 0.65) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 1.25rem !important;
    margin-bottom: 1rem !important;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}
.omni-card:hover {{
    border-color: rgba(99, 102, 241, 0.4) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px -4px rgba(99, 102, 241, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
}}

/* --------------------------------------------------------------------------
   3. Modern Clean Header (Zero Layout Distortion)
   -------------------------------------------------------------------------- */
.omni-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 0 1.25rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 1.5rem;
}}
.omni-title {{
    font-size: 28px !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #FFFFFF 20%, #E2E8F0 50%, #818CF8 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    letter-spacing: -0.03em !important;
    margin: 0 !important;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}
.omni-studio-tag {{
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #818CF8 !important;
    border: 1px solid rgba(99, 102, 241, 0.35) !important;
    padding: 2px 8px !important;
    border-radius: 9999px !important;
    vertical-align: middle !important;
    background: rgba(99, 102, 241, 0.1) !important;
}}
.omni-subtitle {{
    margin: 0.25rem 0 0 0 !important;
    color: #94A3B8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}}
.omni-header-badges {{
    display: flex;
    gap: 0.6rem;
    align-items: center;
}}

/* --------------------------------------------------------------------------
   4. Luminous Badges & Indicators
   -------------------------------------------------------------------------- */
.omni-badge {{
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    background: rgba(99, 102, 241, 0.12) !important;
    border: 1px solid rgba(99, 102, 241, 0.3) !important;
    color: #C7D2FE !important;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    box-shadow: 0 2px 10px rgba(99, 102, 241, 0.15) !important;
}}
.omni-badge.sandbox {{
    background: rgba(16, 185, 129, 0.12) !important;
    border-color: rgba(16, 185, 129, 0.35) !important;
    color: #6EE7B7 !important;
}}
.omni-badge.persona-badge {{
    background: rgba(255, 255, 255, 0.05) !important;
    border-color: rgba(255, 255, 255, 0.1) !important;
    color: #E2E8F0 !important;
}}
.ai-pulse-dot {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background-color: #10B981;
    box-shadow: 0 0 8px #10B981;
    display: inline-block;
    animation: beaconPulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}}
@keyframes beaconPulse {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50% {{ opacity: 0.4; transform: scale(0.85); }}
}}

/* Metric Pills */
.metric-pill {{
    display: inline-flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 9999px;
    padding: 0.3rem 0.75rem;
    font-size: 11px;
    font-weight: 600;
    color: #94A3B8;
    margin-right: 0.5rem;
    backdrop-filter: blur(8px);
    transition: all 0.2s ease;
}}
.metric-pill:hover {{
    border-color: rgba(99, 102, 241, 0.4);
    color: #F8FAFC;
    background: rgba(99, 102, 241, 0.1);
}}
.metric-pill.latency {{
    background: rgba(6, 182, 212, 0.12);
    border-color: rgba(6, 182, 212, 0.3);
    color: #67E8F9;
}}

/* --------------------------------------------------------------------------
   5. Interactive Buttons & Glass Chips
   -------------------------------------------------------------------------- */
.stButton > button {{
    background: linear-gradient(180deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
    color: #F1F5F9 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 0.55rem 1rem !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}}
.stButton > button:hover {{
    border-color: rgba(99, 102, 241, 0.5) !important;
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.3) 0%, rgba(6, 182, 212, 0.3) 100%) !important;
    box-shadow: 0 0 16px rgba(99, 102, 241, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
}}
.stButton > button:active {{
    transform: translateY(0);
}}

/* --------------------------------------------------------------------------
   6. Modern Floating Chat Input & Bubbles
   -------------------------------------------------------------------------- */
[data-testid="stChatInput"] {{
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    background: rgba(15, 23, 42, 0.8) !important;
    backdrop-filter: blur(20px) !important;
    color: #F8FAFC !important;
    box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.6) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}}
[data-testid="stChatInput"]:focus-within {{
    border-color: #6366F1 !important;
    box-shadow: 0 0 24px rgba(99, 102, 241, 0.35) !important;
}}

[data-testid="stChatMessage"] {{
    background: rgba(15, 23, 42, 0.65) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 16px !important;
    padding: 1rem 1.25rem !important;
    margin-bottom: 0.85rem !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25) !important;
}}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {{
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(30, 41, 59, 0.45) 100%) !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
}}

/* --------------------------------------------------------------------------
   7. Form Inputs & Selectboxes
   -------------------------------------------------------------------------- */
[data-testid="stSelectbox"] > div > div {{
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: #F8FAFC !important;
}}
[data-testid="stTextInput"] input {{
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: #F8FAFC !important;
}}

/* --------------------------------------------------------------------------
   8. Studio Artifact Canvas Styling
   -------------------------------------------------------------------------- */
.artifact-studio-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.6rem 0.85rem;
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px 14px 0 0;
    border-bottom: none;
    font-size: 12px;
    font-weight: 600;
    color: #94A3B8;
}}
.artifact-studio-window-dots {{
    display: flex;
    gap: 6px;
    align-items: center;
}}
.dot-red {{ width: 10px; height: 10px; border-radius: 50%; background: #EF4444; }}
.dot-yellow {{ width: 10px; height: 10px; border-radius: 50%; background: #F59E0B; }}
.dot-green {{ width: 10px; height: 10px; border-radius: 50%; background: #10B981; }}

.terminal-box {{
    background: #050608 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 0 0 14px 14px !important;
    padding: 0.85rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    color: #E2E8F0 !important;
}}
</style>
"""

def inject_design_tokens():
    """Injects the advanced AI design tokens and CSS into the application."""
    import streamlit as st
    st.markdown(get_advanced_ai_css(), unsafe_allow_html=True)
