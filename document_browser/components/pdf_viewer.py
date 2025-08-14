"""PDF viewer component for rendering PDF documents."""

import streamlit as st
import base64
from typing import Tuple
from utils.document_loader import load_pdf_document, extract_pdf_metadata


def render_pdf_document(selected_doc: Tuple[str, str]) -> None:
    """Render a PDF document in the Streamlit app."""
    name, date = selected_doc
    
    st.subheader(f"📄 {name} - {date}")
    
    pdf_content = load_pdf_document(name, date)
    
    if not pdf_content:
        st.error(f"Could not load PDF document: {name} ({date})")
        return
    
    # Extract and display metadata
    metadata = extract_pdf_metadata(pdf_content)
    
    if metadata:
        with st.expander("📋 Document Information"):
            for key, value in metadata.items():
                if value:
                    display_key = key.replace('_', ' ').title()
                    st.write(f"**{display_key}:** {value}")
    
    # Display PDF using base64 embedding
    st.markdown("---")
    
    try:
        # Convert PDF to base64
        base64_pdf = base64.b64encode(pdf_content).decode('utf-8')
        
        # Create PDF viewer HTML
        pdf_display = f"""
            <iframe src="data:application/pdf;base64,{base64_pdf}" 
                    width="100%" 
                    height="800" 
                    type="application/pdf">
                <p>Your browser does not support PDFs. 
                   <a href="data:application/pdf;base64,{base64_pdf}">Download the PDF</a>
                </p>
            </iframe>
        """
        
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        # Alternative: Provide download link
        st.markdown("---")
        st.download_button(
            label="📥 Download PDF",
            data=pdf_content,
            file_name=f"{name}_{date}.pdf",
            mime="application/pdf"
        )
        
    except Exception as e:
        st.error(f"Error rendering PDF: {str(e)}")
        
        # Fallback: show download option only
        st.warning("⚠️ PDF preview not available. Use download button below.")
        st.download_button(
            label="📥 Download PDF",
            data=pdf_content,
            file_name=f"{name}_{date}.pdf",
            mime="application/pdf"
        )