"""Login page"""
from fasthtml.common import *
from styles.login import login_styles
from components.login_form import login_form, logo_section, social_login_section
from components.theme_toggle import theme_toggle

def login_page():
    """Create the complete login page"""
    return Html(
        Head(
            Title("FastSet BI - Login"),
            login_styles,
            Meta(name="viewport", content="width=device-width, initial-scale=1.0")
        ),
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