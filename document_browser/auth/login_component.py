"""Login component for OAuth authentication."""

import streamlit as st
from typing import Optional
from .oauth import get_oauth_login_url, handle_oauth_callback, login_user, config


def render_login_page():
    """Render the login page with OAuth options."""
    st.title("🔐 Document Browser - Login")
    
    st.markdown("""
    Welcome to the Document Browser! This application requires authentication to access documents and provide feedback.
    
    Please choose your login method:
    """)
    
    # Check which OAuth providers are configured
    available_providers = []
    if config.is_configured("google"):
        available_providers.append(("google", "🔍 Login with Google", "#4285F4"))
    if config.is_configured("microsoft"):
        available_providers.append(("microsoft", "🏢 Login with Microsoft", "#0078D4"))
    if config.is_configured("github"):
        available_providers.append(("github", "🐙 Login with GitHub", "#333333"))
    
    if not available_providers:
        st.error("""
        ⚠️ No OAuth providers configured!
        
        Please set up at least one OAuth provider by configuring the following environment variables:
        
        **Google OAuth:**
        - `GOOGLE_CLIENT_ID`
        - `GOOGLE_CLIENT_SECRET`
        
        **Microsoft OAuth:**
        - `MICROSOFT_CLIENT_ID`
        - `MICROSOFT_CLIENT_SECRET`
        - `MICROSOFT_TENANT_ID` (optional, defaults to 'common')
        
        **GitHub OAuth:**
        - `GITHUB_CLIENT_ID`
        - `GITHUB_CLIENT_SECRET`
        
        **Redirect URI:**
        - `OAUTH_REDIRECT_URI` (defaults to 'http://localhost:8502/auth/callback')
        """)
        return
    
    # Display login buttons
    st.markdown("### Choose your authentication provider:")
    
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    
    for i, (provider, label, color) in enumerate(available_providers):
        with columns[i % 3]:
            if st.button(label, key=f"login_{provider}"):
                # Store the provider in session state for callback handling
                st.session_state['oauth_provider'] = provider
                
                auth_url = get_oauth_login_url(provider)
                if auth_url:
                    # Show redirect message and automatically redirect
                    st.markdown(f"""
                    <div style="text-align: center; padding: 20px;">
                        <p>🔄 Redirecting to {provider.title()} login...</p>
                        <p><em>If you're not redirected automatically, <a href="{auth_url}" target="_self">click here</a></em></p>
                    </div>
                    <meta http-equiv="refresh" content="1;url={auth_url}">
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"❌ Failed to generate {provider.title()} login URL. Please check your OAuth configuration.")
    
    # Information about OAuth setup
    with st.expander("ℹ️ OAuth Setup Information"):
        st.markdown("""
        ### For Office Environment Setup:
        
        **Microsoft Azure AD:**
        1. Register your app in Azure Portal
        2. Configure redirect URI: `http://localhost:8502/auth/callback`
        3. Grant appropriate API permissions
        4. Set environment variables with your app credentials
        
        **Google Workspace:**
        1. Create OAuth 2.0 credentials in Google Cloud Console
        2. Add authorized redirect URI
        3. Set environment variables
        
        **Security Notes:**
        - All authentication uses industry-standard OAuth 2.0
        - No passwords are stored locally
        - Session tokens expire automatically
        - Users can log out at any time
        """)


def handle_oauth_redirect():
    """Handle OAuth callback - now handled in main app with modern Streamlit."""
    # This function is no longer needed with modern Streamlit
    # OAuth callbacks are handled directly in app.py using st.query_params
    return False
    


def render_user_info(user_info: dict):
    """Render user information and logout option."""
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if user_info.get('avatar_url'):
            st.image(user_info['avatar_url'], width=40)
        st.write(f"**{user_info['name']}**")
        st.write(f"_{user_info['email']}_")
    
    with col3:
        if st.button("Logout", key="logout_btn"):
            from .oauth import logout_user
            logout_user()
            st.rerun()