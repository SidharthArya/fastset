"""FastSet BI Frontend Application"""
from fasthtml.common import *
from routes.auth import setup_auth_routes

# Create FastHTML app
app, rt = fast_app(live=True)

# Setup routes
setup_auth_routes(rt)

serve()