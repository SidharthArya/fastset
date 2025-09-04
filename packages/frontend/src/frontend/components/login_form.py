"""Login form component"""
from fasthtml.common import *

def login_form():
    """Create the login form component"""
    return Form(
        Div(
            Label("Username or Email", for_="username"),
            Input(
                type="text", 
                id="username", 
                name="username", 
                placeholder="Enter your username or email", 
                required=True
            ),
            cls="form-group"
        ),
        Div(
            Label("Password", for_="password"),
            Input(
                type="password", 
                id="password", 
                name="password", 
                placeholder="Enter your password", 
                required=True
            ),
            cls="form-group"
        ),
        Button("Sign In", type="submit", cls="login-btn"),
        method="post",
        action="/login"
    )

def logo_section():
    """Create the logo section component"""
    return Div(
        H1("FastSet BI"),
        P("Business Intelligence Platform"),
        cls="logo"
    )

def social_login_section():
    """Create the social login section component"""
    return Div(
        Div(
            A("Forgot your password?", href="/forgot-password"),
            cls="forgot-password"
        ),
        Div(
            Span("or"),
            cls="divider"
        ),
        Div(
            Button("Google", cls="social-btn"),
            Button("GitHub", cls="social-btn"),
            cls="social-login"
        )
    )