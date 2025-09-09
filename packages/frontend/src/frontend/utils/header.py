from fasthtml.common import *
from frontend.styles.login import login_styles
from frontend.styles.base import base_styles
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
            
            function toggleMobileMenu() {
                const menu = document.getElementById('mobile-nav-menu');
                const overlay = document.getElementById('mobile-overlay');
                const hamburger = document.querySelector('.hamburger');
                
                if (menu.classList.contains('show')) {
                    menu.classList.remove('show');
                    if (overlay) overlay.classList.remove('show');
                    hamburger.classList.remove('active');
                } else {
                    menu.classList.add('show');
                    hamburger.classList.add('active');
                    
                    // Create overlay if it doesn't exist
                    if (!overlay) {
                        const newOverlay = document.createElement('div');
                        newOverlay.id = 'mobile-overlay';
                        newOverlay.className = 'mobile-overlay show';
                        newOverlay.onclick = function() {
                            menu.classList.remove('show');
                            newOverlay.classList.remove('show');
                            hamburger.classList.remove('active');
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
    white-space: nowrap;
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
    position: relative;
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

/* Hamburger Menu */
.hamburger {
    display: none;
    flex-direction: column;
    cursor: pointer;
    padding: 8px;
    border: none;
    background: none;
    gap: 3px;
}

.hamburger span {
    width: 25px;
    height: 3px;
    background: var(--text-primary);
    transition: all 0.3s ease;
    border-radius: 2px;
}

.hamburger.active span:nth-child(1) {
    transform: rotate(45deg) translate(6px, 6px);
}

.hamburger.active span:nth-child(2) {
    opacity: 0;
}

.hamburger.active span:nth-child(3) {
    transform: rotate(-45deg) translate(6px, -6px);
}

/* Mobile Navigation */
.mobile-nav-menu {
    display: none;
    position: fixed;
    top: 0;
    right: -300px;
    width: 280px;
    height: 100vh;
    background: var(--bg-secondary);
    border-left: 1px solid var(--border-light);
    z-index: 1001;
    transition: right 0.3s ease;
    overflow-y: auto;
    padding: 20px 0;
}

.mobile-nav-menu.show {
    right: 0;
}

.mobile-nav-header {
    padding: 0 20px 20px 20px;
    border-bottom: 1px solid var(--border-light);
    margin-bottom: 20px;
}

.mobile-nav-header h3 {
    margin: 0;
    color: var(--text-primary);
    font-size: 1.1rem;
}

.mobile-nav-section {
    margin-bottom: 20px;
}

.mobile-nav-section h4 {
    margin: 0 0 10px 0;
    padding: 0 20px;
    color: var(--text-secondary);
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.mobile-nav-link {
    display: block;
    padding: 12px 20px;
    color: var(--text-primary);
    text-decoration: none;
    transition: background-color 0.2s;
    border-left: 3px solid transparent;
}

.mobile-nav-link:hover {
    background-color: var(--bg-tertiary);
    border-left-color: var(--primary);
}

.mobile-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1000;
    display: none;
}

.mobile-overlay.show {
    display: block;
}

.mobile-actions {
    padding: 20px;
    border-top: 1px solid var(--border-light);
    margin-top: auto;
}

.mobile-actions .logout-btn {
    width: 100%;
    margin-bottom: 10px;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 20px;
}

.header-title {
    margin: 0;
    color: var(--text-primary);
    font-size: 1.5rem;
    font-weight: 600;
}

.header-right {
    display: flex;
    align-items: center;
    gap: 10px;
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

/* Responsive Design */
@media (max-width: 1024px) {
    .nav-menu {
        gap: 15px;
        margin: 0 15px;
    }
    
    .nav-link {
        padding: 6px 12px;
        font-size: 14px;
    }
    
    .dashboard-header {
        padding: 12px 15px;
    }
}

@media (max-width: 768px) {
    .nav-menu {
        display: none;
    }
    
    .hamburger {
        display: flex;
    }
    
    .mobile-nav-menu {
        display: block;
    }
    
    .dashboard-header {
        padding: 10px 15px;
    }
    
    .header-title {
        font-size: 1.25rem;
    }
    
    .logout-btn {
        padding: 6px 12px;
        font-size: 13px;
    }
    
    .theme-toggle {
        min-width: 35px;
        height: 35px;
        font-size: 18px;
    }
}

@media (max-width: 480px) {
    .dashboard-header {
        padding: 8px 10px;
    }
    
    .header-title {
        font-size: 1.1rem;
    }
    
    .header-right {
        gap: 5px;
    }
    
    .logout-btn {
        padding: 5px 10px;
        font-size: 12px;
    }
    
    .theme-toggle {
        min-width: 30px;
        height: 30px;
        font-size: 16px;
    }
    
    .mobile-nav-menu {
        width: 100%;
        right: -100%;
    }
}
"""
)


def get_header(name="Welcome"):
    return (
        Header(
            Div(
                Div(
                    H1(name, cls="header-title"),
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
                                    href="/users",
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
                    cls="header-left",
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
                    Button(
                        Span(),
                        Span(),
                        Span(),
                        cls="hamburger",
                        onclick="toggleMobileMenu()",
                    ),
                    cls="header-right",
                ),
                cls="header-content",
            ),
            # Mobile Navigation Menu
            Div(
                Div(H3("Navigation"), cls="mobile-nav-header"),
                Div(
                    H4("Main"),
                    A("Dashboards", href="/dashboard", cls="mobile-nav-link"),
                    A("Charts", href="/charts", cls="mobile-nav-link"),
                    A("Datasets", href="/datasets", cls="mobile-nav-link"),
                    A("SQL", href="/sql", cls="mobile-nav-link"),
                    cls="mobile-nav-section",
                ),
                Div(
                    H4("Settings"),
                    A("Security", href="/settings/security", cls="mobile-nav-link"),
                    A("List Users", href="/users", cls="mobile-nav-link"),
                    A("List Tasks", href="/settings/tasks", cls="mobile-nav-link"),
                    A("Audit Log", href="/settings/audit", cls="mobile-nav-link"),
                    A(
                        "Row Level Security",
                        href="/settings/rls",
                        cls="mobile-nav-link",
                    ),
                    A(
                        "Database Connections",
                        href="/settings/database",
                        cls="mobile-nav-link",
                    ),
                    A("Manage", href="/settings/manage", cls="mobile-nav-link"),
                    A("CSS Templates", href="/settings/css", cls="mobile-nav-link"),
                    A(
                        "Alerts & Reports",
                        href="/settings/alerts",
                        cls="mobile-nav-link",
                    ),
                    A(
                        "Annotation Layers",
                        href="/settings/annotations",
                        cls="mobile-nav-link",
                    ),
                    cls="mobile-nav-section",
                ),
                Div(
                    H4("Help"),
                    A("Help", href="/help", cls="mobile-nav-link"),
                    A("Profile", href="/profile", cls="mobile-nav-link"),
                    A("Info", href="/info", cls="mobile-nav-link"),
                    A("About", href="/about", cls="mobile-nav-link"),
                    cls="mobile-nav-section",
                ),
                Div(
                    Form(
                        Button("Logout", type="submit", cls="logout-btn"),
                        method="post",
                        action="/logout",
                    ),
                    cls="mobile-actions",
                ),
                id="mobile-nav-menu",
                cls="mobile-nav-menu",
            ),
            cls="dashboard-header",
        ),
    )
