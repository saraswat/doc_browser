"""Main Streamlit application for the Document Browser."""

import streamlit as st
from components.selectors import render_document_selectors
from components.document_viewer import render_document
from auth.oauth import is_authenticated, get_current_user
from auth.login_component import render_login_page, handle_oauth_redirect, render_user_info
from components.comments import render_user_comments_sidebar
from database.database import init_database


def main():
    """Main application function."""
    # Configure page
    st.set_page_config(
        page_title="Document Browser",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize database
    init_database()
    
    # Handle OAuth callback using modern Streamlit query params
    params = st.query_params
    
    # Check if this is an OAuth callback
    if 'code' in params and 'state' in params:
        st.title("🔄 Processing OAuth Login")
        
        code = params['code']
        state = params['state']
        
        # Process OAuth callback
        from auth.oauth import handle_oauth_callback, login_user
        
        try:
            user_info = handle_oauth_callback('google', code, state)
            if user_info:
                session_token = login_user(user_info)
                if session_token:
                    st.success("✅ Login successful!")
                    # Clear query parameters and redirect
                    st.query_params.clear()
                    st.rerun()
                else:
                    st.error("❌ Failed to create session")
            else:
                st.error("❌ OAuth processing failed")
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.write("**Debug Info:**")
            st.write(f"Code: {code[:20]}...")
            st.write(f"State: {state[:20]}...")
            
        return
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stSelectbox > div > div {
            background-color: #f0f2f6;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Check authentication
    if not is_authenticated():
        render_login_page()
        return
    
    # Get current user
    user = get_current_user()
    
    # Main layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # User info at top of sidebar
        st.sidebar.markdown("### 👤 User Profile")
        render_user_info(user)
        
        # Document selectors
        st.sidebar.markdown("### 📄 Browse Documents")
        selected_doc = render_document_selectors()
        
        # User comments sidebar
        render_user_comments_sidebar(user)
    
    with col2:
        if selected_doc:
            # Document viewer in main area
            render_document(selected_doc)
        else:
            st.info("👈 Please select a document name and date from the sidebar to view the document.")
            
            # Show some helpful information
            st.markdown(f"""
            ## Welcome to Document Browser, {user['name']}! 👋
            
            This application allows you to browse AI-generated documents with the following features:
            
            - **📋 Document Selection**: Use the dropdowns to select documents by name and date
            - **🎨 Rich HTML Rendering**: View HTML documents with embedded styles, tables, and charts
            - **📄 PDF Support**: View and download PDF documents with metadata extraction
            - **💬 Comments & Feedback**: Add comments and feedback to documents
            - **👥 User Authentication**: Secure OAuth-based login
            - **📊 Metadata Display**: See document information and properties
            
            ### Getting Started
            1. Select a document name from the dropdown
            2. Choose a date for that document
            3. View the rendered document in the main panel
            4. Add comments and feedback using the comment section
            
            ---
            *Ready to browse some documents? Start by selecting from the sidebar!*
            """)


if __name__ == "__main__":
    main()