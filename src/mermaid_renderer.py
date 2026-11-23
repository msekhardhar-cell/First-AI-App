"""OmniChat - Mermaid HTML/SVG interactive renderer component."""
import streamlit.components.v1 as components

def render_mermaid_svg(mermaid_code: str, height: int = 380):
    """Renders a Mermaid diagram as an interactive SVG matching the advanced AI theme."""
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
      <style>
        body {{
          background: rgba(11, 14, 22, 0.7);
          border-radius: 14px;
          border: 1px solid rgba(255, 255, 255, 0.08);
          margin: 0;
          padding: 16px;
          display: flex;
          justify-content: center;
          align-items: center;
          color: #F8FAFC;
          font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        }}
        .mermaid {{
          width: 100%;
          text-align: center;
        }}
        .mermaid svg {{
          filter: drop-shadow(0 0 12px rgba(99, 102, 241, 0.15));
        }}
      </style>
    </head>
    <body>
      <div class="mermaid">
        {mermaid_code}
      </div>
      <script>
        mermaid.initialize({{
          startOnLoad: true,
          theme: 'dark',
          themeVariables: {{
            darkMode: true,
            background: 'transparent',
            primaryColor: '#1E1B4B',
            primaryTextColor: '#F8FAFC',
            primaryBorderColor: '#6366F1',
            lineColor: '#38BDF8',
            secondaryColor: '#0F172A',
            tertiaryColor: '#020617',
            edgeLabelBackground: '#0F172A',
            nodeBorder: '#818CF8'
          }}
        }});
      </script>
    </body>
    </html>
    """
    components.html(html_code, height=height, scrolling=True)
