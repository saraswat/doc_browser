# Document Browser Application

A modern document browsing application built with Python and Streamlit that allows users to browse AI-generated documents with rich HTML rendering capabilities.

## Features

- **Document Selection**: Browse documents by name and date using intuitive dropdown selectors
- **Rich HTML Rendering**: View documents with preserved styling, tables, and charts
- **Metadata Display**: See document information and properties
- **Responsive Design**: Clean, modern interface optimized for document viewing

## Project Structure

```
document_browser/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── components/
│   ├── document_viewer.py     # Document display component
│   └── selectors.py           # Dropdown components
├── documents/
│   ├── metadata.json          # Document metadata registry
│   └── content/               # HTML files for documents
└── utils/
    └── document_loader.py     # Document loading utilities
```

## Installation

1. Navigate to the project directory:
```bash
cd document_browser
```

2. Install dependencies:
```bash
pip install streamlit beautifulsoup4 lxml
```

## Running the Application

Start the Streamlit server:
```bash
streamlit run app.py --server.port 8501
```

The application will be available at http://localhost:8501

## Usage

1. **Select Document Name**: Choose from available document names in the first dropdown
2. **Select Date**: Choose a date for the selected document in the second dropdown  
3. **View Document**: The document will render in the main panel with full HTML styling
4. **View Metadata**: Expand the document information section to see metadata

## Sample Documents

The application includes sample documents:
- **AI Research Report** (January & February 2024)
- **Market Analysis** (January 2024) 
- **Technical Specification** (January 2024)

## Adding New Documents

1. Create an HTML file in `documents/content/` with the naming pattern: `{name}_{date}.html`
2. Add metadata entry to `documents/metadata.json`
3. Include document metadata in HTML `<meta>` tags:
   - `document-name`
   - `document-date`  
   - `author`
   - `version`

## Architecture

- **Frontend**: Streamlit web framework
- **Document Format**: HTML with embedded CSS and metadata
- **Caching**: Streamlit's built-in caching for performance
- **Components**: Modular design with separate selector and viewer components

## Next Steps

This is Phase 1 of the document browser. Future phases will include:
- **Phase 2**: User authentication with streamlit-authenticator
- **Phase 3**: Document feedback and markup system
- SQLite database integration
- Advanced search and filtering capabilities