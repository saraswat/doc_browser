# Document Browser Application - Build Instructions

## Project Overview
Build a modern document browsing application using Python and Streamlit. Users can browse a collection of AI-generated documents (1-2 pages each) by selecting from dropdowns for "name" and "date". The application will support user authentication, document viewing, and feedback/markup capabilities.

## Technology Stack
- **Framework**: Streamlit (Python web framework)
- **Database**: SQLite (development) with SQLAlchemy ORM
- **Authentication**: streamlit-authenticator
- **Document Format**: Markdown with embedded tables/charts
- **Charts**: Plotly for interactive visualizations
- **Python Version**: 3.10+

## Core Requirements

### Phase 1: Basic Document Browser (Start Here)
1. Create a Streamlit application with a clean, modern UI
2. Implement two dropdown selectors:
   - Name dropdown (list of available document names)
   - Date dropdown (list of available dates)
3. Main display panel showing the selected document
4. Documents stored as HTML files with metadata
5. Support for rendering:
   - Formatted HTML content
   - Tables (HTML tables)
   - Charts (embedded in HTML or using Plotly)

### Phase 2: User Authentication
1. Add user login/registration system using streamlit-authenticator
2. Session management to track logged-in users
3. User profile storage in SQLite database

### Phase 3: Document Feedback System
1. Allow authenticated users to add feedback/markup to documents
2. Store feedback linked to user ID, document name, and date
3. Display user's previous feedback when revisiting documents
4. Feedback should be non-destructive (overlays on original document)

## Project Structure
```
document_browser/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── database/
│   ├── __init__.py
│   ├── models.py              # SQLAlchemy models
│   └── database.db            # SQLite database (auto-generated)
├── auth/
│   ├── __init__.py
│   └── authenticator.py       # Authentication logic
├── components/
│   ├── __init__.py
│   ├── document_viewer.py     # Document display component
│   ├── selectors.py           # Dropdown components
│   └── feedback.py            # Feedback/markup component
├── documents/
│   ├── metadata.json          # Document metadata registry
│   └── content/               # HTML files for documents
│       └── {name}_{date}.html # Individual document files
└── utils/
    ├── __init__.py
    ├── document_loader.py     # Document loading utilities
    └── chart_generator.py     # Plotly chart utilities
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### Documents Table
```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    date DATE NOT NULL,
    file_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, date)
);
```

### Feedback Table
```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    document_id INTEGER NOT NULL,
    feedback_text TEXT,
    markup_data JSON,  -- Store annotations as JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (document_id) REFERENCES documents(id)
);
```

## Implementation Guidelines

### Document Format
Documents are HTML files that can include embedded styles and scripts. Example structure:
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="document-name" content="Document Name">
    <meta name="document-date" content="2024-01-15">
    <meta name="author" content="AI System">
    <meta name="version" content="1.0">
    <style>
        /* Document-specific styles */
        body { font-family: Arial, sans-serif; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; }
    </style>
</head>
<body>
    <h1>Document Title</h1>
    
    <p>Content here with <strong>formatting</strong>, tables, and charts...</p>
    
    <table>
        <tr><th>Header 1</th><th>Header 2</th></tr>
        <tr><td>Data 1</td><td>Data 2</td></tr>
    </table>
    
    <!-- Charts can be embedded as HTML/JS or referenced -->
    <div id="chart-container"></div>
</body>
</html>
```

### Rendering HTML in Streamlit
```python
import streamlit as st
import streamlit.components.v1 as components

# For trusted HTML content (your AI-generated docs)
components.html(html_content, height=600, scrolling=True)

# Alternative: Using iframe for better isolation
st.markdown(f'<iframe srcdoc="{html_content}" width="100%" height="600"></iframe>', 
            unsafe_allow_html=True)
```

### Streamlit Page Configuration
```python
st.set_page_config(
    page_title="Document Browser",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### Key Features to Implement

1. **Responsive Layout**:
   - Use `st.columns()` for side-by-side layouts
   - Sidebar for navigation/filters
   - Main area for document display

2. **Document Rendering**:
   - Use `components.html()` for rendering HTML documents
   - Preserve embedded styles and scripts
   - Handle responsive sizing with height parameter
   - Consider iframe isolation for security
   - Extract metadata from HTML meta tags

3. **Session State Management**:
   - Track current user
   - Remember selected document
   - Store temporary feedback before saving

4. **Caching**:
   - Use `@st.cache_data` for document loading
   - Cache database queries where appropriate

## Sample Code Structure for app.py

```python
import streamlit as st
import streamlit.components.v1 as components
from auth.authenticator import login_user, logout_user, get_current_user
from components.selectors import render_document_selectors
from components.document_viewer import render_html_document
from components.feedback import render_feedback_panel
from utils.document_loader import load_document_list, load_html_document

