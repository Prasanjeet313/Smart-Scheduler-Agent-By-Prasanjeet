# 🎬 Demo Instructions

## 🚀 Running Your First Demo

### Prerequisites Check ✅
Run this first:
```bash
python verify_setup.py
```

### Launch the App 🎯
```bash
streamlit run app.py
```

Browser opens automatically at: `http://localhost:8501`

---

## 🎭 Demo Script

### Scene 1: Initial Setup (30 seconds)
1. Show the app landing page
2. Point to the sidebar
3. Paste your Gemini API key
4. Show "Connected to Google Calendar" message

### Scene 2: Simple Scheduling (1 minute)
**Type:** "Schedule a meeting tomorrow at 3 PM"

**Show:**
- AI parsing the request
- Free slots appearing
- Context panel updating
- Confirmation dialog

**Action:** Click "Confirm & Schedule"
**Result:** 🎈 Balloons! Event created!

### Scene 3: Natural Language (1 minute)
**Type:** "Book a call with john@example.com next Monday morning"

**Show:**
- AI understanding "next Monday"
- AI suggesting morning time
- Attendee being added
- Smart time selection

### Scene 4: Availability Check (30 seconds)
**Type:** "What's my availability on Friday?"

**Show:**
- List of free slots in green
- Busy slots in red
- Time ranges clearly displayed

### Scene 5: Complex Request (1 minute)
**Type:** "Schedule a 2-hour workshop at Conference Room B this Thursday 2 PM with team@company.com"

**Show:**
- Multiple parameters extracted:
  - Duration: 2 hours
  - Location: Conference Room B
  - Day: Thursday
  - Time: 2 PM
  - Attendees: team@company.com

---

## 💬 Demo Phrases to Try

### Basic:
- "Schedule a meeting tomorrow at 3 PM"
- "Book a call next Monday at 10 AM"
- "Create a 30-minute meeting on Friday"

### With Attendees:
- "Meeting with alice@example.com tomorrow"
- "Schedule call with bob@company.com and charlie@startup.com next week"

### With Location:
- "Book Conference Room A for team meeting Thursday"
- "Schedule in Zoom Room 1 tomorrow afternoon"

### Vague Timing:
- "Meeting after lunch tomorrow"
- "Call late next week"
- "Schedule something Friday afternoon"

### Duration Specific:
- "2-hour workshop next Monday"
- "Quick 15-minute sync tomorrow"
- "Half-day training session next Wednesday"

---

## 🎯 Key Features to Highlight

1. **No CLI Required** - All in the browser
2. **Natural Language** - Talk like a human
3. **Smart AI** - Understands context
4. **Real Calendar** - Checks actual availability
5. **Beautiful UI** - Clean and modern
6. **Secure** - API key in session only

---

## 🎨 Visual Tour

### Sidebar (Left):
- 🔑 API Key input
- 📍 Timezone selector
- 📖 Instructions
- 🔄 Reset button

### Main Panel (Right):
- 📋 Current context (top)
- 💬 Chat interface (middle)
- ✅ Action buttons (bottom)

### Context Panel Shows:
- Title
- Date
- Time
- Duration
- Location
- Attendees count

### Chat Shows:
- Your messages
- AI responses
- Free slots (green)
- Busy slots (red)
- Confirmation buttons

---

## 🎬 Ending the Demo

1. Show the Google Calendar
2. Point to the created events
3. Show how they link from the app
4. Highlight the ease of use
5. Mention: "All powered by Gemini AI!"

---

## 🐛 If Something Goes Wrong

### No credentials.json?
→ "We need Google Calendar API credentials first"

### API Key Error?
→ "Let me re-enter the API key"

### Time Slot Not Free?
→ "The AI will suggest another time - watch!"

### Connection Issue?
→ Restart: `Ctrl+C` then `streamlit run app.py`

---

## 📊 Demo Stats to Mention

- ⚡ Built with Streamlit
- 🤖 Powered by Gemini 2.5 Flash
- 📅 Google Calendar API integration
- 🌍 Multi-timezone support
- 💾 Context persistence
- 🔐 Secure session storage

---

## 🎤 Closing Lines

"And that's how you schedule meetings with AI - naturally, quickly, and beautifully. No commands to memorize, no complex interfaces, just chat and schedule!"

---

**Ready to impress! 🌟**

Rehearse once, then go live! 🚀
