"""Document viewer component for rendering HTML and PDF documents."""

import streamlit as st
import streamlit.components.v1 as components
from typing import Tuple
from utils.document_loader import (
    load_html_document, extract_html_metadata, 
    get_document_type
)
from components.pdf_viewer import render_pdf_document
from components.comments import render_comment_section, get_comment_statistics


def render_document(selected_doc: Tuple[str, str]) -> None:
    """Render a document (HTML or PDF) based on its type."""
    name, date = selected_doc
    doc_type = get_document_type(name, date)
    
    if doc_type == "html":
        render_html_document(selected_doc)
    elif doc_type == "pdf":
        render_pdf_document(selected_doc)
    else:
        st.error(f"Document not found: {name} ({date})")
        return
    
    # Add comment section for all document types
    render_comment_section(name, date, doc_type)


def render_html_document(selected_doc: Tuple[str, str]) -> None:
    """Render an HTML document in the Streamlit app."""
    name, date = selected_doc
    
    st.subheader(f"📖 {name} - {date}")
    
    html_content = load_html_document(name, date)
    
    if not html_content:
        st.error(f"Could not load document: {name} ({date})")
        return
    
    # Extract and display metadata
    metadata = extract_html_metadata(html_content)
    
    if metadata:
        with st.expander("📋 Document Information"):
            for key, value in metadata.items():
                if value:
                    display_key = key.replace('document-', '').replace('_', ' ').title()
                    st.write(f"**{display_key}:** {value}")
    
    # Render the HTML document
    st.markdown("---")
    
    try:
        # Use components.html for full HTML rendering with styles and scripts
        components.html(
            html_content,
            height=800,
            scrolling=True
        )
    except Exception as e:
        st.error(f"Error rendering document: {str(e)}")
        
        # Fallback: show raw HTML (less ideal but still functional)
        with st.expander("⚠️ Raw HTML Content (Fallback)"):
            st.code(html_content, language="html")