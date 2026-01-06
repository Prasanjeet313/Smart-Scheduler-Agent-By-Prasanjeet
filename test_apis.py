"""
Test script to verify Gemini API and Google Calendar API are working correctly
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import pytz

# Load environment variables
load_dotenv()

print("=" * 60)
print("🧪 TESTING API CONNECTIONS")
print("=" * 60)

# Test 1: Gemini API
print("\n1️⃣ Testing Gemini API...")
print("-" * 60)
try:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY not found in .env file")
    else:
        print(f"✅ API Key found: {GEMINI_API_KEY[:10]}...")
        
        # Configure and test Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
        # Simple test prompt
        response = model.generate_content("Say 'Hello! I am working correctly!' in exactly 5 words.")
        print(f"📤 Test prompt sent: 'Say Hello in 5 words'")
        print(f"📥 Response received: {response.text.strip()}")
        print("✅ Gemini API is working correctly!")
        
except Exception as e:
    print(f"❌ Gemini API Error: {str(e)}")

# Test 2: Google Calendar API
print("\n2️⃣ Testing Google Calendar API...")
print("-" * 60)
try:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    # Check credentials file
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json not found!")
    else:
        print("✅ credentials.json found")
        
        # Get calendar service
        creds = None
        if os.path.exists('token.json'):
            print("✅ token.json found (already authenticated)")
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        else:
            print("⚠️  token.json not found - starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
            print("✅ Authentication successful! token.json created")
        
        # Build service and test
        service = build('calendar', 'v3', credentials=creds)
        
        # Test: Get calendar list
        print("\n📅 Testing Calendar Access...")
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get('items', [])
        
        if calendars:
            print(f"✅ Found {len(calendars)} calendar(s):")
            for calendar in calendars[:3]:  # Show first 3
                print(f"   - {calendar['summary']}")
        
        # Test: Get events from primary calendar
        print("\n📅 Testing Event Retrieval...")
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            maxResults=5,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        
        print(f"✅ Retrieved {len(events)} upcoming event(s)")
        if events:
            print("   Upcoming events:")
            for event in events[:3]:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"   - {event['summary']} at {start}")
        
        # Test: Check free/busy
        print("\n📅 Testing Free/Busy Query...")
        TIMEZONE = "Asia/Kolkata"
        tz = pytz.timezone(TIMEZONE)
        tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
        start_of_day = tz.localize(datetime.datetime.strptime(tomorrow.strftime("%Y-%m-%d") + " 00:00", "%Y-%m-%d %H:%M"))
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
        print(f"✅ Free/Busy query successful!")
        print(f"   Found {len(busy_times)} busy slot(s) for tomorrow")
        
        # Test: Create a test event
        print("\n📅 Testing Event Creation (Write Permission)...")
        test_start = datetime.datetime.now(tz) + datetime.timedelta(days=7)
        test_end = test_start + datetime.timedelta(hours=1)
        
        test_event = {
            'summary': '🧪 API Test Event - DELETE ME',
            'description': 'This is a test event created by the Smart Scheduler API test. Safe to delete.',
            'start': {
                'dateTime': test_start.isoformat(),
                'timeZone': TIMEZONE,
            },
            'end': {
                'dateTime': test_end.isoformat(),
                'timeZone': TIMEZONE,
            },
        }
        
        try:
            created_event = service.events().insert(calendarId='primary', body=test_event).execute()
            print(f"✅ Test event created successfully!")
            print(f"   Event ID: {created_event['id']}")
            print(f"   Title: {created_event['summary']}")
            print(f"   Link: {created_event.get('htmlLink')}")
            
            # Clean up: Delete the test event
            print("\n🗑️  Cleaning up: Deleting test event...")
            service.events().delete(calendarId='primary', eventId=created_event['id']).execute()
            print("✅ Test event deleted successfully!")
            print("\n✅✅✅ Google Calendar API WRITE permissions confirmed!")
            
        except Exception as create_error:
            print(f"❌ Failed to create test event: {str(create_error)}")
            print("   Check if Calendar API has write permissions enabled")
        
        print("\n✅ Google Calendar API is working correctly!")
        
except Exception as e:
    print(f"❌ Google Calendar API Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("🎉 API TESTING COMPLETE")
print("=" * 60)
