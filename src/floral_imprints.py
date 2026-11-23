"""OmniChat - 3D Flowery Imprint Design System.

Sculptural, dimensional floral imprint designs featuring tactile 3D debossing,
specular surface highlights, and layered botanical bevels:
1. 3D Celestial Lotus Bloom: Multi-layered sacred geometry bloom with 3D bevels
2. 3D Guilloché Floral Rosette: Precision-carved 12-lobed floral matrix engraving
3. 3D Botanical Acanthus Crest: Dimensional organic vine and blossom filigree
"""

import urllib.parse

# 1. 3D Celestial Lotus Bloom (Sculptural Sacred Geometry)
CELESTIAL_LOTUS_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 280" fill="none">
  <defs>
    <!-- 3D Surface Light Gradients -->
    <linearGradient id="lotus3DGrad" x1="15%" y1="10%" x2="85%" y2="90%">
      <stop offset="0%" stop-color="#E0E7FF" stop-opacity="0.95"/>
      <stop offset="30%" stop-color="#818CF8" stop-opacity="0.8"/>
      <stop offset="70%" stop-color="#4F46E5" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#06B6D4" stop-opacity="0.9"/>
    </linearGradient>
    
    <linearGradient id="petalBevelLight" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.4"/>
      <stop offset="50%" stop-color="#818CF8" stop-opacity="0.1"/>
      <stop offset="100%" stop-color="#000000" stop-opacity="0.5"/>
    </linearGradient>

    <!-- 3D Dimensional Bevel & Drop Shadow -->
    <filter id="lotus3DDepth" x="-25%" y="-25%" width="150%" height="150%">
      <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#000000" flood-opacity="0.7"/>
      <feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="#6366F1" flood-opacity="0.35"/>
      <feDropShadow dx="-1" dy="-1" stdDeviation="1.5" flood-color="#FFFFFF" flood-opacity="0.4"/>
    </filter>
  </defs>

  <g filter="url(#lotus3DDepth)">
    <!-- Outer Concentric Imprint Rings with 3D Depth -->
    <circle cx="140" cy="140" r="130" stroke="url(#lotus3DGrad)" stroke-width="0.8" stroke-dasharray="5,3" opacity="0.4"/>
    <circle cx="140" cy="140" r="116" stroke="url(#lotus3DGrad)" stroke-width="1.2" opacity="0.6"/>
    <circle cx="140" cy="140" r="88" stroke="url(#lotus3DGrad)" stroke-width="1" opacity="0.7"/>
    <circle cx="140" cy="140" r="44" stroke="url(#lotus3DGrad)" stroke-width="1.5" opacity="0.85"/>
    
    <!-- Central 3D Core Pearl -->
    <circle cx="140" cy="140" r="16" fill="url(#lotus3DGrad)" stroke="#FFFFFF" stroke-width="0.75" opacity="0.9"/>
    <circle cx="137" cy="137" r="4" fill="#FFFFFF" opacity="0.85"/>

    <!-- 8 Primary 3D Sculpted Petals -->
    <!-- North -->
    <path d="M140 15 C170 65 170 95 140 125 C110 95 110 65 140 15 Z" 
          fill="url(#petalBevelLight)" stroke="url(#lotus3DGrad)" stroke-width="1.6"/>
    <path d="M140 22 C140 70 140 100 140 125" stroke="#FFFFFF" stroke-width="0.7" opacity="0.5"/>
    
    <!-- South -->
    <path d="M140 265 C170 215 170 185 140 155 C110 185 110 215 140 265 Z" 
          fill="url(#petalBevelLight)" stroke="url(#lotus3DGrad)" stroke-width="1.6"/>
    <path d="M140 258 C140 210 140 180 140 155" stroke="#FFFFFF" stroke-width="0.7" opacity="0.5"/>
    
    <!-- West -->
    <path d="M15 140 C65 170 95 170 125 140 C95 110 65 110 15 140 Z" 
          fill="url(#petalBevelLight)" stroke="url(#lotus3DGrad)" stroke-width="1.6"/>
    <path d="M22 140 C70 140 100 140 125 140" stroke="#FFFFFF" stroke-width="0.7" opacity="0.5"/>
    
    <!-- East -->
    <path d="M265 140 C215 170 185 170 155 140 C185 110 215 110 265 140 Z" 
          fill="url(#petalBevelLight)" stroke="url(#lotus3DGrad)" stroke-width="1.6"/>
    <path d="M258 140 C210 140 180 140 155 140" stroke="#FFFFFF" stroke-width="0.7" opacity="0.5"/>

    <!-- Diagonal 3D Intermediate Petals -->
    <path d="M52 52 C95 85 114 104 140 140 C104 114 85 95 52 52 Z" 
          fill="url(#petalBevelLight)" stroke="url(#lotus3DGrad)" stroke-width="1.3"/>
    <path d="M228 228 C185 195 166 176 140 140 C176 166 195 185 228 228 Z" 
          fill="url(#petalBevelLight)" stroke="url(#lotus3DGrad)" stroke-width="1.3"/>
    <path d="M228 52 C195 95 176 114 140 140 C166 104 185 85 228 52 Z" 
          fill="url(#petalBevelLight)" stroke="url(#lotus3DGrad)" stroke-width="1.3"/>
    <path d="M52 228 C85 185 104 166 140 140 C114 176 95 195 52 228 Z" 
          fill="url(#petalBevelLight)" stroke="url(#lotus3DGrad)" stroke-width="1.3"/>

    <!-- Radiant Stamen Pearls -->
    <circle cx="140" cy="62" r="3.5" fill="#E0E7FF" filter="drop-shadow(0 1px 2px #000)"/>
    <circle cx="140" cy="218" r="3.5" fill="#E0E7FF" filter="drop-shadow(0 1px 2px #000)"/>
    <circle cx="62" cy="140" r="3.5" fill="#E0E7FF" filter="drop-shadow(0 1px 2px #000)"/>
    <circle cx="218" cy="140" r="3.5" fill="#E0E7FF" filter="drop-shadow(0 1px 2px #000)"/>
    <circle cx="85" cy="85" r="3" fill="#38BDF8" filter="drop-shadow(0 1px 2px #000)"/>
    <circle cx="195" cy="195" r="3" fill="#38BDF8" filter="drop-shadow(0 1px 2px #000)"/>
    <circle cx="195" cy="85" r="3" fill="#38BDF8" filter="drop-shadow(0 1px 2px #000)"/>
    <circle cx="85" cy="195" r="3" fill="#38BDF8" filter="drop-shadow(0 1px 2px #000)"/>
  </g>
