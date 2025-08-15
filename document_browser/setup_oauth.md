# OAuth Setup Guide for Document Browser

This guide will help you set up OAuth authentication for your office environment.

## Microsoft Azure AD Setup (Recommended for Office Environment)

### 1. Register Application in Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to **Azure Active Directory** > **App registrations**
3. Click **New registration**
4. Configure:
   - **Name**: Document Browser
   - **Supported account types**: Accounts in this organizational directory only
   - **Redirect URI**: Web - `http://localhost:8502/auth/callback`

### 2. Configure API Permissions

1. In your app registration, go to **API permissions**
2. Click **Add a permission** > **Microsoft Graph** > **Delegated permissions**
3. Add these permissions:
   - `openid`
   - `email`
   - `profile`
4. Click **Grant admin consent**

### 3. Create Client Secret

1. Go to **Certificates & secrets**
2. Click **New client secret**
3. Set description and expiration
4. **Copy the secret value immediately** (you won't be able to see it again)

### 4. Configure Environment Variables

Create a `.env` file in your project directory:

```bash
# Microsoft OAuth
MICROSOFT_CLIENT_ID=your_application_id_from_azure
MICROSOFT_CLIENT_SECRET=your_client_secret_from_step_3
MICROSOFT_TENANT_ID=your_tenant_id_or_common

# Application Settings
OAUTH_REDIRECT_URI=http://localhost:8502/auth/callback
DATABASE_URL=sqlite:///./document_browser.db
```

## Alternative: Google OAuth Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project or select existing one
3. Enable **Google+ API**

### 2. Configure OAuth Consent Screen

1. Go to **APIs & Services** > **OAuth consent screen**
2. Configure the consent screen with your application details

### 3. Create OAuth 2.0 Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth 2.0 Client ID**
3. Application type: **Web application**
4. Add authorized redirect URI: `http://localhost:8502/auth/callback`

### 4. Environment Variables for Google

```bash
# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Application Settings
OAUTH_REDIRECT_URI=http://localhost:8502/auth/callback
```

## Security Considerations for Office Environment

### 1. Network Configuration

- Ensure the application is accessible on your corporate network
- Configure firewall rules to allow port 8502
- Consider using HTTPS in production (update redirect URIs accordingly)

### 2. User Access Control

- Use organizational directory-only authentication
- Configure appropriate user consent policies
- Review and audit user permissions regularly

### 3. Database Security

- For production, use PostgreSQL instead of SQLite
- Configure proper database access controls
- Enable database encryption at rest

### 4. Application Security

- Use environment-specific redirect URIs
- Regularly rotate client secrets
- Monitor authentication logs

## Production Deployment

For production deployment, update these settings:

```bash
# Production Environment Variables
OAUTH_REDIRECT_URI=https://your-domain.com/auth/callback
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your_secure_random_secret_key
```

## Testing the Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables (copy `.env.example` to `.env` and fill in values)

3. Run the application:
   ```bash
   streamlit run app.py --server.port 8502
   ```

4. Test authentication flow:
   - Navigate to `http://localhost:8502`
   - Click on your configured OAuth provider
   - Complete authentication
   - Verify you can access documents and add comments

## Troubleshooting

### Common Issues

1. **Redirect URI Mismatch**: Ensure the redirect URI in OAuth provider matches exactly with your environment variable

2. **Missing Permissions**: Verify all required API permissions are granted and consented

3. **Client Secret Issues**: Ensure client secret is correct and not expired

4. **Network Issues**: Check corporate firewall and proxy settings

### Support

For additional help:
- Check Azure AD logs for authentication failures
- Review Streamlit application logs
- Verify environment variables are loaded correctly
- Test OAuth URLs manually in browser