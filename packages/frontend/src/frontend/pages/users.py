"""Users Management Page - Pure FastHTML with Server-Side Rendering"""

from fasthtml.common import *
from frontend.utils.header import get_head, get_header
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime


async def fetch_users_from_api(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = None,
    access_token: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Fetch users from the backend API"""
    try:
        params = {"skip": skip, "limit": limit}
        if search:
            params["search"] = search

        headers = {"Content-Type": "application/json"}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://localhost:8000/v1/users/",
                params=params,
                headers=headers,
                timeout=10.0,
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return []

    except Exception as e:
        print(f"Error fetching users: {e}")
        return []


async def create_user_api(
    user_data: Dict[str, Any], access_token: str
) -> Dict[str, Any]:
    """Create a new user via API"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/v1/users/",
                json=user_data,
                headers=headers,
                timeout=10.0,
            )

            if response.status_code == 201:
                return {"success": True, "user": response.json()}
            else:
                error_detail = response.json().get("detail", "Failed to create user")
                return {"success": False, "error": error_detail}

    except Exception as e:
        return {"success": False, "error": str(e)}


async def update_user_api(
    user_id: int, user_data: Dict[str, Any], access_token: str
) -> Dict[str, Any]:
    """Update a user via API"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"http://localhost:8000/v1/users/{user_id}",
                json=user_data,
                headers=headers,
                timeout=10.0,
            )

            if response.status_code == 200:
                return {"success": True, "user": response.json()}
            else:
                error_detail = response.json().get("detail", "Failed to update user")
                return {"success": False, "error": error_detail}

    except Exception as e:
        return {"success": False, "error": str(e)}


async def delete_user_api(user_id: int, access_token: str) -> Dict[str, Any]:
    """Delete a user via API"""
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"http://localhost:8000/v1/users/{user_id}",
                headers=headers,
                timeout=10.0,
            )

            if response.status_code == 200:
                return {"success": True, "message": "User deleted successfully"}
            else:
                error_detail = response.json().get("detail", "Failed to delete user")
                return {"success": False, "error": error_detail}

    except Exception as e:
        return {"success": False, "error": str(e)}


def create_user_card(
    user_data: Dict[str, Any],
    current_page: int = 1,
    search: str = "",
    status: str = "all",
):
    """Create a user card component with FastHTML links"""
    user_id = user_data.get("id", 0)
    username = user_data.get("username", "Unknown")
    email = user_data.get("email", "No email")
    is_active = user_data.get("is_active", True)
    created_at = user_data.get("created_at", "Unknown")
    attributes = user_data.get("attributes", [])

    status_color = "#28a745" if is_active else "#dc3545"
    status_text = "Active" if is_active else "Inactive"

    # Format creation date
    try:
        if isinstance(created_at, str) and len(created_at) > 10:
            created_date = created_at[:10]
        else:
            created_date = str(created_at)
    except:
        created_date = "Unknown"

    return Div(
        Div(
            Div(
                Div(
                    H4(username, cls="user-card-title"),
                    Span(
                        status_text,
                        cls="user-status-badge",
                        style=f"background-color: {status_color}",
                    ),
                    cls="user-card-header",
                ),
                P(email, cls="user-email"),
                P(f"Created: {created_date}", cls="user-created"),
                Div(
                    Span(f"{len(attributes)} attributes", cls="attributes-count"),
                    cls="user-meta",
                ),
                cls="user-card-content",
            ),
            Div(
                A(
                    "View",
                    href=f"/settings/users/{user_id}",
                    cls="btn btn-outline btn-sm",
                ),
                A(
                    "Edit",
                    href=f"/settings/users/{user_id}/edit?page={current_page}&search={search}&status={status}",
                    cls="btn btn-primary btn-sm",
                ),
                A(
                    "Delete",
                    href=f"/settings/users/{user_id}/delete?page={current_page}&search={search}&status={status}",
                    cls="btn btn-danger btn-sm",
                    onclick=f"return confirm('Are you sure you want to delete user {username}?')",
                ),
                cls="user-card-actions",
            ),
            cls="user-card",
        ),
        cls="user-card-wrapper",
    )


async def users_page(
    request,
    users_data: List[Dict[str, Any]] = None,
    current_page: int = 1,
    page_size: int = 20,
    search_term: str = "",
    status_filter: str = "all",
    total_users: int = 0,
    success_message: str = "",
    error_message: str = "",
):
    """Create the users management page with server-side rendered data"""
    if not users_data:
        access_token = request.cookies.get("access_token")
        users = await fetch_users_from_api(access_token=access_token)
    # users = users_data or []
    has_next = len(users) == page_size
    has_prev = current_page > 1

    # Create user cards
    user_cards = [
        create_user_card(user, current_page, search_term, status_filter)
        for user in users
    ]

    return Html(
        get_head("Users Management"),
        Body(
            get_header("Users Management"),
            Main(
                # Success/Error Messages
                *(
                    [Div(success_message, cls="alert alert-success")]
                    if success_message
                    else []
                ),
                *(
                    [Div(error_message, cls="alert alert-error")]
                    if error_message
                    else []
                ),
                # Page Header with Actions
                Div(
                    Div(
                        H1("Users Management", cls="page-title"),
                        P(
                            "Manage user accounts, permissions, and attributes",
                            cls="page-subtitle",
                        ),
                        cls="page-header-content",
                    ),
                    Div(
                        A(
                            "+ Add User",
                            href=f"/users/add?page={current_page}&search={search_term}&status={status_filter}",
                            cls="btn btn-primary",
                        ),
                        A(
                            "Export Users",
                            href="/users/export",
                            cls="btn btn-secondary",
                        ),
                        A(
                            "Refresh",
                            href=f"/users?page={current_page}&search={search_term}&status={status_filter}",
                            cls="btn btn-secondary",
                        ),
                        cls="page-actions",
                    ),
                    cls="page-header",
                ),
                # Filter and Search Bar
                Form(
                    Div(
                        Input(
                            type="text",
                            name="search",
                            placeholder="Search users by username or email...",
                            cls="search-input",
                            value=search_term,
                        ),
                        Select(
                            Option(
                                "All Status",
                                value="all",
                                selected=(status_filter == "all"),
                            ),
                            Option(
                                "Active",
                                value="active",
                                selected=(status_filter == "active"),
                            ),
                            Option(
                                "Inactive",
                                value="inactive",
                                selected=(status_filter == "inactive"),
                            ),
                            name="status",
                            cls="filter-select",
                        ),
                        Input(
                            type="number",
                            name="size",
                            placeholder="Page size",
                            value=str(page_size),
                            min="10",
                            max="100",
                            cls="page-size-input",
                        ),
                        Input(
                            type="hidden", name="page", value="1"
                        ),  # Reset to page 1 on search
                        Button("Search", type="submit", cls="btn btn-primary"),
                        cls="filters",
                    ),
                    method="get",
                    action="/users",
                    cls="filter-bar",
                ),
                # Users Grid
                Div(
                    *(
                        user_cards
                        if user_cards
                        else [
                            Div(
                                "No users found. Try adjusting your search criteria or add some users.",
                                cls="no-users-message",
                            )
                        ]
                    ),
                    cls="users-grid",
                ),
                # Pagination
                Div(
                    (
                        A(
                            "← Previous",
                            href=(
                                f"/users?page={current_page-1}&size={page_size}&search={search_term}&status={status_filter}"
                                if has_prev
                                else "#"
                            ),
                            cls=f"btn btn-outline {'disabled' if not has_prev else ''}",
                        )
                        if has_prev
                        else Span("← Previous", cls="btn btn-outline disabled")
                    ),
                    Span(f"Page {current_page}", cls="page-info"),
                    (
                        A(
                            "Next →",
                            href=(
                                f"/users?page={current_page+1}&size={page_size}&search={search_term}&status={status_filter}"
                                if has_next
                                else "#"
                            ),
                            cls=f"btn btn-outline {'disabled' if not has_next else ''}",
                        )
                        if has_next
                        else Span("Next →", cls="btn btn-outline disabled")
                    ),
                    cls="pagination",
                ),
                cls="users-page-container",
            ),
            # Styles
            Style(
                """
                .users-page-container {
                    max-width: 1400px;
                    margin: 0 auto;
                    padding: 20px;
                }
                
                .alert {
                    padding: 12px 20px;
                    margin-bottom: 20px;
                    border-radius: 6px;
                    font-weight: 500;
                }
                
                .alert-success {
                    background: #d4edda;
                    color: #155724;
                    border: 1px solid #c3e6cb;
                }
                
                .alert-error {
                    background: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                }
                
                .page-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    margin-bottom: 30px;
                    padding-bottom: 20px;
                    border-bottom: 1px solid var(--border-light);
                }
                
                .page-header-content h1 {
                    margin: 0 0 8px 0;
                    color: var(--text-primary);
                    font-size: 2rem;
                    font-weight: 600;
                }
                
                .page-subtitle {
                    margin: 0;
                    color: var(--text-secondary);
                    font-size: 1rem;
                }
                
                .page-actions {
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                }
                
                .filter-bar {
                    margin-bottom: 25px;
                }
                
                .filters {
                    display: flex;
                    gap: 15px;
                    align-items: center;
                    flex-wrap: wrap;
                }
                
                .search-input {
                    padding: 10px 15px;
                    border: 1px solid var(--border-medium);
                    border-radius: 6px;
                    background: var(--bg-primary);
                    color: var(--text-primary);
                    font-size: 14px;
                    min-width: 300px;
                }
                
                .search-input:focus {
                    outline: none;
                    border-color: var(--primary);
                    box-shadow: 0 0 0 2px var(--primary-light);
                }
                
                .filter-select, .page-size-input {
                    padding: 10px 15px;
                    border: 1px solid var(--border-medium);
                    border-radius: 6px;
                    background: var(--bg-primary);
                    color: var(--text-primary);
                    font-size: 14px;
                    min-width: 120px;
                }
                
                .no-users-message {
                    text-align: center;
                    padding: 60px 20px;
                    color: var(--text-secondary);
                    font-size: 16px;
                    background: var(--bg-secondary);
                    border-radius: 8px;
                    border: 1px solid var(--border-light);
                    grid-column: 1 / -1;
                }
                
                .users-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }
                
                .user-card {
                    background: var(--bg-secondary);
                    border: 1px solid var(--border-light);
                    border-radius: 8px;
                    padding: 20px;
                    transition: all 0.2s ease;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    min-height: 160px;
                }
                
                .user-card:hover {
                    border-color: var(--primary);
                    box-shadow: 0 4px 12px var(--shadow-light);
                    transform: translateY(-2px);
                }
                
                .user-card-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    margin-bottom: 10px;
                }
                
                .user-card-title {
                    margin: 0;
                    color: var(--text-primary);
                    font-size: 1.1rem;
                    font-weight: 600;
                }
                
                .user-status-badge {
                    color: white;
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: 500;
                }
                
                .user-email {
                    color: var(--text-secondary);
                    font-size: 14px;
                    margin: 0 0 5px 0;
                }
                
                .user-created {
                    color: var(--text-muted);
                    font-size: 12px;
                    margin: 0 0 10px 0;
                }
                
                .user-meta {
                    margin-bottom: 15px;
                }
                
                .attributes-count {
                    background: var(--bg-tertiary);
                    color: var(--text-secondary);
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-size: 11px;
                }
                
                .user-card-actions {
                    display: flex;
                    gap: 8px;
                    flex-wrap: wrap;
                }
                
                .pagination {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    gap: 20px;
                    margin-top: 30px;
                }
                
                .page-info {
                    color: var(--text-secondary);
                    font-size: 14px;
                }
                
                .btn {
                    padding: 8px 16px;
                    border-radius: 6px;
                    border: none;
                    cursor: pointer;
                    font-size: 14px;
                    font-weight: 500;
                    transition: all 0.2s;
                    text-decoration: none;
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                }
                
                .btn.disabled {
                    opacity: 0.5;
                    cursor: not-allowed;
                    pointer-events: none;
                }
                
                .btn-sm {
                    padding: 6px 12px;
                    font-size: 13px;
                }
                
                .btn-primary {
                    background: var(--primary);
                    color: white;
                }
                
                .btn-primary:hover:not(.disabled) {
                    background: var(--primary-hover);
                }
                
                .btn-secondary {
                    background: var(--bg-tertiary);
                    color: var(--text-primary);
                    border: 1px solid var(--border-medium);
                }
                
                .btn-secondary:hover:not(.disabled) {
                    background: var(--border-light);
                }
                
                .btn-outline {
                    background: transparent;
                    color: var(--primary);
                    border: 1px solid var(--primary);
                }
                
                .btn-outline:hover:not(.disabled) {
                    background: var(--primary);
                    color: white;
                }
                
                .btn-danger {
                    background: #dc3545;
                    color: white;
                }
                
                .btn-danger:hover:not(.disabled) {
                    background: #c82333;
                }
                
                @media (max-width: 768px) {
                    .users-page-container {
                        padding: 15px;
                    }
                    
                    .page-header {
                        flex-direction: column;
                        gap: 15px;
                        align-items: stretch;
                    }
                    
                    .page-actions {
                        justify-content: stretch;
                    }
                    
                    .page-actions .btn {
                        flex: 1;
                    }
                    
                    .users-grid {
                        grid-template-columns: 1fr;
                    }
                    
                    .filters {
                        flex-direction: column;
                        align-items: stretch;
                    }
                    
                    .search-input, .filter-select, .page-size-input {
                        min-width: auto;
                        width: 100%;
                    }
                    
                    .pagination {
                        flex-direction: column;
                        gap: 10px;
                    }
                }
            """
            ),
            cls="users-page",
        ),
    )


def add_user_form(
    current_page: int = 1,
    search: str = "",
    status: str = "all",
    error_message: str = "",
):
    """Create add user form page"""
    return Html(
        get_head("Add User"),
        Body(
            get_header("Add User"),
            Main(
                Div(
                    A(
                        "← Back to Users",
                        href=f"/users?page={current_page}&search={search}&status={status}",
                        cls="btn btn-outline",
                    ),
                    cls="back-nav",
                ),
                *(
                    [Div(error_message, cls="alert alert-error")]
                    if error_message
                    else []
                ),
                Div(
                    H1("Add New User", cls="form-title"),
                    Form(
                        Div(
                            Label("Username", **{"for": "username"}),
                            Input(
                                type="text",
                                name="username",
                                id="username",
                                cls="form-input",
                                required=True,
                            ),
                            cls="form-group",
                        ),
                        Div(
                            Label("Email", **{"for": "email"}),
                            Input(
                                type="email",
                                name="email",
                                id="email",
                                cls="form-input",
                                required=True,
                            ),
                            cls="form-group",
                        ),
                        Div(
                            Label("Password", **{"for": "password"}),
                            Input(
                                type="password",
                                name="password",
                                id="password",
                                cls="form-input",
                                required=True,
                                minlength="8",
                            ),
                            cls="form-group",
                        ),
                        Div(
                            Label(
                                Input(
                                    type="checkbox",
                                    name="is_active",
                                    value="true",
                                    checked=True,
                                ),
                                " Active User",
                                cls="checkbox-label",
                            ),
                            cls="form-group",
                        ),
                        Input(type="hidden", name="page", value=str(current_page)),
                        Input(type="hidden", name="search", value=search),
                        Input(type="hidden", name="status", value=status),
                        Div(
                            A(
                                "Cancel",
                                href=f"/users?page={current_page}&search={search}&status={status}",
                                cls="btn btn-secondary",
                            ),
                            Button("Create User", type="submit", cls="btn btn-primary"),
                            cls="form-actions",
                        ),
                        method="post",
                        action="/users/add",
                        cls="user-form",
                    ),
                    cls="form-container",
                ),
                cls="add-user-page",
            ),
            Style(
                """
                .add-user-page {
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }
                
                .back-nav {
                    margin-bottom: 20px;
                }
                
                .form-container {
                    background: var(--bg-secondary);
                    border-radius: 8px;
                    padding: 30px;
                    border: 1px solid var(--border-light);
                }
                
                .form-title {
                    margin: 0 0 30px 0;
                    color: var(--text-primary);
                    text-align: center;
                }
                
                .form-group {
                    margin-bottom: 20px;
                }
                
                .form-group label {
                    display: block;
                    margin-bottom: 5px;
                    color: var(--text-primary);
                    font-weight: 500;
                }
                
                .checkbox-label {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    cursor: pointer;
                }
                
                .form-input {
                    width: 100%;
                    padding: 12px 15px;
                    border: 1px solid var(--border-medium);
                    border-radius: 6px;
                    background: var(--bg-primary);
                    color: var(--text-primary);
                    font-size: 14px;
                }
                
                .form-input:focus {
                    outline: none;
                    border-color: var(--primary);
                    box-shadow: 0 0 0 2px var(--primary-light);
                }
                
                .form-actions {
                    display: flex;
                    gap: 15px;
                    justify-content: center;
                    margin-top: 30px;
                }
                
                .alert {
                    padding: 12px 20px;
                    margin-bottom: 20px;
                    border-radius: 6px;
                    font-weight: 500;
                }
                
                .alert-error {
                    background: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                }
            """
            ),
            cls="add-user-page",
        ),
    )


# Route handlers for FastHTML app
async def users_route_handler(
    request, page: int = 1, size: int = 20, search: str = "", status: str = "all"
):
    """Main users page route handler"""
    # Get access token from cookie
    access_token = request.cookies.get("access_token")

    # Calculate skip for API
    skip = (page - 1) * size

    # Fetch users from API
    users_data = await fetch_users_from_api(
        skip=skip,
        limit=size,
        search=search if search else None,
        access_token=access_token,
    )

    # Filter by status if needed (since API doesn't support status filtering yet)
    if status != "all":
        users_data = [
            user
            for user in users_data
            if (status == "active" and user.get("is_active", True))
            or (status == "inactive" and not user.get("is_active", True))
        ]

    return users_page(
        users_data=users_data,
        current_page=page,
        page_size=size,
        search_term=search,
        status_filter=status,
    )


async def add_user_get_handler(
    request, page: int = 1, search: str = "", status: str = "all"
):
    """Add user form GET handler"""
    return add_user_form(page, search, status)


async def add_user_post_handler(request):
    """Add user form POST handler"""
    # Get form data
    form_data = await request.form()
    username = form_data.get("username", "").strip()
    email = form_data.get("email", "").strip()
    password = form_data.get("password", "")
    is_active = form_data.get("is_active") == "true"

    # Get return parameters
    page = int(form_data.get("page", 1))
    search = form_data.get("search", "")
    status = form_data.get("status", "all")

    # Validate
    if not username or not email or not password:
        return add_user_form(page, search, status, "All fields are required")

    if len(password) < 8:
        return add_user_form(
            page, search, status, "Password must be at least 8 characters long"
        )

    # Get access token
    access_token = request.cookies.get("access_token")
    if not access_token:
        return add_user_form(page, search, status, "Authentication required")

    # Create user
    result = await create_user_api(
        {
            "username": username,
            "email": email,
            "password": password,
            "is_active": is_active,
        },
        access_token,
    )

    if result["success"]:
        # Redirect back to users page with success message
        from fastapi.responses import RedirectResponse

        return RedirectResponse(
            url=f"/users?page={page}&search={search}&status={status}&success=User created successfully",
            status_code=303,
        )
    else:
        return add_user_form(page, search, status, result["error"])


async def delete_user_handler(
    request, user_id: int, page: int = 1, search: str = "", status: str = "all"
):
    """Delete user handler"""
    # Get access token
    access_token = request.cookies.get("access_token")
    if not access_token:
        from fastapi.responses import RedirectResponse

        return RedirectResponse(
            url=f"/users?page={page}&search={search}&status={status}&error=Authentication required",
            status_code=303,
        )

    # Delete user
    result = await delete_user_api(user_id, access_token)

    # Redirect back with message
    from fastapi.responses import RedirectResponse

    if result["success"]:
        return RedirectResponse(
            url=f"/users?page={page}&search={search}&status={status}&success=User deleted successfully",
            status_code=303,
        )
    else:
        return RedirectResponse(
            url=f"/users?page={page}&search={search}&status={status}&error={result['error']}",
            status_code=303,
        )
