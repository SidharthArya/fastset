from fasthtml.common import *
from styles.login import login_styles
from styles.base import base_styles
from frontend.components.theme_toggle import theme_toggle


def get_head(title=""):
    return Head(
        Title(f"FastSet {title}"),
        login_styles if title == "Login" else base_styles,
        nav_styles,
        Meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        Script(src="https://cdn.plot.ly/plotly-3.1.0.min.js", charset="utf-8"),
        Script(
            """
            function toggleSettingsDropdown() {
                const menu = document.getElementById('settings-menu');
                const overlay = document.getElementById('dropdown-overlay');
                
                if (menu.classList.contains('show')) {
                    menu.classList.remove('show');
                    if (overlay) overlay.classList.remove('show');
                } else {
                    menu.classList.add('show');
                    
                    // Create overlay if it doesn't exist
                    if (!overlay) {
                        const newOverlay = document.createElement('div');
                        newOverlay.id = 'dropdown-overlay';
                        newOverlay.className = 'dropdown-overlay show';
                        newOverlay.onclick = function() {
                            menu.classList.remove('show');
                            newOverlay.classList.remove('show');
                        };
                        document.body.appendChild(newOverlay);
                    } else {
                        overlay.classList.add('show');
                    }
                }
            }
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function(event) {
                const dropdown = document.querySelector('.dropdown');
                const menu = document.getElementById('settings-menu');
                
                if (dropdown && !dropdown.contains(event.target)) {
                    menu.classList.remove('show');
                    const overlay = document.getElementById('dropdown-overlay');
                    if (overlay) overlay.classList.remove('show');
                }
            });
        """
        ),
    )


inline_div_style = Style(".inline-div { display: inline-block; margin: 10px; }")

nav_styles = Style(
    """
.nav-menu {
    display: flex;
    gap: 20px;
    align-items: center;
    margin: 0 20px;
}
.nav-link {
    color: var(--text-primary);
    text-decoration: none;
    padding: 8px 16px;
    border-radius: 4px;
    transition: background-color 0.2s, color 0.2s;
}
.nav-link:hover {
    background-color: var(--primary-light);
    color: var(--primary);
}
.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

.dashboard-header {
    background: var(--bg-tertiary);
    padding: 15px 20px;
    border-bottom: 1px solid var(--border-light);
}
.theme-toggle {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    padding: 8px;
    border-radius: 4px;
    transition: background-color 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 40px;
    height: 40px;
}
.theme-toggle:hover {
    background-color: var(--primary-light);
}
.theme-toggle-container {
    display: flex;
    align-items: center;
}

/* Dropdown Styles */
.dropdown {
    position: relative;
    display: inline-block;
}

.dropdown-toggle {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 14px;
}

.dropdown-menu {
    display: none;
    position: absolute;
    top: 100%;
    right: 0;
    background: var(--bg-secondary);
    min-width: 200px;
    box-shadow: 0 4px 12px var(--shadow-medium);
    border-radius: 6px;
    border: 1px solid var(--border-medium);
    z-index: 1000;
    padding: 8px 0;
    margin-top: 4px;
}

.dropdown-menu.show {
    display: block;
}

.dropdown-item {
    display: block;
    padding: 8px 16px;
    color: var(--text-primary);
    text-decoration: none;
    font-size: 14px;
    transition: background-color 0.2s, color 0.2s;
}

.dropdown-item:hover {
    background-color: var(--bg-tertiary);
    color: var(--primary);
}

.dropdown-divider {
    height: 1px;
    background-color: var(--border-light);
    margin: 4px 0;
}

/* Close dropdown when clicking outside */
.dropdown-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 999;
    display: none;
}

.dropdown-overlay.show {
    display: block;
}

/* Logout Button Styles */
.logout-btn {
    background: var(--accent);
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
}

.logout-btn:hover {
    background: var(--accent-hover);
    transform: translateY(-1px);
    box-shadow: 0 2px 8px var(--shadow-light);
}

.logout-btn:active {
    transform: translateY(0);
}
"""
)


def get_header(name="Welcome"):
    return (
        Header(
            Div(
                Div(
                    H1(name, cls="text-primary"),
                    Nav(
                        A("Dashboards", href="/dashboard", cls="nav-link"),
                        A("Charts", href="/charts", cls="nav-link"),
                        A("Datasets", href="/datasets", cls="nav-link"),
                        A("SQL", href="/sql", cls="nav-link"),
                        Div(
                            Button(
                                "Settings ▼",
                                cls="nav-link dropdown-toggle",
                                id="settings-dropdown",
                                onclick="toggleSettingsDropdown()",
                            ),
                            Div(
                                A(
                                    "Security",
                                    href="/settings/security",
                                    cls="dropdown-item",
                                ),
                                A(
                                    "List Users",
                                    href="/settings/users",
                                    cls="dropdown-item",
                                ),
                                A(
                                    "List Tasks",
                                    href="/settings/tasks",
                                    cls="dropdown-item",
                                ),
                                A(
                                    "Audit Log",
                                    href="/settings/audit",
                                    cls="dropdown-item",
                                ),
                                A(
                                    "Row Level Security",
                                    href="/settings/rls",
                                    cls="dropdown-item",
                                ),
                                Div(cls="dropdown-divider"),
                                A(
                                    "Database Connections",
                                    href="/settings/database",
                                    cls="dropdown-item",
                                ),
                                A(
                                    "Manage",
                                    href="/settings/manage",
                                    cls="dropdown-item",
                                ),
                                A(
                                    "CSS Templates",
                                    href="/settings/css",
                                    cls="dropdown-item",
                                ),
                                A(
                                    "Alerts & Reports",
                                    href="/settings/alerts",
                                    cls="dropdown-item",
                                ),
                                A(
                                    "Annotation Layers",
                                    href="/settings/annotations",
                                    cls="dropdown-item",
                                ),
                                Div(cls="dropdown-divider"),
                                A("Help", href="/help", cls="dropdown-item"),
                                A("Profile", href="/profile", cls="dropdown-item"),
                                A("Info", href="/info", cls="dropdown-item"),
                                A("About", href="/about", cls="dropdown-item"),
                                cls="dropdown-menu",
                                id="settings-menu",
                            ),
                            cls="dropdown",
                        ),
                        cls="nav-menu",
                    ),
                    style="display: flex; align-items: center;",
                ),
                Div(
                    Form(
                        Button("Logout", type="submit", cls="logout-btn"),
                        method="post",
                        action="/logout",
                    ),
                    Div(
                        theme_toggle(),
                    ),
                    style="display: flex; align-items: center; gap: 10px;",
                ),
                cls="header-content",
            ),
            cls="dashboard-header",
        ),
    )
