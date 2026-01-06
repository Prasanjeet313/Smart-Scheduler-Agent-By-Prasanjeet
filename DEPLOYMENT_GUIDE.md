# Complete Setup Guide for Streamlit Cloud Deployment

## ✅ What Makes This App User-Independent?

Your app is now **100% USER-INDEPENDENT**! 🎉

**Each user provides:**
1. ✅ Their own **Gemini API Key** (free from Google)
2. ✅ Their own **Google Calendar authentication**
3. ✅ Meetings go to **their own calendar**

**You (the admin) only need to provide:**
- Google OAuth Client ID and Secret (one-time setup)

## 📋 Required Streamlit Secrets (Admin Only)

Go to your Streamlit Cloud app → **Settings** → **Secrets** and add:

```toml
# Google OAuth Client Credentials (from Google Cloud Console)
# These allow users to authenticate with their own Google accounts
GOOGLE_CLIENT_ID = "your_client_id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your_client_secret"
```

**That's it!** No Gemini API key needed in secrets - users provide their own!

## 🔧 How to Get Google OAuth Credentials

### Step 1: Go to Google Cloud Console
Visit: https://console.cloud.google.com/

### Step 2: Create/Select Project
- Create a new project OR select existing one
- Note the project name

### Step 3: Enable Google Calendar API
1. Go to **APIs & Services** → **Library**
2. Search for "Google Calendar API"
3. Click **Enable**

### Step 4: Create OAuth 2.0 Credentials
1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. If prompted, configure OAuth consent screen first:
   - User Type: **External**
   - App name: "Smart Scheduler"
   - User support email: your email
   - Scopes: Add "Google Calendar API" (.../auth/calendar)
   - Test users: Add your email and any test users
4. Application type: **Desktop app**
5. Name: "Smart Scheduler Desktop"
6. Click **Create**

### Step 5: Configure OAuth
1. Download the JSON file (optional, for reference)
2. Copy the **Client ID** and **Client Secret**
3. Add them to your Streamlit secrets (as shown above)

### Step 6: Configure Redirect URIs (Important!)
1. Edit your OAuth client
2. Add authorized redirect URI: `urn:ietf:wg:oauth:2.0:oob`
3. Save

## 🚀 How Users Will Use the App

### For Each New User:

1. **Open the App**
   - Visit your Streamlit Cloud URL

2. **Enter Their Own Gemini API Key**
   - Get a free API key from https://makersuite.google.com/app/apikey
   - Enter it in the sidebar
   - This uses THEIR quota, not yours!

3. **Authenticate with Their Google Account**
   - Click "Start Google Authentication" button
   - Click the authorization link
   - Sign in with their Google account
   - Grant calendar access
   - Copy the authorization code shown
   - Paste the code back into the app
   - Click "Submit Code"

4. **Start Scheduling!**
   - Type meeting requests naturally
   - AI schedules meetings in THEIR calendar
   - Uses THEIR Gemini API quota

## 🎯 Key Benefits

✅ **Privacy**: Each user's calendar stays private
✅ **Security**: No shared credentials
✅ **Scalability**: Unlimited users can use the app
✅ **Personal**: Meetings go to the user's own calendar
✅ **No Cost to You**: Each user uses their own Gemini API quota
✅ **Independent**: Users don't need your API keys

## 🔒 Security Notes

- The app only stores credentials in session state (temporary)
- Credentials are lost when the user closes the browser
- Users need to re-authenticate each session
- No user data is stored on your server

## ⚠️ Important Reminders

1. **OAuth Consent Screen**: Must be configured before users can authenticate
2. **Test Users**: Add test users in OAuth consent screen during development
3. **Publishing**: To make it public, submit your OAuth consent screen for verification (takes a few days)
4. **Scopes**: Only Google Calendar API scope is needed

## 🐛 Troubleshooting

### "Invalid Client ID"
- Check GOOGLE_CLIENT_ID in Streamlit secrets
- Ensure no extra spaces or quotes

### "Redirect URI Mismatch"
- Add `urn:ietf:wg:oauth:2.0:oob` to authorized redirect URIs

### "Access Blocked: This app's request is invalid"
- Configure OAuth consent screen
- Add test users
- Enable Google Calendar API

### "Authorization Code Invalid"
- Code expires quickly, use it immediately
- Don't modify the code (no spaces)
- Try generating a new code

## 📞 Support

If users have issues, they should:
1. Try re-authenticating
2. Check if they granted calendar permissions
3. Use the re-authenticate button
4. Clear browser cache and try again

## 🎉 You're All Set!

Your app is now ready for multi-user deployment on Streamlit Cloud!

Repository: https://github.com/Prasanjeet313/Smart-Scheduler-Agent-By-Prasanjeet
