"""SQL Query Interface Page"""

from fasthtml.common import *
from frontend.utils.header import get_head, get_header
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.express as px


def create_sample_dataframe():
    """Create a sample DataFrame for demonstration"""
    data = {
        "ID": [1, 2, 3, 4, 5],
        "Name": [
            "John Doe",
            "Jane Smith",
            "Bob Johnson",
            "Alice Brown",
            "Charlie Wilson",
        ],
        "Email": ["[email]", "[email]", "[email]", "[email]", "[email]"],
        "Age": [28, 34, 45, 29, 38],
        "Department": ["Engineering", "Marketing", "Sales", "Engineering", "HR"],
        "Salary": [75000, 68000, 82000, 71000, 65000],
        "Created": [
            "2024-01-15",
            "2024-01-16",
            "2024-01-10",
            "2024-01-20",
            "2024-01-12",
        ],
    }
    return pd.DataFrame(data)


def dataframe_to_plotly_table(df, max_rows=1000):
    """Convert pandas DataFrame to Plotly table"""
    if df.empty:
        return '<div class="no-data">No data to display</div>'

    # Limit rows for display
    display_df = df.head(max_rows)

    # Prepare data for Plotly table
    header_values = list(display_df.columns)
    cell_values = []

    for col in display_df.columns:
        # Format column values
        formatted_col = []
        for val in display_df[col]:
            if pd.isna(val):
                formatted_col.append("NULL")
            else:
                formatted_col.append(str(val))
        cell_values.append(formatted_col)

    # Create Plotly table
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=header_values,
                    fill_color="#007bff",
                    font=dict(color="white", size=14, family="Arial Black"),
                    align="left",
                    height=40,
                ),
                cells=dict(
                    values=cell_values,
                    fill_color=[["#f8f9fa", "#ffffff"] * len(display_df)],
                    font=dict(color="#333333", size=12),
                    align="left",
                    height=35,
                ),
            )
        ]
    )

    # Update layout
    fig.update_layout(
        title=dict(
            text=f"Query Results - {len(display_df)} of {len(df)} rows",
            font=dict(size=16, color="#333"),
            x=0,
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        height=min(600, 50 + len(display_df) * 35 + 40),  # Dynamic height
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    # Convert to HTML
    table_html = fig.to_html(
        include_plotlyjs="cdn",
        div_id="plotly-table",
        config={"displayModeBar": True, "displaylogo": False},
    )

    # Extract just the div content (remove full HTML structure)
    import re

    div_match = re.search(r'<div id="plotly-table".*?</script>', table_html, re.DOTALL)
    if div_match:
        return div_match.group(0)
    else:
        return table_html


def sql_page():
    """Create the SQL query interface page"""
    return Html(
        get_head("SQL"),
        Head(
            Script(src="https://cdn.plot.ly/plotly-latest.min.js")
        ),
        Body(
            get_header("SQL Query Interface"),
            Main(
                Div(
                    # Query Editor Section
                    Div(
                        H2("Query Editor", cls="section-title"),
                        Div(
                            Textarea(
                                placeholder="Enter your SQL query here...\n\nExample:\nSELECT * FROM users WHERE created_date > '2024-01-01'\nLIMIT 10;",
                                id="sql-editor",
                                cls="sql-editor",
                                rows="12",
                            ),
                            Div(
                                Button(
                                    "Run Query", id="run-query", cls="btn btn-primary"
                                ),
                                Button(
                                    "Clear", id="clear-query", cls="btn btn-secondary"
                                ),
                                Button(
                                    "Save Query", id="save-query", cls="btn btn-outline"
                                ),
                                cls="query-controls",
                            ),
                            cls="editor-container",
                        ),
                        cls="query-section",
                    ),
                    # Results Section
                    Div(
                        H2("Query Results", cls="section-title"),
                        Div(
                            Div(
                                "No query executed yet",
                                id="results-content",
                                cls="results-placeholder",
                            ),
                            cls="results-container",
                        ),
                        cls="results-section",
                    ),
                    cls="sql-main-content",
                ),
                # Sidebar with saved queries
                Aside(
                    H3("Saved Queries", cls="sidebar-title"),
                    Div(
                        Div(
                            H4("Recent Queries"),
                            Ul(
                                Li(
                                    A(
                                        "User Analytics",
                                        href="#",
                                        cls="query-link",
                                        **{
                                            "data-query": "SELECT COUNT(*) as total_users, AVG(age) as avg_age FROM users"
                                        },
                                    )
                                ),
                                Li(
                                    A(
                                        "Sales Report",
                                        href="#",
                                        cls="query-link",
                                        **{
                                            "data-query": "SELECT DATE(created_at) as date, SUM(amount) as daily_sales FROM orders GROUP BY DATE(created_at) ORDER BY date DESC LIMIT 30"
                                        },
                                    )
                                ),
                                Li(
                                    A(
                                        "Active Sessions",
                                        href="#",
                                        cls="query-link",
                                        **{
                                            "data-query": "SELECT user_id, session_start, session_end FROM user_sessions WHERE session_end IS NULL"
                                        },
                                    )
                                ),
                                cls="query-list",
                            ),
                            cls="query-group",
                        ),
                        Div(
                            H4("Templates"),
                            Ul(
                                Li(
                                    A(
                                        "Basic SELECT",
                                        href="#",
                                        cls="query-link",
                                        **{
                                            "data-query": "SELECT column1, column2 FROM table_name WHERE condition;"
                                        },
                                    )
                                ),
                                Li(
                                    A(
                                        "JOIN Query",
                                        href="#",
                                        cls="query-link",
                                        **{
                                            "data-query": "SELECT a.*, b.column FROM table_a a JOIN table_b b ON a.id = b.table_a_id;"
                                        },
                                    )
                                ),
                                Li(
                                    A(
                                        "Aggregation",
                                        href="#",
                                        cls="query-link",
                                        **{
                                            "data-query": "SELECT column, COUNT(*), AVG(numeric_column) FROM table_name GROUP BY column ORDER BY COUNT(*) DESC;"
                                        },
                                    )
                                ),
                                cls="query-list",
                            ),
                            cls="query-group",
                        ),
                        cls="saved-queries-content",
                    ),
                    cls="sidebar",
                ),
                cls="sql-container",
            ),
            # SQL Page Styles
            Style(
                """
                .sql-container {
                    display: flex;
                    gap: 20px;
                    padding: 20px;
                    max-width: 1400px;
                    margin: 0 auto;
                }
                
                .sql-main-content {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    gap: 20px;
                }
                
                .query-section, .results-section {
                    background: var(--card-bg, #ffffff);
                    border-radius: 8px;
                    padding: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                
                .section-title {
                    margin: 0 0 15px 0;
                    color: var(--text-primary, #333);
                    font-size: 1.25rem;
                    font-weight: 600;
                }
                
                .editor-container {
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                }
                
                .sql-editor {
                    width: 100%;
                    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                    font-size: 14px;
                    line-height: 1.5;
                    padding: 15px;
                    border: 1px solid var(--border-color, #ddd);
                    border-radius: 6px;
                    background: var(--input-bg, #fafafa);
                    resize: vertical;
                    min-height: 200px;
                }
                
                .sql-editor:focus {
                    outline: none;
                    border-color: var(--primary-color, #007bff);
                    box-shadow: 0 0 0 2px rgba(0,123,255,0.25);
                }
                
                .query-controls {
                    display: flex;
                    gap: 10px;
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
                }
                
                .btn-primary {
                    background: var(--primary-color, #007bff);
                    color: white;
                }
                
                .btn-primary:hover {
                    background: var(--primary-hover, #0056b3);
                }
                
                .btn-secondary {
                    background: var(--secondary-color, #6c757d);
                    color: white;
                }
                
                .btn-secondary:hover {
                    background: var(--secondary-hover, #545b62);
                }
                
                .btn-outline {
                    background: transparent;
                    color: var(--primary-color, #007bff);
                    border: 1px solid var(--primary-color, #007bff);
                }
                
                .btn-outline:hover {
                    background: var(--primary-color, #007bff);
                    color: white;
                }
                
                .results-container {
                    min-height: 300px;
                    border: 1px solid var(--border-color, #ddd);
                    border-radius: 6px;
                    padding: 15px;
                    background: var(--input-bg, #fafafa);
                }
                
                .results-placeholder {
                    color: var(--text-muted, #666);
                    text-align: center;
                    padding: 50px 20px;
                    font-style: italic;
                }
                
                .sidebar {
                    width: 300px;
                    background: var(--card-bg, #ffffff);
                    border-radius: 8px;
                    padding: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    height: fit-content;
                }
                
                .sidebar-title {
                    margin: 0 0 20px 0;
                    color: var(--text-primary, #333);
                    font-size: 1.1rem;
                    font-weight: 600;
                }
                
                .query-group {
                    margin-bottom: 25px;
                }
                
                .query-group h4 {
                    margin: 0 0 10px 0;
                    color: var(--text-secondary, #555);
                    font-size: 0.9rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }
                
                .query-list {
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }
                
                .query-list li {
                    margin-bottom: 8px;
                }
                
                .query-link {
                    display: block;
                    padding: 8px 12px;
                    color: var(--text-primary, #333);
                    text-decoration: none;
                    border-radius: 4px;
                    transition: background-color 0.2s;
                    font-size: 14px;
                }
                
                .query-link:hover {
                    background: var(--hover-bg, #f8f9fa);
                    color: var(--primary-color, #007bff);
                }
                
                /* Plotly table container styles */
                #plotly-table, #demo-plotly-table {
                    margin: 15px 0;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }
                
                /* Override Plotly default styles */
                .plotly .modebar {
                    background: rgba(255,255,255,0.9) !important;
                    border-radius: 4px !important;
                    padding: 4px !important;
                }
                
                .plotly .modebar-btn {
                    background: transparent !important;
                    border: none !important;
                    color: #666 !important;
                }
                
                .plotly .modebar-btn:hover {
                    background: rgba(0,123,255,0.1) !important;
                    color: #007bff !important;
                }
                
                .query-success {
                    background: #d4edda;
                    color: #155724;
                    padding: 10px 15px;
                    border-radius: 6px;
                    margin-bottom: 15px;
                    border: 1px solid #c3e6cb;
                    font-weight: 500;
                }
                
                .query-error {
                    background: #f8d7da;
                    color: #721c24;
                    padding: 15px;
                    border-radius: 6px;
                    margin-bottom: 15px;
                    border: 1px solid #f5c6cb;
                }
                
                .executed-query {
                    background: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 6px;
                    padding: 15px;
                    margin-bottom: 15px;
                }
                
                .executed-query pre {
                    margin: 5px 0 0 0;
                    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                    font-size: 13px;
                    line-height: 1.4;
                    color: #495057;
                }
                
                .query-stats {
                    display: flex;
                    gap: 20px;
                    margin-top: 15px;
                    padding: 10px 0;
                    border-top: 1px solid #eee;
                    font-size: 14px;
                }
                
                .stat-item {
                    color: var(--text-muted, #666);
                    font-weight: 500;
                }
                

                
                .no-data {
                    text-align: center;
                    padding: 40px 20px;
                    color: var(--text-muted, #666);
                    font-style: italic;
                }
                
                @media (max-width: 768px) {
                    .sql-container {
                        flex-direction: column;
                        padding: 10px;
                    }
                    
                    .sidebar {
                        width: 100%;
                        order: -1;
                    }
                    
                    .query-controls {
                        justify-content: center;
                    }
                    
                    #plotly-table, #demo-plotly-table {
                        margin: 10px 0;
                    }
                    
                    .query-stats {
                        flex-direction: column;
                        gap: 5px;
                    }
                }
            """
            ),
            # JavaScript for SQL functionality
            Script(
                """
                document.addEventListener('DOMContentLoaded', function() {
                    const editor = document.getElementById('sql-editor');
                    const runBtn = document.getElementById('run-query');
                    const clearBtn = document.getElementById('clear-query');
                    const saveBtn = document.getElementById('save-query');
                    const resultsContent = document.getElementById('results-content');
                    const queryLinks = document.querySelectorAll('.query-link');
                    
                    // Run query functionality
                    runBtn.addEventListener('click', function() {
                        const query = editor.value.trim();
                        if (!query) {
                            alert('Please enter a SQL query');
                            return;
                        }
                        
                        // Show loading state
                        resultsContent.innerHTML = '<div style="text-align: center; padding: 20px;">Executing query...</div>';
                        
                        // Simulate query execution with DataFrame results
                        fetch('/api/execute-sql', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ query: query })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                resultsContent.innerHTML = `
                                    <div class="query-success">Query executed successfully</div>
                                    <div class="executed-query">
                                        <strong>Executed Query:</strong>
                                        <pre>${query}</pre>
                                    </div>
                                    ${data.html_table}
                                    <div class="query-stats">
                                        <span class="stat-item">Rows: ${data.row_count}</span>
                                        <span class="stat-item">Columns: ${data.column_count}</span>
                                        <span class="stat-item">Execution Time: ${data.execution_time}s</span>
                                    </div>
                                `;
                            } else {
                                resultsContent.innerHTML = `
                                    <div class="query-error">
                                        <strong>Query Error:</strong>
                                        <pre>${data.error}</pre>
                                    </div>
                                `;
                            }
                        })
                        .catch(error => {
                            // Fallback to mock Plotly table for demo
                            setTimeout(() => {
                                resultsContent.innerHTML = `
                                    <div class="query-success">Query executed successfully (Demo Mode)</div>
                                    <div class="executed-query">
                                        <strong>Executed Query:</strong>
                                        <pre>${query}</pre>
                                    </div>
                                    <div id="demo-plotly-table" style="width: 100%; height: 400px;"></div>
                                    <div class="query-stats">
                                        <span class="stat-item">Rows: 5</span>
                                        <span class="stat-item">Columns: 7</span>
                                        <span class="stat-item">Execution Time: 0.045s</span>
                                    </div>
                                `;
                                
                                // Create demo Plotly table
                                const demoData = [{
                                    type: 'table',
                                    header: {
                                        values: ['ID', 'Name', 'Email', 'Age', 'Department', 'Salary', 'Created'],
                                        fill: {color: '#007bff'},
                                        font: {color: 'white', size: 14, family: 'Arial Black'},
                                        align: 'left',
                                        height: 40
                                    },
                                    cells: {
                                        values: [
                                            [1, 2, 3, 4, 5],
                                            ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
                                            ['[email]', '[email]', '[email]', '[email]', '[email]'],
                                            [28, 34, 45, 29, 38],
                                            ['Engineering', 'Marketing', 'Sales', 'Engineering', 'HR'],
                                            [75000, 68000, 82000, 71000, 65000],
                                            ['2024-01-15', '2024-01-16', '2024-01-10', '2024-01-20', '2024-01-12']
                                        ],
                                        fill: {color: [['#f8f9fa', '#ffffff']]},
                                        font: {color: '#333333', size: 12},
                                        align: 'left',
                                        height: 35
                                    }
                                }];
                                
                                const layout = {
                                    title: {
                                        text: 'Query Results - 5 of 5 rows',
                                        font: {size: 16, color: '#333'},
                                        x: 0
                                    },
                                    margin: {l: 0, r: 0, t: 50, b: 0},
                                    paper_bgcolor: 'rgba(0,0,0,0)',
                                    plot_bgcolor: 'rgba(0,0,0,0)'
                                };
                                
                                const config = {
                                    displayModeBar: true,
                                    displaylogo: false,
                                    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
                                };
                                
                                if (typeof Plotly !== 'undefined') {
                                    Plotly.newPlot('demo-plotly-table', demoData, layout, config);
                                } else {
                                    document.getElementById('demo-plotly-table').innerHTML = 
                                        '<div style="text-align: center; padding: 50px; color: #666;">Plotly not loaded. Please refresh the page.</div>';
                                }
                            }, 800);
                        });
                    });
                    
                    // Clear query functionality
                    clearBtn.addEventListener('click', function() {
                        editor.value = '';
                        editor.focus();
                    });
                    
                    // Save query functionality
                    saveBtn.addEventListener('click', function() {
                        const query = editor.value.trim();
                        if (!query) {
                            alert('Please enter a SQL query to save');
                            return;
                        }
                        
                        const name = prompt('Enter a name for this query:');
                        if (name) {
                            alert(`Query "${name}" saved successfully!`);
                            // Here you would typically save to backend
                        }
                    });
                    
                    // Load saved queries
                    queryLinks.forEach(link => {
                        link.addEventListener('click', function(e) {
                            e.preventDefault();
                            const query = this.getAttribute('data-query');
                            editor.value = query;
                            editor.focus();
                        });
                    });
                    
                    // Add syntax highlighting effect (basic)
                    editor.addEventListener('input', function() {
                        // This is a placeholder for syntax highlighting
                        // In a real app, you'd use a library like CodeMirror or Monaco Editor
                    });
                });
            """
            ),
            cls="sql-page",
        ),
    )


def execute_sql_api(query: str):
    """
    API endpoint to execute SQL queries and return DataFrame results
    This function should be added to your FastHTML routes
    """
    try:
        # For demo purposes, create sample data
        # In production, replace this with actual database connection
        sample_df = create_sample_dataframe()

        # Simulate query filtering (in production, execute actual SQL)
        if "WHERE" in query.upper():
            # Simple demo filtering
            result_df = sample_df.head(3)
        else:
            result_df = sample_df

        # Convert DataFrame to Plotly table
        html_table = dataframe_to_plotly_table(result_df)

        return {
            "success": True,
            "html_table": html_table,
            "row_count": len(result_df),
            "column_count": len(result_df.columns),
            "execution_time": "0.045",
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
