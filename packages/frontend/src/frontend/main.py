"""FastSet BI Frontend Application"""
from fasthtml.common import *
from frontend.routes.auth import setup_auth_routes
from frontend.pages.sql import sql_page
from frontend.pages.database import database_page
from frontend.pages.users import users_page

# Create FastHTML app
app, rt = fast_app(live=True)

# Setup routes
setup_auth_routes(rt)

@rt("/sql")
def get():
    return sql_page()

@rt("/settings/database")
def get():
    return database_page()

@rt("/settings/users")
async def get(request):
    return await users_page(request)

serve()