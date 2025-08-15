# Document Browser - Quick Start Guide

**Fast track to get your Document Browser running with OAuth authentication**

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
cd document_browser
pip install streamlit beautifulsoup4 lxml PyPDF2 reportlab sqlalchemy requests authlib cryptography python-jose
```

### 2. Choose Your OAuth Provider

#### Option A: Microsoft (Recommended for Office)
1. Go to [Azure Portal](https://portal.azure.com) → App registrations → New registration
2. Set redirect URI: `http://localhost:8502/auth/callback`
3. Add API permissions: `openid`, `email`, `profile`
4. Create client secret

#### Option B: Google (Universal Choice - Personal & Workspace)
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project and enable Google+ API
3. Configure OAuth consent screen (Internal for Workspace, External for personal)
4. Create OAuth 2.0 Web Application credentials
5. Add authorized redirect URI: `http://localhost:8502/auth/callback`
6. Copy Client ID and Client Secret

**📖 Need detailed Google setup?** See `document_browser/GOOGLE_OAUTH_SETUP.md`

### 3. Configure Environment
Create `.env` file:
```bash
# For Microsoft
MICROSOFT_CLIENT_ID=your_app_id_here
MICROSOFT_CLIENT_SECRET=your_secret_here
MICROSOFT_TENANT_ID=common

# For Google (works with @gmail.com and Google Workspace accounts)
GOOGLE_CLIENT_ID=your_google_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-your_google_secret_here

# App settings
OAUTH_REDIRECT_URI=http://localhost:8502/auth/callback
```

### 4. Run the Application
```bash
streamlit run app.py --server.port 8502
```

### 5. Test the Features
1. Visit: http://localhost:8502
2. Click your OAuth provider to log in
3. Browse sample documents (HTML and PDF)
4. Add comments to test the feedback system

## 🎯 What You Get

- **6 sample documents** (HTML reports, PDF summaries)
- **OAuth authentication** (secure office-grade login)
- **Comment system** (add feedback to any document)
- **User management** (profiles, sessions, logout)
- **Rich document viewing** (HTML with charts, PDF with metadata)

## 🔧 Customization

### Add Your Own Documents
1. Place HTML/PDF files in `documents/content/`
2. Name format: `Document Name_YYYY-MM-DD.html/pdf`
3. Update `documents/metadata.json`

### Styling
- Edit `.streamlit/config.toml` for themes
- Modify `app.py` for custom CSS

### Database
- Development: SQLite (auto-created)
- Production: Set `DATABASE_URL` to PostgreSQL

## 🚨 Troubleshooting

**OAuth redirect errors**: Check redirect URI matches exactly  
**Database errors**: Delete `document_browser.db` and restart  
**Import errors**: Ensure all dependencies installed  
**Port conflicts**: Change port in command: `--server.port 8503`

## 📁 Key Files Created

```
document_browser/
├── app.py                    # Main application
├── auth/                     # OAuth system
├── database/                 # Data models
├── components/               # UI components  
├── documents/                # Sample docs
└── utils/                    # Utilities
```

---
**Ready for Production?** See `IMPLEMENTATION_SUMMARY.md` for full deployment guide and advanced configuration options.