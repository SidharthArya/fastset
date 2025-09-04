"""Theme toggle component"""
from fasthtml.common import *

def theme_toggle():
    """Create a theme toggle button"""
    return Div(
        Button(
            "🌙",
            id="theme-toggle",
            cls="theme-toggle",
            onclick="toggleTheme()",
            title="Toggle dark/light theme"
        ),
        Script("""
            function toggleTheme() {
                const html = document.documentElement;
                const currentTheme = html.getAttribute('data-theme');
                const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                html.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
                
                // Update button icon
                const button = document.getElementById('theme-toggle');
                button.textContent = newTheme === 'dark' ? '☀️' : '🌙';
            }
            
            // Initialize theme from localStorage or system preference
            function initTheme() {
                const savedTheme = localStorage.getItem('theme');
                const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
                const theme = savedTheme || systemTheme;
                
                document.documentElement.setAttribute('data-theme', theme);
                const button = document.getElementById('theme-toggle');
                if (button) {
                    button.textContent = theme === 'dark' ? '☀️' : '🌙';
                }
            }
            
            // Initialize on page load
            document.addEventListener('DOMContentLoaded', initTheme);
        """),
        cls="theme-toggle-container"
    )