"""Dashboard page"""
from fasthtml.common import *
from frontend.styles.base import base_styles

from frontend.utils.header import get_head, get_header

def welcome_page():
    """Create the dashboard page"""
    return Html(
        get_head(),
        Body(
            Div(get_header("Welcome"),

                Main(
                    Div(
                        H2("Welcome to FastSet BI Dashboard", cls="text-primary"),
                        P("You have successfully logged in!", cls="text-secondary"),
                        P("Your business intelligence platform is ready to use.", cls="text-muted"),
                        cls="dashboard-content"
                    ),
                    cls="container"
                ),
                cls="dashboard-layout"
            ),
            Style("""
                .dashboard-layout {
                    min-height: 100vh;
                    background: var(--bg-secondary);
                }
                
                .dashboard-header {
                    background: var(--bg-primary);
                    border-bottom: 1px solid var(--border-light);
                    padding: 1rem 0;
                    box-shadow: 0 2px 4px var(--shadow-light);
                }
                
                .header-content {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 0 20px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .header-content h1 {
                    font-size: 24px;
                    font-weight: 600;
                    margin: 0;
                }
                
                .logout-btn {
                    background: var(--gradient-primary);
                    color: var(--text-inverse);
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: 500;
                    cursor: pointer;
                    transition: all 0.2s ease;
                }
                
                .logout-btn:hover {
                    background: var(--gradient-secondary);
                    transform: translateY(-1px);
                }
                
                .dashboard-content {
                    padding: 2rem 0;
                }
                
                .dashboard-content h2 {
                    font-size: 32px;
                    font-weight: 600;
                    margin-bottom: 1rem;
                }
                
                .dashboard-content p {
                    font-size: 16px;
                    margin-bottom: 0.5rem;
                }
            """)
        )
    )