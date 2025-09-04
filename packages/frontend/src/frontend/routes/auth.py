"""Authentication routes"""
from fasthtml.common import *
from pages.login import login_page
from pages.dashboard import dashboard_page

def setup_auth_routes(rt):
    """Setup authentication routes"""
    
    @rt("/")
    def get_login():
        return login_page()
    
    @rt("/login", methods=["POST"])
    def post_login(username: str, password: str):
        # Simple authentication logic (replace with real auth)
        if username and password:
            return RedirectResponse("/dashboard", status_code=302)
        else:
            return login_page()  # Return login page with error
    
    @rt("/dashboard")
    def get_dashboard():
        return dashboard_page()