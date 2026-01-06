"""
Installation Verification Script
Run this to check if everything is set up correctly
"""

import sys
import os

def check_python_version():
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_dependencies():
    print("\n📦 Checking dependencies...")
    required = [
        "streamlit",
        "google.generativeai",
        "googleapiclient",
        "google_auth_oauthlib",
        "pytz"
    ]
    
    all_ok = True
    for package in required:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (missing)")
            all_ok = False
    
    return all_ok

def check_files():
    print("\n📁 Checking required files...")
    
    # Check app.py
    if os.path.exists("app.py"):
        print("   ✅ app.py")
    else:
        print("   ❌ app.py (missing)")
        return False
    
    # Check credentials.json
    if os.path.exists("credentials.json"):
        print("   ✅ credentials.json")
        creds_ok = True
    else:
        print("   ⚠️  credentials.json (missing - you need to create this)")
        creds_ok = False
    
    # Check requirements.txt
    if os.path.exists("requirements.txt"):
        print("   ✅ requirements.txt")
    else:
        print("   ❌ requirements.txt (missing)")
        return False
    
    return creds_ok

def main():
    print("=" * 60)
    print("🔍 Smart Scheduler AI Agent - Installation Verification")
    print("=" * 60)
    
    python_ok = check_python_version()
    deps_ok = check_dependencies()
    files_ok = check_files()
    
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print("=" * 60)
    
    if python_ok and deps_ok:
        print("✅ Python & Dependencies: READY")
    else:
        print("❌ Python & Dependencies: NOT READY")
        print("   Run: pip install -r requirements.txt")
    
    if files_ok:
        print("✅ Required Files: READY")
    else:
        print("⚠️  Required Files: MISSING")
        print("   Download credentials.json from Google Cloud Console")
    
    print("\n" + "=" * 60)
    
    if python_ok and deps_ok and files_ok:
        print("🎉 ALL SYSTEMS GO!")
        print("\n🚀 Run: streamlit run app.py")
    elif python_ok and deps_ok:
        print("⚠️  Almost ready! Just need credentials.json")
        print("\n📋 Next Steps:")
        print("   1. Go to https://console.cloud.google.com/")
        print("   2. Enable Google Calendar API")
        print("   3. Download credentials.json")
        print("   4. Place in project folder")
        print("\n   Then run: streamlit run app.py")
    else:
        print("❌ Setup incomplete")
        print("\n📋 Next Steps:")
        print("   1. Run: pip install -r requirements.txt")
        print("   2. Download credentials.json")
        print("   3. Run this script again")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
