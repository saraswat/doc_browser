# Google OAuth Setup Guide

**Complete guide to configure Google OAuth for the Document Browser**

## 🔍 Google OAuth Overview

Google OAuth allows users to authenticate using their Google accounts, supporting both:
- **Personal Google accounts** (@gmail.com)
- **Google Workspace accounts** (your-domain.com managed by Google)

## 📋 Prerequisites

- Google account with access to Google Cloud Console
- Administrator access (for Google Workspace domain setup)

## 🛠️ Step-by-Step Setup

### 1. Create Google Cloud Project

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com
   - Sign in with your Google account

2. **Create New Project**
   - Click "Select a project" dropdown
   - Click "NEW PROJECT"
   - Enter project name: "Document Browser"
   - Select your organization (if applicable)
   - Click "CREATE"

3. **Enable Required APIs**
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it
   - Search for "People API" and enable it (for profile access)

### 2. Configure OAuth Consent Screen

1. **Go to OAuth Consent Screen**
   - Navigate to "APIs & Services" > "OAuth consent screen"

2. **Choose User Type**
   - **Internal**: For Google Workspace users only (recommended for organizations)
   - **External**: For any Google account (required for @gmail.com users)

3. **Fill OAuth Consent Screen**
   ```
   App name: Document Browser
   User support email: your-email@domain.com
   Logo: (optional) Upload your company logo
   Application home page: http://localhost:8502
   Authorized domains: localhost
   Developer contact: your-email@domain.com
   ```

4. **Scopes Configuration**
   - Click "ADD OR REMOVE SCOPES"
   - Select these scopes:
     - `openid`
     - `email` 
     - `profile`
   - Save and continue

5. **Test Users** (for External apps only)
   - Add test user email addresses during development
   - Production apps need Google verification

### 3. Create OAuth 2.0 Credentials

1. **Go to Credentials**
   - Navigate to "APIs & Services" > "Credentials"
   - Click "CREATE CREDENTIALS" > "OAuth 2.0 Client ID"

2. **Configure OAuth Client**
   ```
   Application type: Web application
   Name: Document Browser OAuth Client
   
   Authorized JavaScript origins:
   - http://localhost:8502
   - http://localhost:8503
   - http://127.0.0.1:8502
   
   Authorized redirect URIs:
   - http://localhost:8502/auth/callback
   - http://localhost:8503/auth/callback
   ```

3. **Download Credentials**
   - Click "CREATE"
   - Copy the **Client ID** and **Client Secret**
   - Keep these secure!

### 4. Configure Environment Variables

Create `.env` file with your credentials:

```bash
# Google OAuth Configuration
GOOGLE_CLIENT_ID=123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-1234567890abcdefghijklmnop

# Application Settings
OAUTH_REDIRECT_URI=http://localhost:8502/auth/callback
DATABASE_URL=sqlite:///./document_browser.db
```

### 5. Test Your Setup

1. **Start the Application**
   ```bash
   streamlit run app.py --server.port 8502
   ```

2. **Test Google Login**
   - Go to http://localhost:8502
   - Click "🔍 Login with Google"
   - You should be redirected to Google's login page
   - Complete authentication
   - You should be redirected back to the app

## 🏢 Google Workspace Configuration

For enterprise/office environments using Google Workspace:

### Admin Console Setup

1. **Go to Google Admin Console**
   - Visit: https://admin.google.com
   - Sign in as domain administrator

2. **Configure OAuth Apps**
   - Go to "Security" > "API controls" > "App access control"
   - Click "MANAGE THIRD-PARTY APP ACCESS"
   - Add your app's Client ID to trusted apps

3. **Domain-wide Delegation** (if needed)
   - For accessing user data across the domain
   - Go to "Security" > "API controls" > "Domain-wide delegation"
   - Add your Client ID with required scopes

### Organizational Units

Configure access by organizational unit:
- Restrict app access to specific departments
- Set different policies for different user groups

## 🔒 Security Best Practices

### Development Environment
- Use `localhost` for redirect URIs during development
- Keep Client ID and Secret in environment variables
- Never commit credentials to version control

### Production Environment
- Use HTTPS for all redirect URIs
- Configure proper CORS settings
- Implement proper session management
- Regular security audits

### Google Workspace Security
- Enable 2-factor authentication for admin accounts
- Regular review of authorized applications
- Monitor OAuth usage through admin console
- Implement conditional access policies

## 🚨 Troubleshooting

### Common Errors

**"redirect_uri_mismatch"**
- Ensure redirect URI in code matches Google Console exactly
- Check for trailing slashes, http vs https
- Verify port numbers match

**"access_denied"**
- User declined authorization
- Check OAuth consent screen configuration
- Verify user has access to the application

**"invalid_client"**
- Client ID or Client Secret incorrect
- Verify environment variables are loaded correctly

**"unauthorized_client"**
- OAuth client not properly configured
- Check application type is "Web application"

### Debug Steps

1. **Check Environment Variables**
   ```python
   import os
   print("Google Client ID:", os.getenv("GOOGLE_CLIENT_ID"))
   print("Redirect URI:", os.getenv("OAUTH_REDIRECT_URI"))
   ```

2. **Verify OAuth URLs**
   - Check the generated auth URL includes correct parameters
   - Ensure state parameter is being set and validated

3. **Test with Minimal Scope**
   - Start with just `openid email` scope
   - Add `profile` after basic auth works

## 🔄 Multi-Provider Setup

The Document Browser supports multiple OAuth providers simultaneously:

```bash
# Support both Google and Microsoft
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

MICROSOFT_CLIENT_ID=your_microsoft_client_id  
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret
MICROSOFT_TENANT_ID=common

# Users can choose their preferred login method
```

## 📊 Usage Analytics

Monitor OAuth usage through:
- **Google Cloud Console**: API usage and quota
- **Google Admin Console**: User access patterns (Workspace)
- **Application Logs**: Authentication success/failure rates

## 🔄 Production Migration

### HTTPS Configuration
```bash
# Production environment variables
GOOGLE_CLIENT_ID=your_production_client_id
GOOGLE_CLIENT_SECRET=your_production_client_secret
OAUTH_REDIRECT_URI=https://your-domain.com/auth/callback
```

### Domain Verification
- Add your production domain to Google Cloud Console
- Configure DNS verification for domain ownership
- Update authorized domains in OAuth consent screen

### SSL Certificate
- Obtain SSL certificate for your domain
- Configure reverse proxy (nginx/Apache) for HTTPS
- Update all redirect URIs to use HTTPS

---

## ✅ Verification Checklist

- [ ] Google Cloud project created and configured
- [ ] OAuth consent screen configured with proper scopes
- [ ] OAuth 2.0 credentials created with correct redirect URIs
- [ ] Environment variables set with valid Client ID and Secret  
- [ ] Application starts without OAuth configuration errors
- [ ] Google login button appears on login page
- [ ] Successful redirect to Google authentication page
- [ ] Successful authentication and redirect back to app
- [ ] User profile information displayed correctly
- [ ] User can access documents and add comments
- [ ] Logout functionality works properly

**Google OAuth is now fully configured and ready for use!**

For additional support, refer to [Google's OAuth 2.0 documentation](https://developers.google.com/identity/protocols/oauth2) or the main project documentation.