"""Document selector components for the Streamlit application."""

import streamlit as st
from typing import Optional, Tuple
from utils.document_loader import load_document_list, get_available_documents
from components.comments import get_comment_statistics


def render_document_selectors() -> Optional[Tuple[str, str]]:
    """Render document name and date selectors."""
    st.header("📄 Document Browser")
    
    names, dates = load_document_list()
    
    if not names or not dates:
        st.warning("No documents found. Please add documents to the documents/content directory.")
        return None
    
    st.subheader("Select Document")
    
    # Name selector
    selected_name = st.selectbox(
        "Document Name:",
        options=[""] + names,
        index=0,
        key="document_name"
    )
    
    # Date selector - show all dates initially, filter by name if selected
    available_dates = dates
    if selected_name:
        filtered_docs = get_available_documents(name=selected_name)
        available_dates = sorted(list(set(doc["date"] for doc in filtered_docs)), reverse=True)
    
    selected_date = st.selectbox(
        "Document Date:",
        options=[""] + available_dates,
        index=0,
        key="document_date"
    )
    
    if selected_name and selected_date:
        # Show comment statistics for selected document
        try:
            stats = get_comment_statistics(selected_name, selected_date)
            if stats["total"] > 0:
                st.markdown(f"💬 **{stats['total']}** comment(s)")
                if stats["unresolved"] > 0:
                    st.markdown(f"⚠️ **{stats['unresolved']}** unresolved")
                if stats["resolved"] > 0:
                    st.markdown(f"✅ **{stats['resolved']}** resolved")
        except Exception:
            pass  # Ignore errors in comment statistics
        
        return selected_name, selected_date
    
    return None