</svg>"""

# 2. 3D Guilloché Floral Rosette (12-Lobed Precision Engraving)
GEOMETRIC_ROSETTE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 280" fill="none">
  <defs>
    <linearGradient id="rosette3DGrad" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38BDF8" stop-opacity="0.95"/>
      <stop offset="50%" stop-color="#818CF8" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#34D399" stop-opacity="0.95"/>
    </linearGradient>

    <!-- 3D Deboss Filter with Opposing Highlight/Shadow -->
    <filter id="deboss3DDeep" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="2" dy="4" stdDeviation="3" flood-color="#000000" flood-opacity="0.8"/>
      <feDropShadow dx="-1" dy="-1" stdDeviation="1.5" flood-color="#FFFFFF" flood-opacity="0.3"/>
    </filter>
  </defs>

  <g filter="url(#deboss3DDeep)" stroke="url(#rosette3DGrad)">
    <!-- Concentric Engraved Calibrated Rings -->
    <circle cx="140" cy="140" r="128" stroke-width="0.9" opacity="0.4"/>
    <circle cx="140" cy="140" r="105" stroke-width="0.8" opacity="0.5"/>
    <circle cx="140" cy="140" r="70" stroke-width="1.1" opacity="0.65"/>
    <circle cx="140" cy="140" r="28" stroke-width="1.5" opacity="0.85"/>

    <!-- 12 Overlapping 3D Guilloché Petal Ellipses -->
    <ellipse cx="140" cy="140" rx="105" ry="38" stroke-width="1.1" opacity="0.75" transform="rotate(0 140 140)"/>
    <ellipse cx="140" cy="140" rx="105" ry="38" stroke-width="1.1" opacity="0.75" transform="rotate(30 140 140)"/>
    <ellipse cx="140" cy="140" rx="105" ry="38" stroke-width="1.1" opacity="0.75" transform="rotate(60 140 140)"/>
    <ellipse cx="140" cy="140" rx="105" ry="38" stroke-width="1.1" opacity="0.75" transform="rotate(90 140 140)"/>
    <ellipse cx="140" cy="140" rx="105" ry="38" stroke-width="1.1" opacity="0.75" transform="rotate(120 140 140)"/>
    <ellipse cx="140" cy="140" rx="105" ry="38" stroke-width="1.1" opacity="0.75" transform="rotate(150 140 140)"/>

    <!-- 3D Faceted Center Star Bloom -->
    <polygon points="140,110 149,131 170,140 149,149 140,170 131,149 110,140 131,131" 
             stroke-width="1.5" fill="url(#rosette3DGrad)" fill-opacity="0.2"/>
    <circle cx="140" cy="140" r="5" fill="#38BDF8"/>
  </g>
</svg>"""

