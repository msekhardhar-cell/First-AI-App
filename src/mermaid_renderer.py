"""OmniChat - Mermaid HTML/SVG interactive renderer component."""
import streamlit.components.v1 as components

def render_mermaid_svg(mermaid_code: str, height: int = 380):
    """Renders a Mermaid diagram as an interactive, SVG diagram matching Figma dark tokens."""
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
      <style>
        body {{
          background-color: #111a25;
          margin: 0;
          padding: 10px;
          display: flex;
          justify-content: center;
          align-items: center;
          color: #f5fafd;
          font-family: 'Inter', sans-serif;
        }}
        .mermaid {{
          width: 100%;
          text-align: center;
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
            background: '#111a25',
            primaryColor: '#29434b',
            primaryTextColor: '#f5fafd',
            primaryBorderColor: '#65dbd0',
            lineColor: '#65dbd0',
            secondaryColor: '#1d2d3c',
            tertiaryColor: '#111a25'
          }}
        }});
      </script>
    </body>
    </html>
    """
    components.html(html_code, height=height, scrolling=True)
