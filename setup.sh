#!/bin/bash

echo "🚀 Starting Smart Scheduler AI Agent Setup..."

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python found"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Place your credentials.json file in this directory"
echo "2. Run: streamlit run app.py"
echo "3. Enter your Gemini API key in the web interface"
echo ""
echo "🎉 Happy Scheduling!"
