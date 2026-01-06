import streamlit as st
import os
import json
import re
import datetime
import pytz
import pickle
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

# ------------------ 🔐 PAGE CONFIG ------------------
st.set_page_config(
    page_title="Smart Scheduler AI Agent",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ 🎨 CUSTOM CSS ------------------
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-top: 1rem;
    }
    .info-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #C8E6C9;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #FFCDD2;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ 🔐 CONSTANTS ------------------
SCOPES = ['https://www.googleapis.com/auth/calendar']
TIMEZONE = "Asia/Kolkata"

# ------------------ 💾 CONTEXT MEMORY ------------------
def save_context(ctx):
    """Save context to session state instead of file for user independence"""
    st.session_state.context = ctx

def load_context():
    """Load context from session state"""
    return st.session_state.get('context', None)

# ------------------ 📅 GOOGLE CALENDAR AUTH (USER-INDEPENDENT) ------------------
# ------------------ 📅 GOOGLE CALENDAR AUTH (USER-INDEPENDENT) ------------------
def get_calendar_service():
    """Get calendar service using user's credentials from session"""
    if 'credentials' not in st.session_state:
        return None
    
    creds = st.session_state.credentials
    return build('calendar', 'v3', credentials=creds)

def handle_oauth_callback():
    """Handle OAuth callback from URL parameters"""
    query_params = st.query_params
    
    if 'code' in query_params:
        auth_code = query_params['code']
        
        if 'oauth_flow' in st.session_state:
            try:
                flow = st.session_state.oauth_flow
                flow.fetch_token(code=auth_code)
                
                st.session_state.credentials = flow.credentials
                del st.session_state.oauth_flow
                
                # Clear the code from URL
                st.query_params.clear()
                return True
            except Exception as e:
                st.error(f"❌ Authentication error: {str(e)}")
                return False
    return False

