"""Authentication routes"""
import os
import httpx
from fasthtml.common import *
from frontend.pages.login import login_page
from frontend.pages.welcome import welcome_page

def login_page_with_error(error_message: str):
    """Return login page with error message"""
    from styles.login import login_styles
    from components.login_form import logo_section, social_login_section
    from components.theme_toggle import theme_toggle
    
    # Create login form with error message
    login_form_with_error = Form(
        Div(
            P(error_message, cls="error-message", style="color: var(--error); margin-bottom: 1rem; text-align: center; font-size: 14px;"),
            cls="error-container"
        ),
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
                login_form_with_error,
                social_login_section(),
                cls="login-container"
            )
        )
    )

def setup_auth_routes(rt):
    """Setup authentication routes"""
    
    @rt("/")
    def get_login():
        return login_page()
    
    @rt("/login", methods=["POST"])
    async def post_login(username: str, password: str):
        """Handle login form submission"""
        backend_url = os.getenv("FASTSET_BACKEND_URL", "http://localhost:8000")
        login_url = f"{backend_url}/v1/auth/login"
        
        try:
            # Prepare login data
            login_data = {
                "username": username,
                "password": password
            }
            
            # Make API call to backend
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    login_url,
                    json=login_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    # Login successful
                    response_data = response.json()
                    
                    # Create redirect response
                    redirect_response = RedirectResponse("/welcome", status_code=302)
                    # Set the access_token cookie if provided by backend
                    if "access_token" in response_data:
                        redirect_response.set_cookie(
                            key="access_token",
                            value=response_data["access_token"],
                            httponly=True,
                            secure=True,  # Use HTTPS in production
                            samesite="lax"
                        )
                    
                    # Also set any other cookies from backend response
                    for cookie in response.cookies.items():
                        redirect_response.set_cookie(
                            key=cookie[0],
                            value=cookie[1],
                            httponly=True,
                            secure=True,
                            samesite="lax"
                        )
                    
                    return redirect_response
                    
                else:
                    # Login failed - return login page with error
                    error_message = "Invalid username or password"
                    if response.status_code == 422:
                        try:
                            error_data = response.json()
                            error_message = error_data.get("detail", error_message)
                        except:
                            pass
                    
                    return login_page_with_error(error_message)
                    
        except httpx.RequestError as e:
            # Network error or backend unavailable
            error_message = "Unable to connect to authentication service. Please try again."
            return login_page_with_error(error_message)
        except Exception as e:
            # Other unexpected errors
            error_message = "An unexpected error occurred. Please try again."
            return login_page_with_error(error_message)
    
    @rt("/welcome")
    def get_dashboard(request):
        """Dashboard page - requires authentication"""
        # Check if user has access_token cookie
        access_token = request.cookies.get("access_token")
        if not access_token:
            # Redirect to login if no token
            return RedirectResponse("/", status_code=302)
        
        return welcome_page()
    
    @rt("/logout", methods=["POST", "GET"])
    def logout():
        """Handle logout"""
        response = RedirectResponse("/", status_code=302)
        # Clear the access_token cookie
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response