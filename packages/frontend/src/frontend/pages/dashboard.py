"""Dashboard page"""
from fasthtml.common import *

def dashboard_page():
    """Create the dashboard page"""
    return Html(
        Head(Title("FastSet BI - Dashboard")),
        Body(
            H1("Welcome to FastSet BI Dashboard"),
            P("You have successfully logged in!"),
            A("Logout", href="/")
        )
    )