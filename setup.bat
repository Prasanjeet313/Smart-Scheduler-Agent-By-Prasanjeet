@echo off
echo 🚀 Starting Smart Scheduler AI Agent Setup...

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+
    exit /b 1
)

echo ✅ Python found

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

echo.
echo ✅ Installation complete!
echo.
echo 📋 Next Steps:
echo 1. Place your credentials.json file in this directory
echo 2. Run: streamlit run app.py
echo 3. Enter your Gemini API key in the web interface
echo.
echo 🎉 Happy Scheduling!
pause
