"""Login page styles using color system"""
from fasthtml.common import Style
from .colors import color_variables

login_styles = Style(f"""
    {color_variables.children[0]}
    
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    body {{
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: var(--gradient-background);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }}
    
    .login-container {{
        background: var(--bg-primary);
        border-radius: 12px;
        box-shadow: 0 8px 25px var(--shadow-light);
        padding: 40px;
        width: 100%;
        max-width: 400px;
        margin: 20px;
        border: 1px solid var(--border-light);
    }}
    
    .logo {{
        text-align: center;
        margin-bottom: 30px;
    }}
    
    .logo h1 {{
        color: var(--primary);
        font-size: 28px;
        font-weight: 600;
        margin-bottom: 8px;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .logo p {{
        color: var(--text-secondary);
        font-size: 14px;
        font-weight: 400;
    }}
    
    .form-group {{
        margin-bottom: 20px;
    }}
    
    .form-group label {{
        display: block;
        margin-bottom: 6px;
        color: var(--text-primary);
        font-weight: 500;
        font-size: 14px;
    }}
    
    .form-group input {{
        width: 100%;
        padding: 12px 16px;
        border: 2px solid var(--border-light);
        border-radius: 8px;
        font-size: 14px;
        transition: all 0.3s ease;
        background: var(--bg-primary);
        color: var(--text-primary);
    }}
    
    .form-group input:focus {{
        outline: none;
        border-color: var(--primary);
        box-shadow: 0 0 0 3px var(--primary-light);
        background: var(--bg-primary);
    }}
    
    .login-btn {{
        width: 100%;
        background: var(--gradient-primary);
        color: var(--text-inverse);
        border: none;
        padding: 14px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 10px;
        box-shadow: 0 4px 15px var(--primary-light);
    }}
    
    .login-btn:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px var(--shadow-light);
        background: var(--gradient-secondary);
    }}
    
    .forgot-password {{
        text-align: center;
        margin-top: 20px;
    }}
    
    .forgot-password a {{
        color: var(--secondary);
        text-decoration: none;
        font-size: 14px;
        font-weight: 500;
        transition: color 0.2s ease;
    }}
    
    .forgot-password a:hover {{
        color: var(--primary);
        text-decoration: underline;
    }}
    
    .divider {{
        text-align: center;
        margin: 30px 0;
        position: relative;
        color: var(--text-secondary);
        font-size: 14px;
        font-weight: 500;
    }}
    
    .divider::before {{
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-medium), transparent);
        z-index: 1;
    }}
    
    .divider span {{
        background: var(--bg-primary);
        padding: 0 20px;
        position: relative;
        z-index: 2;
    }}
    
    .social-login {{
        display: flex;
        gap: 12px;
    }}
    
    .social-btn {{
        flex: 1;
        padding: 12px;
        border: 2px solid var(--border-light);
        background: var(--bg-primary);
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 14px;
        font-weight: 500;
        color: var(--text-primary);
    }}
    
    .social-btn:hover {{
        border-color: var(--tertiary);
        background: var(--tertiary-light);
        box-shadow: 0 2px 8px var(--shadow-light);
    }}
    
    .social-btn:first-child:hover {{
        border-color: var(--accent);
        background: var(--accent-light);
        box-shadow: 0 2px 8px var(--shadow-light);
    }}
    
    /* Theme Toggle Styles */
    .theme-toggle-container {{
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
    }}
    
    .theme-toggle {{
        background: var(--bg-primary);
        border: 2px solid var(--border-light);
        border-radius: 50%;
        width: 48px;
        height: 48px;
        font-size: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px var(--shadow-light);
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    .theme-toggle:hover {{
        background: var(--bg-secondary);
        border-color: var(--primary);
        transform: scale(1.05);
        box-shadow: 0 4px 12px var(--shadow-medium);
    }}
    
    /* Dark theme specific adjustments */
    [data-theme="dark"] .login-container {{
        background: var(--bg-primary);
        border-color: var(--border-medium);
        box-shadow: 0 8px 25px var(--shadow-medium);
    }}
    
    [data-theme="dark"] .form-group input {{
        background: var(--bg-secondary);
        border-color: var(--border-light);
        color: var(--text-primary);
    }}
    
    [data-theme="dark"] .form-group input:focus {{
        background: var(--bg-primary);
        border-color: var(--primary);
    }}
    
    [data-theme="dark"] .social-btn {{
        background: var(--bg-secondary);
        border-color: var(--border-light);
        color: var(--text-primary);
    }}
""")