# 3. 3D Botanical Acanthus Crest (Sculpted Vine & Bloom Filigree)
BOTANICAL_FLOURISH_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 280" fill="none">
  <defs>
    <linearGradient id="vine3DGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#F43F5E" stop-opacity="0.85"/>
      <stop offset="50%" stop-color="#C084FC" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#6366F1" stop-opacity="0.85"/>
    </linearGradient>

    <filter id="vine3DEmboss" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="5" stdDeviation="4" flood-color="#000000" flood-opacity="0.8"/>
      <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#C084FC" flood-opacity="0.3"/>
      <feDropShadow dx="-1" dy="-1" stdDeviation="1" flood-color="#FFFFFF" flood-opacity="0.4"/>
    </filter>
  </defs>

  <g filter="url(#vine3DEmboss)" stroke="url(#vine3DGrad)">
    <!-- Central Tiered 3D Blossom -->
    <path d="M140 32 C155 58 162 88 140 112 C118 88 125 58 140 32 Z" 
          stroke-width="1.8" fill="url(#vine3DGrad)" fill-opacity="0.18"/>
    <path d="M140 112 C158 135 158 164 140 188 C122 164 122 135 140 112 Z" 
          stroke-width="1.8" fill="url(#vine3DGrad)" fill-opacity="0.12"/>
    
    <!-- Sweeping 3D Symmetrical Tendrils -->
    <path d="M140 112 C105 94 58 106 46 148 C34 190 76 220 112 202 C130 192 135 178 140 172" 
          stroke-width="1.9" stroke-linecap="round"/>
    <path d="M140 112 C175 94 222 106 234 148 C246 190 204 220 168 202 C150 192 145 178 140 172" 
          stroke-width="1.9" stroke-linecap="round"/>

    <!-- Sculpted Leaf Buds (Left Wing) -->
    <path d="M52 130 C40 118 34 136 44 148 C52 142 56 136 52 130 Z" 
          stroke-width="1.3" fill="url(#vine3DGrad)" fill-opacity="0.3"/>
    <path d="M70 190 C58 202 76 220 88 208 C82 196 76 190 70 190 Z" 
          stroke-width="1.3" fill="url(#vine3DGrad)" fill-opacity="0.3"/>
    <path d="M100 112 C88 94 106 88 112 100 C108 106 104 112 100 112 Z" 
          stroke-width="1.3" fill="url(#vine3DGrad)" fill-opacity="0.3"/>

    <!-- Sculpted Leaf Buds (Right Wing) -->
    <path d="M228 130 C240 118 246 136 236 148 C228 142 224 136 228 130 Z" 
          stroke-width="1.3" fill="url(#vine3DGrad)" fill-opacity="0.3"/>
    <path d="M210 190 C222 202 204 220 192 208 C198 196 204 190 210 190 Z" 
          stroke-width="1.3" fill="url(#vine3DGrad)" fill-opacity="0.3"/>
    <path d="M180 112 C192 94 174 88 168 100 C172 106 176 112 180 112 Z" 
          stroke-width="1.3" fill="url(#vine3DGrad)" fill-opacity="0.3"/>

    <!-- Bottom Dimensional Scroll Anchor -->
    <path d="M112 202 C124 226 135 244 140 256 C145 244 156 226 168 202" stroke-width="1.4"/>
    <circle cx="140" cy="260" r="3.5" fill="#F43F5E" filter="drop-shadow(0 1px 3px #000)"/>
  </g>
</svg>"""

def get_svg_data_uri(svg_string: str) -> str:
    """Converts raw SVG into an inline data URI for CSS background-image embedding."""
    clean_svg = " ".join(svg_string.split())
    encoded = urllib.parse.quote(clean_svg)
    return f"data:image/svg+xml;utf8,{encoded}"

IMPRINT_LOTUS_DATA_URI = get_svg_data_uri(CELESTIAL_LOTUS_SVG)
IMPRINT_ROSETTE_DATA_URI = get_svg_data_uri(GEOMETRIC_ROSETTE_SVG)
IMPRINT_FLOURISH_DATA_URI = get_svg_data_uri(BOTANICAL_FLOURISH_SVG)

ALL_3D_IMPRINTS = [
    {
        "id": "lotus",
        "name": "Celestial Lotus Bloom",
        "tag": "Sacred Geometry 3D Imprint",
        "desc": "Concentric 8-fold lotus petals with 3D drop bevels and central radiant pearl.",
        "svg": CELESTIAL_LOTUS_SVG,
        "accent": "#818CF8"
    },
    {
        "id": "rosette",
        "name": "Guilloché Floral Rosette",
        "tag": "Precision Engraved 3D Imprint",
        "desc": "12-lobed interlocking geometric flower matrix with tactile debossed depth.",
        "svg": GEOMETRIC_ROSETTE_SVG,
        "accent": "#38BDF8"
    },
    {
        "id": "flourish",
        "name": "Botanical Acanthus Crest",
        "tag": "Organic Filigree 3D Imprint",
        "desc": "Symmetrical curving vine tendrils, acanthus leaf buds, and embossed floral crest.",
        "svg": BOTANICAL_FLOURISH_SVG,
        "accent": "#F43F5E"
    }
]
