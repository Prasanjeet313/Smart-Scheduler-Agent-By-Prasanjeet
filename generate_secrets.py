"""
Helper script to convert token.json to Streamlit secrets format
Run this locally after authenticating to generate the secrets configuration
"""
import json

print("=" * 60)
print("GENERATING STREAMLIT SECRETS CONFIGURATION")
print("=" * 60)

try:
    with open('token.json', 'r') as f:
        token_data = json.load(f)
    
    print("\n✅ Found token.json. Copy the following to your Streamlit secrets:\n")
    print("=" * 60)
    print("[google_credentials]")
    
    for key, value in token_data.items():
        if isinstance(value, str):
            print(f'{key} = "{value}"')
        elif isinstance(value, list):
            print(f'{key} = {json.dumps(value)}')
        else:
            print(f'{key} = {json.dumps(value)}')
    
    print("=" * 60)
    print("\n📋 INSTRUCTIONS:")
    print("1. Go to your Streamlit app settings")
    print("2. Navigate to 'Secrets' section")
    print("3. Copy and paste the above configuration")
    print("4. Also add: GEMINI_API_KEY = \"your_api_key_here\"")
    print("\n" + "=" * 60)
    
except FileNotFoundError:
    print("\n❌ ERROR: token.json not found!")
    print("\nPlease run the app locally first to generate token.json:")
    print("1. Make sure credentials.json exists")
    print("2. Run: streamlit run app.py")
    print("3. Complete the Google OAuth authentication")
    print("4. Run this script again")
    print("\n" + "=" * 60)
