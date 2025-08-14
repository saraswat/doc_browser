"""Main Streamlit application for the Document Browser."""

import streamlit as st
from components.selectors import render_document_selectors
from components.document_viewer import render_document


def main():
    """Main application function."""
    # Configure page
    st.set_page_config(
        page_title="Document Browser",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
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
    
    # Main layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Document selectors in sidebar
        selected_doc = render_document_selectors()
    
    with col2:
        if selected_doc:
            # Document viewer in main area
            render_document(selected_doc)
        else:
            st.info("👈 Please select a document name and date from the sidebar to view the document.")
            
            # Show some helpful information
            st.markdown("""
            ## Welcome to Document Browser
            
            This application allows you to browse AI-generated documents with the following features:
            
            - **📋 Document Selection**: Use the dropdowns to select documents by name and date
            - **🎨 Rich HTML Rendering**: View HTML documents with embedded styles, tables, and charts
            - **📄 PDF Support**: View and download PDF documents with metadata extraction
            - **📊 Metadata Display**: See document information and properties
            
            ### Getting Started
            1. Select a document name from the dropdown
            2. Choose a date for that document
            3. View the rendered document in the main panel
            
            ---
            *Ready to browse some documents? Start by selecting from the sidebar!*
            """)


if __name__ == "__main__":
    main()