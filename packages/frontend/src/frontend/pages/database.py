"""Database Connections Management Page - Superset-like Interface"""

from fasthtml.common import *
from frontend.utils.header import get_head, get_header


def create_database_card(db_name, db_type, status, last_connected, description=""):
    """Create a database connection card"""
    status_color = "#28a745" if status == "Connected" else "#dc3545"
    status_icon = "●" if status == "Connected" else "●"
    
    return Div(
        Div(
            Div(
                Div(
                    H4(db_name, cls="db-card-title"),
                    Span(db_type, cls="db-type-badge"),
                    cls="db-card-header"
                ),
                P(description or f"{db_type} database connection", cls="db-card-description"),
                Div(
                    Span(
                        status_icon,
                        style=f"color: {status_color}; margin-right: 5px;"
                    ),
                    Span(status, cls="status-text"),
                    Span(f"Last connected: {last_connected}", cls="last-connected"),
                    cls="db-status"
                ),
                cls="db-card-content"
            ),
            Div(
                Button("Test Connection", cls="btn btn-outline btn-sm", onclick=f"testConnection('{db_name}')"),
                Button("Edit", cls="btn btn-primary btn-sm", onclick=f"editDatabase('{db_name}')"),
                Button("Delete", cls="btn btn-danger btn-sm", onclick=f"deleteDatabase('{db_name}')"),
                cls="db-card-actions"
            ),
            cls="database-card"
        ),
        cls="database-card-wrapper"
    )


