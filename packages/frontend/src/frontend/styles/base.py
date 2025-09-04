"""Base styles with color system"""
from fasthtml.common import Style
from .colors import color_variables

base_styles = Style(f"""
    {color_variables.children[0]}
    
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.6;
        color: var(--text-primary);
        background: var(--bg-primary);
    }}
    
    .container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }}
    
    /* Utility classes using color variables */
    .text-primary {{ color: var(--text-primary); }}
    .text-secondary {{ color: var(--text-secondary); }}
    .text-muted {{ color: var(--text-muted); }}
    .text-inverse {{ color: var(--text-inverse); }}
    
    .bg-primary {{ background: var(--bg-primary); }}
    .bg-secondary {{ background: var(--bg-secondary); }}
    .bg-tertiary {{ background: var(--bg-tertiary); }}
    
    .border-light {{ border-color: var(--border-light); }}
    .border-medium {{ border-color: var(--border-medium); }}
    .border-dark {{ border-color: var(--border-dark); }}
""")