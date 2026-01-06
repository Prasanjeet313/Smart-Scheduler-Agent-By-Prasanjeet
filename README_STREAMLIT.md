# 📅 Smart Scheduler AI Agent - Streamlit Web App

A full-stack web application that uses AI to help schedule meetings through natural conversation and integrates with Google Calendar.

## ✨ Features

- **🔐 Secure API Key Input**: Enter your Gemini API key directly in the web interface
- **💬 Natural Language Processing**: Chat naturally about your meetings
- **📅 Google Calendar Integration**: Real-time free/busy slot detection
- **🤖 AI-Powered Scheduling**: Gemini 2.5 Flash understands vague inputs like "after lunch tomorrow"
- **✅ Smart Confirmation**: Review details before scheduling
- **🎨 Beautiful UI**: Clean, responsive Streamlit interface
- **💾 Context Memory**: Maintains conversation context across messages
- **🌍 Multi-timezone Support**: Choose your preferred timezone

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **Google Calendar API**
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Configure OAuth consent screen
6. Download `credentials.json` and place it in the project root

### 3. Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create or select a project
3. Click **Get API Key**
4. Copy your API key (you'll enter this in the web app)

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

1. **Enter API Key**: Paste your Gemini API key in the sidebar
2. **Connect Calendar**: On first run, authenticate with Google Calendar
3. **Start Chatting**: Type natural meeting requests like:
   - "Schedule a meeting tomorrow at 3 PM"
   - "Book a 1-hour call with john@example.com next Friday afternoon"
   - "Find a free slot for team standup this week"
4. **Review Details**: Check the meeting context panel
5. **Confirm**: Click "Confirm & Schedule" when ready

## 💬 Example Commands

- "Schedule a client meeting tomorrow at 2 PM for 30 minutes"
- "Book a team sync next Monday morning"
- "Find me a free slot on Friday afternoon"
- "Add a meeting with alice@company.com at 4 PM today"
- "Schedule a 2-hour workshop next week"

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI**: Google Gemini 2.5 Flash
- **Calendar**: Google Calendar API
- **Backend**: Python 3.8+
- **Libraries**: 
  - `streamlit` - Web framework
  - `google-generativeai` - Gemini AI
  - `google-api-python-client` - Calendar API
  - `pytz` - Timezone handling
  - `pickle` - Context persistence

## 📁 Project Structure

```
Smart-Scheduler-Agent/
├── app.py                  # Main Streamlit application
├── main.ipynb             # Original Jupyter notebook (legacy)
├── requirements.txt       # Python dependencies
├── credentials.json       # Google Calendar OAuth (you create this)
├── token.json            # Auto-generated after first auth
├── context.pkl           # Conversation context (auto-generated)
└── README_STREAMLIT.md   # This file
```

## ⚙️ Configuration

### Timezone
Change timezone in the sidebar or modify the default in `app.py`:
```python
TIMEZONE = "Asia/Kolkata"  # Change to your timezone
```

### API Settings
All API keys are entered directly in the web interface - no `.env` file needed!

## 🔒 Security Notes

- API keys are stored in session state (not persistent)
- Re-enter API key each time you restart the app
- Never commit `credentials.json` or `token.json` to version control
- Add them to `.gitignore`

## 🐛 Troubleshooting

**"credentials.json not found"**
- Download from Google Cloud Console
- Place in project root directory

**"Failed to connect to Google Calendar"**
- Check credentials.json is valid
- Ensure Calendar API is enabled
- Re-authenticate by deleting token.json

**"API Key Invalid"**
- Verify key from Google AI Studio
- Check for extra spaces when pasting
- Ensure Gemini API is enabled

**Slots not showing correctly**
- Verify timezone setting
- Check Google Calendar has events
- Ensure date format is YYYY-MM-DD

## 🎯 Roadmap

- [ ] Add recurring event support
- [ ] Multiple calendar support
- [ ] Email notifications
- [ ] Meeting reminders
- [ ] Export to other calendar formats
- [ ] Mobile-responsive improvements
- [ ] Dark mode toggle

## 📄 License

MIT License - Feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Built with ❤️ using Streamlit and Google Gemini AI**
