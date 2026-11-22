"""OmniChat - Figma Design Tokens extracted from Figma file TKiZXwjkWdkponF1zNsfli."""

# Tokens extracted via figctl from Figma Node 5:186 (DARK High Contrast) & 52:164 (Theme C)
FIGMA_DESIGN_TOKENS = {
    "colors": {
        # Core Slate Dark Theme (Figma Node 5:186)
        "bg_root": "#111a25",          # Root background
        "bg_surface": "#1d2d3c",       # Card container fill
        "bg_action": "#29434b",        # Button & action fill
        "border_accent": "#65dbd0",    # Cyan / teal 1px stroke
        "text_primary": "#f5fafd",     # White frost text
        "text_accent": "#65dbd0",      # Cyan accent text
        "text_secondary": "#9bb3c7",   # Muted body slate
        "text_muted": "#626d77",       # Secondary label
        # Theme C Accents (Figma Node 52:164)
        "accent_sage": "#85ad8b",
        "accent_amber": "#e5b679",
        "accent_crimson": "#b73527",
    },
    "typography": {
        "font_family": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
        "heading_size": "24px",
        "heading_weight": "700",
        "card_title_size": "17px",
        "card_title_weight": "700",
        "body_size": "14px",
        "body_weight": "400",
        "badge_size": "11px",
        "badge_weight": "700"
    },
    "geometry": {
        "frame_radius": "25px",
        "card_radius": "17px",
        "pill_radius": "14px",
        "button_radius": "17px"
    }
}

FIGMA_CSS = """
<style>
/* Root Container Styling (Figma Node 5:186) */
[data-testid="stAppViewContainer"] {
    background-color: #111a25 !important;
    color: #f5fafd !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
}

[data-testid="stHeader"] {
    background: rgba(17, 26, 37, 0.9) !important;
    backdrop-filter: blur(12px) !important;
    border-bottom: 1px solid rgba(101, 219, 208, 0.2) !important;
}

[data-testid="stSidebar"] {
    background-color: #0c141d !important;
    border-right: 1px solid rgba(101, 219, 208, 0.15) !important;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #111a25;
}
::-webkit-scrollbar-thumb {
    background: #1d2d3c;
    border-radius: 9999px;
}
::-webkit-scrollbar-thumb:hover {
    background: #65dbd0;
}

/* Figma Card Specification (box: w 296px, fills: #1d2d3c, radius: 17px) */
.omni-card {
    background: #1d2d3c !important;
    border: 1px solid rgba(101, 219, 208, 0.2) !important;
    border-radius: 17px !important;
    padding: 1.25rem !important;
    margin-bottom: 1rem !important;
    box-sizing: border-box !important;
    transition: border-color 0.2s ease, transform 0.2s ease;
}
.omni-card:hover {
    border-color: #65dbd0 !important;
    transform: translateY(-1px);
}

/* Figma Header Banner */
.omni-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 0 1.25rem 0;
    border-bottom: 1px solid rgba(101, 219, 208, 0.15);
    margin-bottom: 1.5rem;
}
.omni-title {
    font-size: 24px !important;
    font-weight: 700 !important;
    color: #f5fafd !important;
    letter-spacing: -0.02em;
    margin: 0;
}
.omni-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: #29434b !important;
    border: 1px solid #65dbd0 !important;
    color: #65dbd0 !important;
    padding: 0.3rem 0.85rem;
    border-radius: 14px !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
}
.omni-badge.sandbox {
    background: rgba(133, 173, 139, 0.15) !important;
    border-color: #85ad8b !important;
    color: #85ad8b !important;
}

/* Metric Pills */
.metric-pill {
    display: inline-flex;
    align-items: center;
    background: #1d2d3c;
    border: 1px solid rgba(101, 219, 208, 0.25);
    border-radius: 14px;
    padding: 0.25rem 0.65rem;
    font-size: 12px;
    font-weight: 600;
    color: #65dbd0;
    margin-right: 0.4rem;
}

/* Action Buttons (Figma Node 5:196 Action, fills: #29434b, radius: 17px) */
.stButton > button {
    background-color: #29434b !important;
    color: #f5fafd !important;
    border: 1px solid rgba(101, 219, 208, 0.3) !important;
    border-radius: 17px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    border-color: #65dbd0 !important;
    background-color: #355762 !important;
    box-shadow: 0 0 12px rgba(101, 219, 208, 0.2) !important;
}

/* Chat Input Styling */
[data-testid="stChatInput"] {
    border-radius: 17px !important;
    border: 1px solid rgba(101, 219, 208, 0.3) !important;
    background-color: #1d2d3c !important;
    color: #f5fafd !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #65dbd0 !important;
    box-shadow: 0 0 12px rgba(101, 219, 208, 0.25) !important;
}

/* Chat Message Bubbles */
[data-testid="stChatMessage"] {
    background: #1d2d3c !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 17px !important;
    padding: 1rem !important;
    margin-bottom: 0.75rem !important;
}
</style>
"""

def inject_design_tokens():
    """Injects the verified Figma CSS tokens into the application."""
    import streamlit as st
    st.markdown(FIGMA_CSS, unsafe_allow_html=True)
