"""Document loading utilities for the document browser application."""

import os
import json
import base64
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
from bs4 import BeautifulSoup
import streamlit as st
import PyPDF2


@st.cache_data
def load_document_metadata() -> Dict:
    """Load document metadata from metadata.json file."""
    metadata_path = Path(__file__).parent.parent / "documents" / "metadata.json"
    
    if not metadata_path.exists():
        return {"documents": []}
    
    try:
        with open(metadata_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"documents": []}


@st.cache_data
def load_document_list() -> Tuple[List[str], List[str]]:
    """Load available document names and dates."""
    metadata = load_document_metadata()
    documents = metadata.get("documents", [])
    
    names = sorted(list(set(doc["name"] for doc in documents)))
    dates = sorted(list(set(doc["date"] for doc in documents)), reverse=True)
    
    return names, dates


@st.cache_data
def load_document_content(name: str, date: str) -> Optional[Union[str, bytes]]:
    """Load document content by name and date - supports both HTML and PDF."""
    documents_dir = Path(__file__).parent.parent / "documents" / "content"
    
    # Try HTML first
    html_filename = f"{name}_{date}.html"
    html_filepath = documents_dir / html_filename
    
    if html_filepath.exists():
        try:
            with open(html_filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError:
            pass
    
    # Try PDF
    pdf_filename = f"{name}_{date}.pdf"
    pdf_filepath = documents_dir / pdf_filename
    
    if pdf_filepath.exists():
        try:
            with open(pdf_filepath, 'rb') as f:
                return f.read()
        except IOError:
            pass
    
    return None

@st.cache_data
def load_html_document(name: str, date: str) -> Optional[str]:
    """Load HTML document content by name and date."""
    content = load_document_content(name, date)
    if content and isinstance(content, str):
        return content
    return None

@st.cache_data
def load_pdf_document(name: str, date: str) -> Optional[bytes]:
    """Load PDF document content by name and date."""
    content = load_document_content(name, date)
    if content and isinstance(content, bytes):
        return content
    return None


def extract_html_metadata(html_content: str) -> Dict[str, str]:
    """Extract metadata from HTML document."""
    soup = BeautifulSoup(html_content, 'html.parser')
    metadata = {}
    
    for meta in soup.find_all('meta'):
        name = meta.get('name', '')
        if name.startswith('document-'):
            metadata[name] = meta.get('content', '')
    
    # Also extract title
    title_tag = soup.find('title')
    if title_tag:
        metadata['title'] = title_tag.get_text().strip()
    
    return metadata


def extract_pdf_metadata(pdf_content: bytes) -> Dict[str, str]:
    """Extract metadata from PDF document."""
    try:
        from io import BytesIO
        pdf_file = BytesIO(pdf_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        metadata = {}
        
        # Get PDF metadata
        if pdf_reader.metadata:
            metadata['title'] = pdf_reader.metadata.get('/Title', '')
            metadata['author'] = pdf_reader.metadata.get('/Author', '')
            metadata['subject'] = pdf_reader.metadata.get('/Subject', '')
            metadata['creator'] = pdf_reader.metadata.get('/Creator', '')
            metadata['producer'] = pdf_reader.metadata.get('/Producer', '')
            metadata['creation_date'] = str(pdf_reader.metadata.get('/CreationDate', ''))
            
        # Add page count
        metadata['page_count'] = str(len(pdf_reader.pages))
        
        return metadata
    except Exception:
        return {}

def get_document_type(name: str, date: str) -> Optional[str]:
    """Determine document type (html or pdf) by checking which file exists."""
    documents_dir = Path(__file__).parent.parent / "documents" / "content"
    
    html_filepath = documents_dir / f"{name}_{date}.html"
    pdf_filepath = documents_dir / f"{name}_{date}.pdf"
    
    if html_filepath.exists():
        return "html"
    elif pdf_filepath.exists():
        return "pdf"
    return None

def get_available_documents(name: Optional[str] = None, date: Optional[str] = None) -> List[Dict]:
    """Get list of available documents, optionally filtered by name or date."""
    metadata = load_document_metadata()
    documents = metadata.get("documents", [])
    
    if name:
        documents = [doc for doc in documents if doc["name"] == name]
    if date:
        documents = [doc for doc in documents if doc["date"] == date]
    
    return documents