def main():
    st.set_page_config(page_title="Document Browser", layout="wide")
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Authentication
    if not st.session_state.authenticated:
        login_user()
    else:
        # Main app layout
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Document selectors
            selected_doc = render_document_selectors()
            
            # User info and logout
            user = get_current_user()
            st.write(f"Logged in as: {user['username']}")
            if st.button("Logout"):
                logout_user()
        
        with col2:
            # Document viewer
            if selected_doc:
                render_html_document(selected_doc)
                render_feedback_panel(selected_doc, user)

if __name__ == "__main__":
    main()
```

## Dependencies (requirements.txt)
```
streamlit>=1.32.0
sqlalchemy>=2.0.0
streamlit-authenticator>=0.3.0
beautifulsoup4>=4.12.0
lxml>=5.0.0
plotly>=5.18.0
pandas>=2.2.0
python-dateutil>=2.8.0
bcrypt>=4.1.0
pyyaml>=6.0
```

## Development Steps

1. **Initial Setup**:
   - Create project directory structure
   - Initialize git repository
   - Create virtual environment
   - Install dependencies

2. **Phase 1 Implementation**:
   - Build basic Streamlit app with dropdowns
   - Create sample HTML documents with tables and styling
   - Implement HTML document loading and display
   - Test embedded charts and styles
   - Handle HTML metadata extraction

3. **Phase 2 Implementation**:
   - Set up SQLAlchemy models
   - Implement user registration/login
   - Add session management
   - Secure document access

4. **Phase 3 Implementation**:
   - Create feedback UI components
   - Implement feedback storage
   - Add feedback retrieval and display
   - Test multi-user scenarios

## Testing Approach
- Create sample documents with various content types
- Test with multiple concurrent users
- Verify feedback persistence
- Check responsive design on different screen sizes

## Deployment Considerations
- Use environment variables for sensitive configuration
- Consider migrating to PostgreSQL for production
- Implement proper logging
- Add error handling and user-friendly error messages
- Set up backup strategy for database and documents

## Extension Points
The architecture supports future additions:
- Document search functionality
- User permissions and document access control
- Document versioning
- Export functionality (PDF, etc.)
- Real-time collaboration features
- Analytics dashboard
- Document templates
- AI-powered document generation interface

## Notes for Claude for Code
- Start with Phase 1 and get basic functionality working before moving to authentication
- Use BeautifulSoup for HTML parsing and metadata extraction
- Implement HTML rendering using `components.html()` for full style preservation
- Consider security when rendering HTML (use iframe isolation if needed)
- Add comprehensive docstrings to all functions
- Implement proper error handling from the start
- Use type hints for better code clarity
- Follow PEP 8 style guidelines
- Create modular, reusable components
- Prioritize user experience with loading states and clear feedback

## Success Criteria
- Users can browse HTML documents using intuitive dropdowns
- HTML documents render correctly with preserved styling, tables, and charts
- Authentication system is secure and user-friendly
- Feedback is properly stored and retrieved per user
- Application performs well with dozens of concurrent users
- Code is clean, documented, and easily extensible

## Additional Implementation Notes

### HTML Document Handling
```python
from bs4 import BeautifulSoup
import streamlit.components.v1 as components

def load_and_render_html_document(filepath):
    """Load and render an HTML document with metadata extraction."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extract metadata from HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    metadata = {}
    for meta in soup.find_all('meta'):
        if meta.get('name', '').startswith('document-'):
            metadata[meta.get('name')] = meta.get('content')
    
    # Render HTML in Streamlit
    components.html(html_content, height=800, scrolling=True)
    
    return metadata

def sanitize_html_for_feedback(html_content):
    """Prepare HTML for feedback overlay system."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Add unique IDs to paragraphs, tables, etc. for feedback anchoring
    for i, elem in enumerate(soup.find_all(['p', 'table', 'h1', 'h2', 'h3'])):
        if not elem.get('id'):
            elem['id'] = f'doc-element-{i}'
    
    return str(soup)
```

### Feedback Overlay Strategy
Since documents are HTML, feedback can be implemented as:
1. **HTML annotations**: Inject feedback as HTML elements with special styling
2. **JavaScript overlay**: Add interactive feedback layer using JS
3. **Side panel**: Display feedback in a separate panel linked to document sections

### Security Considerations
- Sanitize any user-provided HTML content
- Use iframe isolation for untrusted content
- Consider Content Security Policy (CSP) headers
- Validate all HTML documents before rendering
