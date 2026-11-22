"""OmniChat AI - Figma Design System Tokens & CSS generator."""

# Figma Design Tokens Specification (Obsidian Dark System)
DESIGN_TOKENS = {
    "colors": {
        "bg_main": "#090d16",
        "bg_surface": "#111726",
        "bg_elevated": "#172033",
        "bg_glass": "rgba(23, 32, 51, 0.75)",
        "border_subtle": "rgba(255, 255, 255, 0.08)",
        "border_focus": "rgba(139, 92, 246, 0.4)",
        "accent_primary": "#8b5cf6",       # Electric Violet
        "accent_secondary": "#06b6d4",     # Cyan
        "accent_success": "#10b981",       # Emerald
        "accent_warning": "#f59e0b",       # Amber
        "text_primary": "#f8fafc",
        "text_secondary": "#94a3b8",
        "text_muted": "#64748b",
        "gradient_brand": "linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%)",
        "gradient_card": "linear-gradient(180deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0) 100%)",
    },
    "radii": {
        "sm": "6px",
        "md": "12px",
        "lg": "16px",
        "full": "9999px"
    },
    "shadows": {
        "card": "0 8px 30px rgba(0, 0, 0, 0.4)",
        "glow": "0 0 25px rgba(139, 92, 246, 0.25)"
    }
}

CUSTOM_CSS = """
<style>
/* Base Theme Overrides */
[data-testid="stAppViewContainer"] {
    background-color: #090d16;
    color: #f8fafc;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(9, 13, 22, 0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

[data-testid="stSidebar"] {
    background-color: #0c111d !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #090d16;
}
::-webkit-scrollbar-thumb {
    background: #1e293b;
    border-radius: 9999px;
}
::-webkit-scrollbar-thumb:hover {
    background: #8b5cf6;
}

/* Glassmorphism Cards */
.omni-card {
    background: rgba(23, 32, 51, 0.7);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.35);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.omni-card:hover {
    border-color: rgba(139, 92, 246, 0.35);
}

/* Header Banner */
.omni-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 0 1.25rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    margin-bottom: 1.5rem;
}
.omni-title {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #f8fafc 0%, #cbd5e1 50%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}
.omni-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(139, 92, 246, 0.15);
    border: 1px solid rgba(139, 92, 246, 0.3);
    color: #c4b5fd;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
}
.omni-badge.sandbox {
    background: rgba(16, 185, 129, 0.15);
    border-color: rgba(16, 185, 129, 0.35);
    color: #6ee7b7;
}

/* Prompt Starter Chip */
.prompt-chip {
    background: rgba(23, 32, 51, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #e2e8f0;
    border-radius: 12px;
    padding: 0.85rem 1rem;
    text-align: left;
    cursor: pointer;
    transition: all 0.2s ease;
    height: 100%;
}
.prompt-chip:hover {
    background: rgba(139, 92, 246, 0.12);
    border-color: #8b5cf6;
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.2);
}

/* Quiz Card Styling */
.quiz-box {
    background: rgba(17, 24, 39, 0.9);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}
.quiz-option {
    padding: 0.75rem 1rem;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.2s;
}
.quiz-option:hover {
    background: rgba(255, 255, 255, 0.05);
    border-color: rgba(255, 255, 255, 0.2);
}

/* Chat Input Styling */
[data-testid="stChatInput"] {
    border-radius: 16px !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    background-color: #111726 !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.3) !important;
}

/* Metric Pill */
.metric-pill {
    display: inline-flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 0.2rem 0.5rem;
    font-size: 0.75rem;
    color: #94a3b8;
    margin-right: 0.4rem;
}
</style>
"""

def inject_design_tokens():
    """Injects custom CSS design tokens into the Streamlit app."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