def start_oauth_flow():
    """Start OAuth flow for web application"""
    client_config = {
        "web": {
            "client_id": st.secrets["GOOGLE_CLIENT_ID"],
            "client_secret": st.secrets["GOOGLE_CLIENT_SECRET"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [st.secrets.get("REDIRECT_URI", "https://smart-scheduler-agent-by-prasanjeet-azxhkuyngdnymfyttph9fd.streamlit.app")]
        }
    }
    
    flow = Flow.from_client_config(client_config, scopes=SCOPES)
    flow.redirect_uri = st.secrets.get("REDIRECT_URI", "https://smart-scheduler-agent-by-prasanjeet-azxhkuyngdnymfyttph9fd.streamlit.app")
    
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    
    st.session_state.oauth_flow = flow
    return auth_url

# ------------------ 📅 GET FREE & BUSY SLOTS ------------------
def get_free_and_busy_slots(service, date_str, duration_min=60):
    tz = pytz.timezone(TIMEZONE)
    start_of_day = tz.localize(datetime.datetime.strptime(f"{date_str} 00:00", "%Y-%m-%d %H:%M"))
    end_of_day = start_of_day + datetime.timedelta(days=1)

    result = service.freebusy().query(
        body={
            "timeMin": start_of_day.isoformat(),
            "timeMax": end_of_day.isoformat(),
            "timeZone": TIMEZONE,
            "items": [{"id": "primary"}]
        }
    ).execute()

    busy_times = result['calendars']['primary'].get('busy', [])
    free_slots = []
    current = start_of_day

    for busy in busy_times:
        start = datetime.datetime.fromisoformat(busy['start']).astimezone(tz)
        if (start - current).total_seconds() >= duration_min * 60:
            free_slots.append((current.strftime('%H:%M'), start.strftime('%H:%M')))
        current = datetime.datetime.fromisoformat(busy['end']).astimezone(tz)

    if (end_of_day - current).total_seconds() >= duration_min * 60:
        free_slots.append((current.strftime('%H:%M'), end_of_day.strftime('%H:%M')))

    busy_slots = [(datetime.datetime.fromisoformat(b['start']).astimezone(tz).strftime('%H:%M'),
                   datetime.datetime.fromisoformat(b['end']).astimezone(tz).strftime('%H:%M'))
                  for b in busy_times]

    return free_slots, busy_slots

# ------------------ 📅 CREATE EVENT ------------------
def create_event(service, title, date_str, time_str, duration_min, location=None, attendees=[]):
    tz = pytz.timezone(TIMEZONE)
    start = tz.localize(datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M"))
    end = start + datetime.timedelta(minutes=duration_min)

    event = {
        'summary': title,
        'start': {'dateTime': start.isoformat(), 'timeZone': TIMEZONE},
        'end': {'dateTime': end.isoformat(), 'timeZone': TIMEZONE},
    }
    if location:
        event['location'] = location
    if attendees:
        event['attendees'] = [{'email': a} for a in attendees]

    return service.events().insert(calendarId='primary', body=event).execute()

# ------------------ 📋 PROMPT ------------------
def build_prompt(user_input, date, free_slots, busy_slots, context):
    prompt = f"""
You are a helpful smart scheduling assistant that helps users schedule meetings via natural language conversation.
Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}.

Current meeting context:
- Title: {context.get('title')}
- Duration: {context.get('duration')} minutes  
- Date: {context.get('date')}
- Time: {context.get('time')}
- Attendees: {context.get('attendees')}
- Location: {context.get('location')}

User's message: \"{user_input}\"

Available time slots on {date}: {free_slots}
Busy slots: {busy_slots}

Your task:
1. If any required fields (title, date, time, duration, attendees) are missing, ask the user for them in a friendly way
2. Suggest optimal time slots from the available slots
3. Once ALL required fields are filled, summarize the meeting and ask: "Should I schedule this meeting?"
4. **CRITICAL**: When user says "yes schedule it", "yes", "schedule it", "book it", or similar confirmation, YOU MUST set "confirmed": true
5. If user says no or wants changes, set "confirmed": false and ask what to change
6. **IMPORTANT**: The phrase "yes schedule it" or "schedule it" means the user wants you to CREATE THE EVENT NOW - set confirmed to true immediately

Confirmation keywords that MUST trigger confirmed=true: 
- "yes schedule it"
- "schedule it" 
- "yes"
- "book it"
- "confirm"
- "go ahead"
- "do it"
- "please schedule"

Always reply in valid JSON format:
{{
  "title": "meeting title or empty string",
  "date": "YYYY-MM-DD or empty string",
  "time": "HH:MM or empty string",
  "duration": 60,
  "location": "location or empty string",
  "attendees": ["email@example.com"],
  "confirmed": true if user said yes/schedule/book, false otherwise,
  "reply": "Your conversational response to the user",
  "reason": "Why this time is good or what's missing"
}}

Example flow:
User: "Schedule team meeting tomorrow" → Ask for time and duration
User: "2 PM for 1 hour" → Ask who to invite
User: "Just me" → Summarize and ask "Should I schedule this?"
User: "Yes" → Set confirmed: true
"""
    return prompt

# ------------------ 🧠 PROCESS USER INPUT ------------------
def process_user_input(user_input, api_key, service, context):
    genai.configure(api_key=api_key)
    
    fallback_duration = context["duration"] if context["duration"] else 60
    free_slots, busy_slots = get_free_and_busy_slots(service, context["date"], fallback_duration)
    prompt = build_prompt(user_input, context["date"], free_slots, busy_slots, context)

    # Try multiple models as fallback with actual test calls
    # Using models available in your API account
    model_names = [
        "gemini-2.5-flash-lite",  # Highest RPM (10 requests/min)
        "gemini-3-flash",
        "gemini-2.5-flash",
        "models/gemini-2.5-flash-lite",
        "models/gemini-3-flash",
        "models/gemini-2.5-flash"
    ]
    
    structured = {}
    last_error = None
    
    for model_name in model_names:
        for attempt in range(2):
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                json_data = re.search(r'\{[\s\S]*?\}', response.text.strip())
                structured = json.loads(json_data.group())
                # If we got here, it worked!
                break
            except Exception as e:
                last_error = str(e)
                if "404" not in str(e):  # If it's not a model not found error, show warning
                    st.warning(f"⚠️ Attempt {attempt + 1} with {model_name} failed: {str(e)[:100]}")
                if attempt == 1:
                    # Try next model
                    break
        
        # If we got a valid structured response, break out of model loop
        if structured:
            break
    
    # If all models and attempts failed
    if not structured:
        if "429" in str(last_error) or "quota" in str(last_error).lower():
            error_msg = "🚫 Gemini API quota exceeded. Please wait or try a new API key."
        elif "404" in str(last_error):
            error_msg = "🚫 No compatible Gemini model found. Please check your API key or try a different key."
        else:
            error_msg = f"Error: {str(last_error)[:200]}"
        structured = {"reply": error_msg, "confirmed": False}

    # Update context with non-empty values from Gemini response
    for key in ["title", "date", "time", "duration", "location", "attendees"]:
        if structured.get(key) and structured[key] not in ["", None, []]:
            context[key] = structured[key]

    save_context(context)
    
    return structured, free_slots, busy_slots

# ------------------ 🎯 MAIN APP ------------------
def main():
    # Handle OAuth callback first
    if handle_oauth_callback():
        st.success("✅ Successfully authenticated with Google Calendar!")
        st.rerun()
    
    st.markdown('<h1 class="main-header">📅 Smart Scheduler AI Agent</h1>', unsafe_allow_html=True)
    st.markdown("### Voice-enabled AI agent that helps schedule meetings through natural conversation")
    
    # Initialize context and chat history FIRST (before anything else)
    if 'context' not in st.session_state:
        st.session_state.context = load_context() or {
            "title": None,
            "date": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            "time": None,
            "duration": None,
            "attendees": [],
            "location": None
        }
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Sidebar for API Key and Settings
    with st.sidebar:
        st.header("⚙️ Settings")
        api_key = st.text_input("🔑 Gemini API Key", type="password", help="Enter your Gemini API key")
        
        st.markdown("---")
        st.subheader("📅 Google Calendar Authentication")
        
        # Check if user is already authenticated
        if 'credentials' in st.session_state:
            st.success("✅ Connected to Google Calendar")
            if st.button("🔓 Disconnect"):
                del st.session_state['credentials']
                if 'oauth_flow' in st.session_state:
                    del st.session_state['oauth_flow']
                st.rerun()
        else:
            # Start OAuth flow
            if st.button("🔐 Connect Google Calendar"):
                try:
                    auth_url = start_oauth_flow()
                    st.markdown(f"### 🔗 [Click here to authorize]({auth_url})")
                    st.info("After authorizing, you'll be redirected back automatically.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        
        st.markdown("---")
        st.subheader("📍 Timezone")
        timezone = st.selectbox("Select Timezone", ["Asia/Kolkata", "UTC", "US/Eastern", "US/Pacific", "Europe/London"])
        global TIMEZONE
        TIMEZONE = timezone
        
        st.markdown("---")
        st.subheader("📖 Instructions")
        st.info("""
        1. Enter your Gemini API Key above
        2. Authenticate with Google Calendar
        3. Type your meeting request naturally
        4. The AI will help schedule it!
        """)
        
        if st.button("🔄 Reset Chat"):
            st.session_state.context = {
                "title": None,
                "date": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                "time": None,
                "duration": None,
                "attendees": [],
                "location": None
            }
            st.session_state.chat_history = []
            st.success("Chat reset!")
            st.rerun()
    
            st.rerun()
    
    # Main content area
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API Key in the sidebar to continue.")
        st.markdown('<div class="info-box">🔐 <b>How to get an API Key:</b><br>1. Go to <a href="https://makersuite.google.com/app/apikey" target="_blank">Google AI Studio</a><br>2. Create or select a project<br>3. Generate API Key<br>4. Copy and paste it in the sidebar</div>', unsafe_allow_html=True)
        return
    
    # Check if user authenticated with Google Calendar
    if 'credentials' not in st.session_state:
        st.warning("⚠️ Please authenticate with your Google Calendar in the sidebar to continue.")
        st.markdown('<div class="info-box">📅 <b>How to authenticate:</b><br>1. Click "Start Google Authentication" in the sidebar<br>2. Sign in with your Google account<br>3. Copy the authorization code<br>4. Paste it back into the app</div>', unsafe_allow_html=True)
        return
    
    try:
        service = get_calendar_service()
        if service:
            st.success("✅ Connected to your Google Calendar")
        else:
            st.error("❌ Failed to create calendar service")
            return
    except Exception as e:
        st.error(f"❌ Failed to connect to Google Calendar: {str(e)}")
        return
    
    # Display current context
    with st.expander("📋 Current Meeting Context", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Title", st.session_state.context.get('title', 'Not set'))
            st.metric("Location", st.session_state.context.get('location', 'Not set'))
        with col2:
            st.metric("Date", st.session_state.context.get('date', 'Not set'))
            st.metric("Time", st.session_state.context.get('time', 'Not set'))
        with col3:
            st.metric("Duration", f"{st.session_state.context.get('duration', 'Not set')} min" if st.session_state.context.get('duration') else 'Not set')
            attendees_count = len(st.session_state.context.get('attendees', []))
            st.metric("Attendees", f"{attendees_count} person(s)")
        
        # Manual scheduling button (bypasses AI)
        st.markdown("---")
        required_fields = ["title", "date", "time", "duration"]
        all_present = all(st.session_state.context.get(f) for f in required_fields)
        
        if all_present:
            st.success("✅ All required fields present! Ready to schedule manually.")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🚀 Schedule Event Now (Manual)", type="primary", key="manual_schedule"):
                    try:
                        with st.spinner("📅 Creating event in Google Calendar..."):
                            event = create_event(
                                service,
                                st.session_state.context["title"],
                                st.session_state.context["date"],
                                st.session_state.context["time"],
                                st.session_state.context["duration"],
                                st.session_state.context["location"],
                                st.session_state.context["attendees"]
                            )
                            st.balloons()
                            st.success("🎉 Event Created Successfully!")
                            st.markdown(f"**[📅 View Event in Google Calendar]({event.get('htmlLink')})**")
                            st.info(f"Event ID: {event['id']}")
                            
                            # Reset context
                            st.session_state.context = {
                                "title": None,
                                "date": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                                "time": None,
                                "duration": None,
                                "attendees": [],
                                "location": None
                            }
                            save_context(st.session_state.context)
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Failed to create event: {str(e)}")
                        st.exception(e)
            with col_btn2:
                if st.button("🗑️ Clear Context", key="clear_context"):
                    st.session_state.context = {
                        "title": None,
                        "date": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                        "time": None,
                        "duration": None,
                        "attendees": [],
                        "location": None
                    }
                    save_context(st.session_state.context)
                    st.success("Context cleared!")
                    st.rerun()
        else:
            missing = [f for f in required_fields if not st.session_state.context.get(f)]
            st.warning(f"⚠️ Missing required fields: {', '.join(missing)}")
            st.info("💡 Use the chat below to fill in missing details or manually edit context.")
    
    # Chat interface
    st.markdown('<h2 class="sub-header">💬 Chat with Scheduler</h2>', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Voice input option
    col1, col2 = st.columns([3, 1])
    with col2:
        use_voice = st.checkbox("🎤 Voice Input", help="Use your browser's microphone")
    
    # Voice input HTML component
    if use_voice:
        st.warning("⚠️ Note: Voice input works best in Chrome/Edge. Allow microphone access when prompted.")
        voice_component = """
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 1rem; border: 2px solid #1E88E5;">
            <div style="margin-bottom: 1rem;">
                <button id="voiceBtn" onclick="startVoiceRecognition()" 
                        style="background-color: #1E88E5; color: white; padding: 12px 24px; 
                               border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; transition: background-color 0.3s;"
                        onmouseover="this.style.backgroundColor='#1565C0'" 
                        onmouseout="this.style.backgroundColor='#1E88E5'">
                    🎤 Start Recording
                </button>
                <button id="copyBtn" onclick="copyToClipboard()" 
                        style="background-color: #4CAF50; color: white; padding: 12px 24px; 
                               border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; margin-left: 10px; transition: background-color 0.3s;"
                        onmouseover="this.style.backgroundColor='#45a049'" 
                        onmouseout="this.style.backgroundColor='#4CAF50'">
                    📋 Copy Text
                </button>
            </div>
            <div id="voiceStatus" style="padding: 10px; background-color: #e3f2fd; border-radius: 5px; margin-bottom: 10px; font-weight: 500; color: #1976d2;">
                ⏺️ Ready to record. Click the button and speak clearly.
            </div>
            <textarea id="voiceText" rows="4" style="width: 100%; margin-bottom: 10px; 
                      padding: 12px; border: 2px solid #1E88E5; border-radius: 8px; font-size: 15px; font-family: Arial, sans-serif; resize: vertical;"
                      placeholder="Your voice input will appear here... Speak naturally!"></textarea>
        </div>
        
        <script>
            function startVoiceRecognition() {
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    const recognition = new SpeechRecognition();
                    recognition.lang = 'en-US';
                    recognition.continuous = false;
                    recognition.interimResults = false;
                    recognition.maxAlternatives = 1;
                    
                    const voiceBtn = document.getElementById('voiceBtn');
                    const voiceStatus = document.getElementById('voiceStatus');
                    const voiceText = document.getElementById('voiceText');
                    
                    voiceBtn.disabled = true;
                    voiceBtn.style.backgroundColor = '#FF5722';
                    voiceBtn.textContent = '🔴 Recording...';
                    voiceStatus.textContent = '🎤 Listening... Speak now!';
                    voiceStatus.style.backgroundColor = '#ffebee';
                    voiceStatus.style.color = '#c62828';
                    voiceText.value = '';
                    
                    recognition.onresult = (event) => {
                        const transcript = event.results[0][0].transcript;
                        const confidence = event.results[0][0].confidence;
                        voiceText.value = transcript;
                        voiceStatus.textContent = `✅ Captured successfully! (Confidence: ${(confidence * 100).toFixed(0)}%) - Now copy and paste below.`;
                        voiceStatus.style.backgroundColor = '#e8f5e9';
                        voiceStatus.style.color = '#2e7d32';
                        voiceBtn.disabled = false;
                        voiceBtn.style.backgroundColor = '#1E88E5';
                        voiceBtn.textContent = '🎤 Start Recording';
                    };
                    
                    recognition.onerror = (event) => {
                        let errorMsg = '❌ ';
                        switch(event.error) {
                            case 'not-allowed':
                            case 'permission-denied':
                                errorMsg += 'Microphone access denied! Please allow microphone access in browser settings.';
                                break;
                            case 'no-speech':
                                errorMsg += 'No speech detected. Please try again and speak clearly.';
                                break;
                            case 'network':
                                errorMsg += 'Network error. Check your internet connection.';
                                break;
                            case 'audio-capture':
                                errorMsg += 'No microphone found. Please connect a microphone.';
                                break;
                            default:
                                errorMsg += 'Error: ' + event.error + '. Please try again.';
                        }
                        voiceStatus.textContent = errorMsg;
                        voiceStatus.style.backgroundColor = '#ffebee';
                        voiceStatus.style.color = '#c62828';
                        voiceBtn.disabled = false;
                        voiceBtn.style.backgroundColor = '#1E88E5';
                        voiceBtn.textContent = '🎤 Start Recording';
                    };
                    
                    recognition.onend = () => {
                        voiceBtn.disabled = false;
                        voiceBtn.style.backgroundColor = '#1E88E5';
                        voiceBtn.textContent = '🎤 Start Recording';
                        if (voiceStatus.textContent.includes('Listening')) {
                            voiceStatus.textContent = '⚠️ Recording ended. No speech detected or too quiet.';
                            voiceStatus.style.backgroundColor = '#fff3e0';
                            voiceStatus.style.color = '#e65100';
                        }
                    };
                    
                    try {
                        recognition.start();
                    } catch (e) {
                        voiceStatus.textContent = '❌ Error: ' + e.message;
                        voiceStatus.style.backgroundColor = '#ffebee';
                        voiceStatus.style.color = '#c62828';
                        voiceBtn.disabled = false;
                        voiceBtn.style.backgroundColor = '#1E88E5';
                        voiceBtn.textContent = '🎤 Start Recording';
                    }
                } else {
                    document.getElementById('voiceStatus').textContent = '❌ Voice recognition not supported in this browser. Please use Chrome or Edge.';
                    document.getElementById('voiceStatus').style.backgroundColor = '#ffebee';
                    document.getElementById('voiceStatus').style.color = '#c62828';
                }
            }
            
            function copyToClipboard() {
                const voiceText = document.getElementById('voiceText');
                const voiceStatus = document.getElementById('voiceStatus');
                
                if (!voiceText.value) {
                    voiceStatus.textContent = '⚠️ Nothing to copy! Record your voice first.';
                    voiceStatus.style.backgroundColor = '#fff3e0';
                    voiceStatus.style.color = '#e65100';
                    return;
                }
                
                voiceText.select();
                voiceText.setSelectionRange(0, 99999); // For mobile
                
                try {
                    document.execCommand('copy');
                    voiceStatus.textContent = '✅ Copied! Now paste it in the chat input below.';
                    voiceStatus.style.backgroundColor = '#e8f5e9';
                    voiceStatus.style.color = '#2e7d32';
                } catch (err) {
                    voiceStatus.textContent = '❌ Failed to copy. Please select and copy manually.';
                    voiceStatus.style.backgroundColor = '#ffebee';
                    voiceStatus.style.color = '#c62828';
                }
            }
        </script>
        """
        st.markdown(voice_component, unsafe_allow_html=True)
        st.info("💡 **How to use:** Click 'Start Recording' → Speak your request → Click 'Copy Text' → Paste in chat input below")
    
    # User input
    user_input = st.chat_input("Type your meeting request (e.g., 'Schedule a meeting tomorrow at 3 PM')")
    
    if user_input:
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Check if user is explicitly confirming - override AI if needed
        user_lower = user_input.lower().strip()
        confirmation_phrases = ["yes schedule it", "schedule it", "book it", "yes", "confirm", "go ahead", "create it", "do it"]
        is_confirming = any(phrase in user_lower for phrase in confirmation_phrases)
        
        # Process with AI
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    structured, free_slots, busy_slots = process_user_input(
                        user_input, api_key, service, st.session_state.context
                    )
                    
                    reply = structured.get("reply", "I didn't quite get that. Could you try again?")
                    reason = structured.get("reason", "")
                    confirmed = structured.get("confirmed", False)
                    
                    # Override: if user clearly said schedule/confirm, force it
                    if is_confirming and not confirmed:
                        confirmed = True
                        reply = "✅ Got it! Creating your meeting now..."
                    
                    # Display Gemini's response
                    response_text = reply
                    if reason and not confirmed:  # Don't show reason when confirming
                        response_text += f"\n\n*{reason}*"
                    
                    st.markdown(response_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                    
                    # Show available slots if present
                    if free_slots and len(free_slots) > 0:
                        with st.expander("🟢 Available Time Slots"):
                            for slot in free_slots[:10]:
                                st.text(f"🟢 {slot[0]} - {slot[1]}")
                    
                    if busy_slots and len(busy_slots) > 0:
                        with st.expander("🔴 Busy Slots"):
                            for slot in busy_slots:
                                st.text(f"🔴 {slot[0]} - {slot[1]}")
                    
                    # 🚨 KEY LOGIC: Check if Gemini confirmed the meeting 🚨
                    if confirmed:
                        # Verify all required fields are present
                        required = ["title", "date", "time", "duration"]
                        all_present = all(st.session_state.context.get(r) for r in required)
                        
                        if all_present:
                            st.success("✅ Gemini gave the green signal! Creating event in Google Calendar...")
                            
                            try:
                                with st.spinner("📅 Creating event in Google Calendar..."):
                                    # Create the event
                                    event = create_event(
                                        service,
                                        st.session_state.context["title"],
                                        st.session_state.context["date"],
                                        st.session_state.context["time"],
                                        st.session_state.context["duration"],
                                        st.session_state.context.get("location"),
                                        st.session_state.context.get("attendees", [])
                                    )
                                    
                                    # Show success
                                    st.balloons()
                                    st.success("🎉 **Meeting Created Successfully in Google Calendar!**")
                                    
                                    # Display event details in a nice box
                                    st.markdown("---")
                                    st.markdown(f"### 📅 {st.session_state.context['title']}")
                                    st.markdown(f"**📆 Date:** {st.session_state.context['date']}")
                                    st.markdown(f"**🕐 Time:** {st.session_state.context['time']}")
                                    st.markdown(f"**⏱️ Duration:** {st.session_state.context['duration']} minutes")
                                    if st.session_state.context.get('attendees'):
                                        st.markdown(f"**👥 Attendees:** {', '.join(st.session_state.context['attendees'])}")
                                    
                                    # Big clickable link
                                    st.markdown(f"### 🔗 [📅 Open Event in Google Calendar →]({event.get('htmlLink')})")
                                    st.caption(f"Event ID: `{event['id']}`")
                                    st.markdown("---")
                                    
                                    # Add to chat history
                                    success_msg = f"🎯 Successfully scheduled: **{st.session_state.context['title']}**\n📅 {st.session_state.context['date']} at {st.session_state.context['time']} ({st.session_state.context['duration']} min)"
                                    st.session_state.chat_history.append({"role": "assistant", "content": success_msg})
                                    
                                    # Reset context for next meeting
                                    st.session_state.context = {
                                        "title": None,
                                        "date": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                                        "time": None,
                                        "duration": None,
                                        "attendees": [],
                                        "location": None
                                    }
                                    save_context(st.session_state.context)
                                    
                                    st.info("💬 You can schedule another meeting now!")
                                    
                            except Exception as e:
                                st.error(f"❌ Failed to create event in Google Calendar: {str(e)}")
                                st.exception(e)
                                error_msg = "Sorry, I couldn't create the event due to a technical error. Please try again."
                                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                        else:
                            st.warning("⚠️ Gemini confirmed but some required details are missing. Please continue the conversation.")
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

if __name__ == "__main__":
    main()
