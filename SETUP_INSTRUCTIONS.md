# Setup Instructions for User-Independent Deployment

## Required Streamlit Secrets (Admin Setup Only)

For the app to work for ANY user (user-independent), you need to add the following to your Streamlit Cloud secrets:

```toml
# Google OAuth Client Credentials
# Get these from: https://console.cloud.google.com/apis/credentials
GOOGLE_CLIENT_ID = "your_client_id_here.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your_client_secret_here"
```

**Note:** You do NOT need to add GEMINI_API_KEY to secrets. Each user will provide their own!

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
2. User enters THEIR OWN Gemini API key (free from Google)
3. User clicks "Start Google Authentication"
4. User is redirected to Google login
5. User grants calendar access to THEIR account
6. User copies the authorization code
7. User pastes code back into app
8. App creates meetings in THEIR calendar using THEIR API key

## Benefits

- ✅ No hardcoded credentials
- ✅ Each user uses their own Google Calendar
- ✅ Each user uses their own Gemini API key and quota
- ✅ Privacy-friendly - no shared data
- ✅ Multi-user support - unlimited users
- ✅ No cost to you - users provide their own API keys
- ✅ No token.json needed in repo
