# Setup Instructions for User-Independent Deployment

## Required Streamlit Secrets

For the app to work for ANY user (user-independent), you need to add the following to your Streamlit Cloud secrets:

```toml
# Gemini API Key (your personal key)
GEMINI_API_KEY = "your_gemini_api_key_here"

# Google OAuth Client Credentials
# Get these from: https://console.cloud.google.com/apis/credentials
GOOGLE_CLIENT_ID = "your_client_id_here.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your_client_secret_here"
```

## How to Get Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google Calendar API**
4. Go to **Credentials** → **Create Credentials** → **OAuth client ID**
5. Application type: **Desktop app** or **Web application**
6. For redirect URIs, add: `urn:ietf:wg:oauth:2.0:oob`
7. Copy the **Client ID** and **Client Secret**
8. Add them to Streamlit secrets

## User Flow

1. User opens your Streamlit app
2. User clicks "Start Google Authentication"
3. User is redirected to Google login
4. User grants calendar access
5. User copies the authorization code
6. User pastes code back into app
7. App creates meeting in THEIR calendar

## Benefits

- ✅ No hardcoded credentials
- ✅ Each user uses their own Google Calendar
- ✅ Privacy-friendly
- ✅ Multi-user support
- ✅ No token.json needed in repo
