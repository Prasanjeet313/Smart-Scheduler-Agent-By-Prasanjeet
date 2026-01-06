# 🚀 Quick Start Guide

Get your Smart Scheduler AI Agent running in 5 minutes!

## Step 1: Install Dependencies (1 min)

**Windows:**
```bash
setup.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Manual:**
```bash
pip install -r requirements.txt
```

## Step 2: Get Google Calendar Credentials (2 min)

1. Go to: https://console.cloud.google.com/
2. Create a new project
3. Enable **Google Calendar API**
4. Create **OAuth 2.0 Client ID** credentials
5. Download as `credentials.json`
6. Place in project folder

## Step 3: Get Gemini API Key (1 min)

1. Visit: https://makersuite.google.com/app/apikey
2. Click "Get API Key"
3. Copy the key (you'll paste it in the app)

## Step 4: Launch App (1 min)

```bash
streamlit run app.py
```

Browser will open automatically at `http://localhost:8501`

## Step 5: Start Scheduling! ✨

1. Paste your Gemini API key in the sidebar
2. Authenticate with Google Calendar (first time only)
3. Type: "Schedule a meeting tomorrow at 3 PM"
4. Watch the magic happen! 🎉

## Example Queries

- "Book a 30-minute call with john@example.com next Monday"
- "Find me a free slot Friday afternoon"
- "Schedule team standup for 9 AM tomorrow"
- "Create a 2-hour workshop meeting next week"

## Troubleshooting

**No credentials.json?**
- Download from Google Cloud Console
- Must be in same folder as app.py

**API Key not working?**
- Verify it's copied correctly
- Check it's from Google AI Studio
- No spaces at the beginning/end

**Can't connect to Calendar?**
- Delete token.json and try again
- Check Calendar API is enabled
- Verify credentials.json is valid

## Need Help?

Check the full [README_STREAMLIT.md](README_STREAMLIT.md) for detailed documentation.

---

**Enjoy your AI-powered scheduling assistant! 🎊**
