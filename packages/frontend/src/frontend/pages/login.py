"""Login page"""
from fasthtml.common import *
from frontend.components.login_form import login_form, logo_section, social_login_section
from frontend.components.theme_toggle import theme_toggle
from frontend.utils.header import get_head

def login_page():
    """Create the complete login page"""
    return Html(
       get_head("Login"),
        Body(
            theme_toggle(),
            Div(
                logo_section(),
                login_form(),
                social_login_section(),
                cls="login-container"
            )
        )
    )