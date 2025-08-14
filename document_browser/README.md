# Document Browser with OAuth Authentication

A modern, enterprise-ready document browsing application built with Streamlit that supports HTML and PDF documents with OAuth authentication and collaborative commenting features.

## 🚀 Features

### 📄 Document Management
- **HTML Documents**: Rich rendering with embedded styles, tables, and interactive charts
- **PDF Documents**: In-browser viewing with metadata extraction and download capability
- **Document Metadata**: Automatic extraction of title, author, creation date, and other properties
- **File Type Detection**: Seamless handling of different document formats

### 🔐 Enterprise Authentication
- **Multi-Provider OAuth**: Google, Microsoft (Azure AD), GitHub
- **Google OAuth**: Supports both personal (@gmail.com) and Google Workspace accounts
- **Microsoft OAuth**: Azure AD integration for enterprise environments
- **Secure Sessions**: Token-based authentication with automatic expiration
- **User Profiles**: Automatic user provisioning from OAuth provider data

### 💬 Collaborative Features
- **Document Comments**: Add feedback and discussions to any document
- **User Attribution**: Comments linked to authenticated users with timestamps
- **Comment Management**: Edit, delete, and resolve comments
- **Element Linking**: Reference specific document sections in comments
- **Comment Statistics**: Track resolution status and activity

### 🎨 Modern UI/UX
- **Responsive Design**: Optimized for desktop and tablet viewing
- **Clean Interface**: Intuitive sidebar navigation with document selection
- **Real-time Updates**: Immediate feedback on user actions
- **User Dashboard**: Personal comment history and activity tracking

## 📋 Quick Start

### 1. Installation
```bash
git clone https://github.com/saraswat/doc_browser.git
cd doc_browser/document_browser
pip install -r requirements.txt
```

### 2. OAuth Configuration
Choose at least one OAuth provider:

#### Google OAuth (Recommended for broad compatibility)
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project and enable Google+ API
3. Configure OAuth consent screen
4. Create OAuth 2.0 Web Application credentials
5. Add redirect URI: `http://localhost:8502/auth/callback`

#### Microsoft OAuth (Recommended for enterprises)
1. Go to [Azure Portal](https://portal.azure.com)
2. Register new application in App registrations
3. Add API permissions: `openid`, `email`, `profile`
4. Create client secret
5. Configure redirect URI: `http://localhost:8502/auth/callback`

### 3. Environment Setup
Create `.env` file:
```bash
# Google OAuth
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your_client_secret

# Microsoft OAuth  
MICROSOFT_CLIENT_ID=your_application_id
MICROSOFT_CLIENT_SECRET=your_client_secret
MICROSOFT_TENANT_ID=common

# Application Settings
OAUTH_REDIRECT_URI=http://localhost:8502/auth/callback
DATABASE_URL=sqlite:///./document_browser.db
```

### 4. Run Application
```bash
streamlit run app.py --server.port 8502
```

Visit: http://localhost:8502

## 📚 Documentation

- **[Quick Start Guide](../QUICK_START_GUIDE.md)** - Get running in 5 minutes
- **[Google OAuth Setup](GOOGLE_OAUTH_SETUP.md)** - Detailed Google configuration
- **[OAuth Setup Guide](setup_oauth.md)** - Multi-provider configuration
- **[Implementation Summary](../IMPLEMENTATION_SUMMARY.md)** - Technical architecture
- **[Code Changes Log](../CODE_CHANGES_LOG.md)** - Development history

## 🏗️ Architecture

### Technology Stack
- **Frontend**: Streamlit with custom components
- **Authentication**: OAuth 2.0 (Google, Microsoft, GitHub)
- **Database**: SQLAlchemy with SQLite (dev) / PostgreSQL (prod)
- **Document Processing**: BeautifulSoup4, PyPDF2, ReportLab
- **Security**: Authlib, Cryptography, secure session management

### Project Structure
```
document_browser/
├── app.py                      # Main Streamlit application
├── auth/                       # OAuth authentication system
│   ├── oauth.py               # OAuth providers and flows
│   └── login_component.py     # Login UI components
├── components/                 # UI components
│   ├── selectors.py           # Document selection interface
│   ├── document_viewer.py     # HTML/PDF rendering
│   ├── pdf_viewer.py          # PDF-specific viewer
│   └── comments.py            # Comment management
├── database/                   # Data layer
│   ├── models.py              # SQLAlchemy models
│   ├── database.py            # Database connection
│   └── crud.py                # Database operations
├── documents/                  # Document storage
│   ├── metadata.json          # Document registry
│   └── content/               # HTML and PDF files
└── utils/                      # Utilities
    ├── document_loader.py     # Document processing
    └── pdf_generator.py       # Sample PDF creation
```

## 🔒 Security Features

### Authentication Security
- OAuth 2.0 with CSRF protection via state parameter
- Secure session token generation and validation
- Automatic session expiration and cleanup
- Multi-provider support with provider isolation

### Data Security
- SQL injection prevention through SQLAlchemy ORM
- Input validation and sanitization for comments
- Secure database connection handling
- Environment-based configuration management

### Network Security
- Configurable HTTPS support for production
- CORS policy management
- Secure cookie handling
- Content Security Policy ready

## 🚀 Production Deployment

### Environment Variables
```bash
# Production OAuth (HTTPS required)
GOOGLE_CLIENT_ID=prod_client_id.apps.googleusercontent.com
MICROSOFT_CLIENT_ID=prod_application_id
OAUTH_REDIRECT_URI=https://your-domain.com/auth/callback

# Production Database
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Security
SECRET_KEY=your_secure_random_secret_key
```

### Database Migration
```bash
# Migrate to PostgreSQL
pip install psycopg2-binary
export DATABASE_URL="postgresql://user:pass@host:port/dbname"
python -c "from database.database import init_database; init_database()"
```

### Docker Deployment
```dockerfile
FROM python:3.8-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

## 📊 Sample Documents

The application includes sample documents demonstrating different features:

### HTML Documents
- **AI Research Report** (2 versions) - Rich formatting with progress bars and tables
- **Market Analysis** - Interactive charts and metrics cards  
- **Technical Specification** - System architecture with code blocks

### PDF Documents
- **Financial Summary** - Professional report with tables and KPIs
- **Product Roadmap** - Timeline with milestones and technology stack

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit with descriptive messages
5. Push and create pull request

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include comprehensive docstrings
- Write unit tests for new features
- Update documentation for changes

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues
- **OAuth redirect errors**: Verify redirect URI matches configuration exactly
- **Database errors**: Check SQLAlchemy version compatibility  
- **Import errors**: Ensure all dependencies installed with correct versions
- **Port conflicts**: Use different port: `--server.port 8503`

### Getting Help
- Check documentation in `/docs` folder
- Review troubleshooting guides
- Open GitHub issue with detailed error information
- For enterprise support, contact the development team

### Resources
- [Streamlit Documentation](https://docs.streamlit.io)
- [Google OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)  
- [Microsoft Identity Platform](https://docs.microsoft.com/en-us/azure/active-directory/develop/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)

---

**Document Browser** - Enterprise-ready document viewing with OAuth authentication and collaborative features.

Built with ❤️ using Streamlit, SQLAlchemy, and modern OAuth 2.0 standards.