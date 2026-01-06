"""
Test script to manually create an event using the context data
"""
import pickle
import datetime
import pytz
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']
TIMEZONE = "Asia/Kolkata"

# Load context
with open('context.pkl', 'rb') as f:
    context = pickle.load(f)

print("=" * 60)
print("🧪 TESTING EVENT CREATION WITH ACTUAL CONTEXT DATA")
print("=" * 60)
print("\n📋 Context Data:")
print(f"   Title: {context['title']}")
print(f"   Date: {context['date']}")
print(f"   Time: {context['time']}")
print(f"   Duration: {context['duration']} minutes")
print(f"   Attendees: {context['attendees']}")
print(f"   Location: {context['location']}")

# Get calendar service
print("\n🔐 Authenticating...")
creds = Credentials.from_authorized_user_file('token.json', SCOPES)
service = build('calendar', 'v3', credentials=creds)
print("✅ Authenticated!")

# Create event
print("\n📅 Creating event...")
tz = pytz.timezone(TIMEZONE)
start = tz.localize(datetime.datetime.strptime(f"{context['date']} {context['time']}", "%Y-%m-%d %H:%M"))
end = start + datetime.timedelta(minutes=context['duration'])

event = {
    'summary': context['title'],
    'start': {'dateTime': start.isoformat(), 'timeZone': TIMEZONE},
    'end': {'dateTime': end.isoformat(), 'timeZone': TIMEZONE},
}

if context['location']:
    event['location'] = context['location']
    
if context['attendees']:
    event['attendees'] = [{'email': a} for a in context['attendees']]

print(f"\n🔍 Event payload:")
import json
print(json.dumps(event, indent=2))

try:
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print("\n✅✅✅ EVENT CREATED SUCCESSFULLY!")
    print(f"   Event ID: {created_event['id']}")
    print(f"   Title: {created_event['summary']}")
    print(f"   Start: {created_event['start']['dateTime']}")
    print(f"   Link: {created_event.get('htmlLink')}")
    print("\n🎉 The event is now in your Google Calendar!")
    
except Exception as e:
    print(f"\n❌ FAILED TO CREATE EVENT:")
    print(f"   Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