def database_page():
    """Create the database connections management page"""
    return Html(
        get_head("Database Connections"),
        Body(
            get_header("Database Connections"),
            Main(
                # Page Header with Actions
                Div(
                    Div(
                        H1("Database Connections", cls="page-title"),
                        P("Manage your database connections and data sources", cls="page-subtitle"),
                        cls="page-header-content"
                    ),
                    Div(
                        Button(
                            "+ Add Database",
                            cls="btn btn-primary",
                            onclick="showAddDatabaseModal()"
                        ),
                        Button(
                            "Import",
                            cls="btn btn-outline",
                            onclick="showImportModal()"
                        ),
                        Button(
                            "Refresh All",
                            cls="btn btn-secondary",
                            onclick="refreshAllConnections()"
                        ),
                        cls="page-actions"
                    ),
                    cls="page-header"
                ),
                
                # Filter and Search Bar
                Div(
                    Div(
                        Input(
                            type="text",
                            placeholder="Search databases...",
                            cls="search-input",
                            id="database-search",
                            oninput="filterDatabases()"
                        ),
                        Select(
                            Option("All Types", value="all"),
                            Option("PostgreSQL", value="postgresql"),
                            Option("MySQL", value="mysql"),
                            Option("SQLite", value="sqlite"),
                            Option("MongoDB", value="mongodb"),
                            Option("Redis", value="redis"),
                            cls="filter-select",
                            id="type-filter",
                            onchange="filterDatabases()"
                        ),
                        Select(
                            Option("All Status", value="all"),
                            Option("Connected", value="connected"),
                            Option("Disconnected", value="disconnected"),
                            cls="filter-select",
                            id="status-filter",
                            onchange="filterDatabases()"
                        ),
                        cls="filters"
                    ),
                    cls="filter-bar"
                ),
                
                # Database Cards Grid
                Div(
                    # Sample database connections
                    create_database_card(
                        "Production PostgreSQL",
                        "PostgreSQL",
                        "Connected",
                        "2 minutes ago",
                        "Main production database with user data and transactions"
                    ),
                    create_database_card(
                        "Analytics Warehouse",
                        "PostgreSQL",
                        "Connected",
                        "5 minutes ago",
                        "Data warehouse for analytics and reporting"
                    ),
                    create_database_card(
                        "User Cache",
                        "Redis",
                        "Connected",
                        "1 minute ago",
                        "Redis cache for user sessions and temporary data"
                    ),
                    create_database_card(
                        "Legacy MySQL",
                        "MySQL",
                        "Disconnected",
                        "2 hours ago",
                        "Legacy MySQL database - migration in progress"
                    ),
                    create_database_card(
                        "Document Store",
                        "MongoDB",
                        "Connected",
                        "10 minutes ago",
                        "MongoDB for document storage and content management"
                    ),
                    create_database_card(
                        "Development DB",
                        "SQLite",
                        "Connected",
                        "30 seconds ago",
                        "Local development database for testing"
                    ),
                    cls="databases-grid",
                    id="databases-container"
                ),
                
                # Add Database Modal
                Div(
                    Div(
                        Div(
                            H3("Add Database Connection"),
                            Button("×", cls="modal-close", onclick="hideAddDatabaseModal()"),
                            cls="modal-header"
                        ),
                        Div(
                            Form(
                                Div(
                                    Label("Database Name", **{"for": "db-name"}),
                                    Input(type="text", id="db-name", cls="form-input", placeholder="Enter database name"),
                                    cls="form-group"
                                ),
                                Div(
                                    Label("Database Type", **{"for": "db-type"}),
                                    Select(
                                        Option("Select database type", value="", selected=True),
                                        Option("PostgreSQL", value="postgresql"),
                                        Option("MySQL", value="mysql"),
                                        Option("SQLite", value="sqlite"),
                                        Option("MongoDB", value="mongodb"),
                                        Option("Redis", value="redis"),
                                        Option("Oracle", value="oracle"),
                                        Option("SQL Server", value="sqlserver"),
                                        id="db-type",
                                        cls="form-select"
                                    ),
                                    cls="form-group"
                                ),
                                Div(
                                    Label("Host", **{"for": "db-host"}),
                                    Input(type="text", id="db-host", cls="form-input", placeholder="localhost"),
                                    cls="form-group"
                                ),
                                Div(
                                    Label("Port", **{"for": "db-port"}),
                                    Input(type="number", id="db-port", cls="form-input", placeholder="5432"),
                                    cls="form-group"
                                ),
                                Div(
                                    Label("Database Name", **{"for": "db-database"}),
                                    Input(type="text", id="db-database", cls="form-input", placeholder="database_name"),
                                    cls="form-group"
                                ),
                                Div(
                                    Label("Username", **{"for": "db-username"}),
                                    Input(type="text", id="db-username", cls="form-input", placeholder="username"),
                                    cls="form-group"
                                ),
                                Div(
                                    Label("Password", **{"for": "db-password"}),
                                    Input(type="password", id="db-password", cls="form-input", placeholder="password"),
                                    cls="form-group"
                                ),
                                Div(
                                    Label("Description (Optional)", **{"for": "db-description"}),
                                    Textarea(id="db-description", cls="form-textarea", placeholder="Enter description", rows="3"),
                                    cls="form-group"
                                ),
                                cls="modal-form"
                            ),
                            cls="modal-body"
                        ),
                        Div(
                            Button("Test Connection", cls="btn btn-outline", onclick="testNewConnection()"),
                            Button("Cancel", cls="btn btn-secondary", onclick="hideAddDatabaseModal()"),
                            Button("Add Database", cls="btn btn-primary", onclick="addDatabase()"),
                            cls="modal-footer"
                        ),
                        cls="modal-content"
                    ),
                    cls="modal-overlay",
                    id="add-database-modal",
                    style="display: none;",
                    onclick="event.target === this && hideAddDatabaseModal()"
                ),
                
                cls="database-page-container"
            ),
            
            # Styles
            Style("""
                .database-page-container {
                    max-width: 1400px;
                    margin: 0 auto;
                    padding: 20px;
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
                
                .filter-select {
                    padding: 10px 15px;
                    border: 1px solid var(--border-medium);
                    border-radius: 6px;
                    background: var(--bg-primary);
                    color: var(--text-primary);
                    font-size: 14px;
                    min-width: 150px;
                }
                
                .databases-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
                    gap: 20px;
                }
                
                .database-card {
                    background: var(--bg-secondary);
                    border: 1px solid var(--border-light);
                    border-radius: 8px;
                    padding: 20px;
                    transition: all 0.2s ease;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    min-height: 180px;
                }
                
                .database-card:hover {
                    border-color: var(--primary);
                    box-shadow: 0 4px 12px var(--shadow-light);
                    transform: translateY(-2px);
                }
                
                .db-card-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    margin-bottom: 10px;
                }
                
                .db-card-title {
                    margin: 0;
                    color: var(--text-primary);
                    font-size: 1.1rem;
                    font-weight: 600;
                }
                
                .db-type-badge {
                    background: var(--primary-light);
                    color: var(--primary);
                    padding: 4px 8px;
                    border-radius: 4px;
                    font-size: 12px;
                    font-weight: 500;
                }
                
                .db-card-description {
                    color: var(--text-secondary);
                    font-size: 14px;
                    margin: 0 0 15px 0;
                    line-height: 1.4;
                }
                
                .db-status {
                    display: flex;
                    flex-direction: column;
                    gap: 5px;
                    margin-bottom: 15px;
                }
                
                .status-text {
                    font-weight: 500;
                    font-size: 14px;
                }
                
                .last-connected {
                    color: var(--text-muted);
                    font-size: 12px;
                }
                
                .db-card-actions {
                    display: flex;
                    gap: 8px;
                    flex-wrap: wrap;
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
                
                .btn-sm {
                    padding: 6px 12px;
                    font-size: 13px;
                }
                
                .btn-primary {
                    background: var(--primary);
                    color: white;
                }
                
                .btn-primary:hover {
                    background: var(--primary-hover);
                }
                
                .btn-secondary {
                    background: var(--bg-tertiary);
                    color: var(--text-primary);
                    border: 1px solid var(--border-medium);
                }
                
                .btn-secondary:hover {
                    background: var(--border-light);
                }
                
                .btn-outline {
                    background: transparent;
                    color: var(--primary);
                    border: 1px solid var(--primary);
                }
                
                .btn-outline:hover {
                    background: var(--primary);
                    color: white;
                }
                
                .btn-danger {
                    background: #dc3545;
                    color: white;
                }
                
                .btn-danger:hover {
                    background: #c82333;
                }
                
                /* Modal Styles */
                .modal-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.5);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 1000;
                }
                
                .modal-content {
                    background: var(--bg-primary);
                    border-radius: 8px;
                    width: 90%;
                    max-width: 600px;
                    max-height: 90vh;
                    overflow-y: auto;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                }
                
                .modal-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 20px;
                    border-bottom: 1px solid var(--border-light);
                }
                
                .modal-header h3 {
                    margin: 0;
                    color: var(--text-primary);
                }
                
                .modal-close {
                    background: none;
                    border: none;
                    font-size: 24px;
                    cursor: pointer;
                    color: var(--text-muted);
                    padding: 0;
                    width: 30px;
                    height: 30px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                
                .modal-body {
                    padding: 20px;
                }
                
                .modal-footer {
                    display: flex;
                    justify-content: flex-end;
                    gap: 10px;
                    padding: 20px;
                    border-top: 1px solid var(--border-light);
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
                
                .form-input, .form-select, .form-textarea {
                    width: 100%;
                    padding: 10px 12px;
                    border: 1px solid var(--border-medium);
                    border-radius: 6px;
                    background: var(--bg-primary);
                    color: var(--text-primary);
                    font-size: 14px;
                }
                
                .form-input:focus, .form-select:focus, .form-textarea:focus {
                    outline: none;
                    border-color: var(--primary);
                    box-shadow: 0 0 0 2px var(--primary-light);
                }
                
                .form-textarea {
                    resize: vertical;
                    min-height: 80px;
                }
                
                @media (max-width: 768px) {
                    .database-page-container {
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
                    
                    .databases-grid {
                        grid-template-columns: 1fr;
                    }
                    
                    .filters {
                        flex-direction: column;
                        align-items: stretch;
                    }
                    
                    .search-input, .filter-select {
                        min-width: auto;
                        width: 100%;
                    }
                }
            """),
            
            # JavaScript
            Script("""
                function showAddDatabaseModal() {
                    document.getElementById('add-database-modal').style.display = 'flex';
                }
                
                function hideAddDatabaseModal() {
                    document.getElementById('add-database-modal').style.display = 'none';
                    // Reset form
                    document.querySelector('.modal-form').reset();
                }
                
                function testConnection(dbName) {
                    alert(`Testing connection to ${dbName}...`);
                    // Here you would make an API call to test the connection
                }
                
                function editDatabase(dbName) {
                    alert(`Editing ${dbName}...`);
                    // Here you would open edit modal with pre-filled data
                }
                
                function deleteDatabase(dbName) {
                    if (confirm(`Are you sure you want to delete ${dbName}?`)) {
                        alert(`Deleting ${dbName}...`);
                        // Here you would make an API call to delete the database
                    }
                }
                
                function testNewConnection() {
                    const dbType = document.getElementById('db-type').value;
                    const host = document.getElementById('db-host').value;
                    const port = document.getElementById('db-port').value;
                    
                    if (!dbType || !host) {
                        alert('Please fill in database type and host');
                        return;
                    }
                    
                    alert('Testing connection...');
                    // Here you would make an API call to test the new connection
                }
                
                function addDatabase() {
                    const name = document.getElementById('db-name').value;
                    const type = document.getElementById('db-type').value;
                    
                    if (!name || !type) {
                        alert('Please fill in required fields');
                        return;
                    }
                    
                    alert(`Adding database ${name}...`);
                    hideAddDatabaseModal();
                    // Here you would make an API call to add the database
                }
                
                function refreshAllConnections() {
                    alert('Refreshing all connections...');
                    // Here you would make API calls to refresh all database connections
                }
                
                function filterDatabases() {
                    const searchTerm = document.getElementById('database-search').value.toLowerCase();
                    const typeFilter = document.getElementById('type-filter').value;
                    const statusFilter = document.getElementById('status-filter').value;
                    
                    const cards = document.querySelectorAll('.database-card-wrapper');
                    
                    cards.forEach(card => {
                        const title = card.querySelector('.db-card-title').textContent.toLowerCase();
                        const type = card.querySelector('.db-type-badge').textContent.toLowerCase();
                        const status = card.querySelector('.status-text').textContent.toLowerCase();
                        
                        const matchesSearch = title.includes(searchTerm);
                        const matchesType = typeFilter === 'all' || type === typeFilter;
                        const matchesStatus = statusFilter === 'all' || 
                            (statusFilter === 'connected' && status === 'connected') ||
                            (statusFilter === 'disconnected' && status === 'disconnected');
                        
                        if (matchesSearch && matchesType && matchesStatus) {
                            card.style.display = 'block';
                        } else {
                            card.style.display = 'none';
                        }
                    });
                }
                
                function showImportModal() {
                    alert('Import functionality coming soon...');
                }
            """),
            
            cls="database-page"
        )
    )