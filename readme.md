# 🤖 Smart Scheduler AI Agent

A voice-enabled AI agent that helps users schedule meetings through natural conversation and integrates with Google Calendar.

## 🎯 Features

- ✅ Voice-to-Text and Text-to-Speech
- ✅ Memory across conversation turns
- ✅ Gemini LLM-powered prompt reasoning
- ✅ Free/busy slot detection with Google Calendar API
- ✅ Smart suggestions and confirmation prompts
- ✅ Natural parsing of vague inputs (e.g. “after lunch tomorrow”)

## 📦 Tech Stack

- Python + Gemini 2.5 Flash
- SpeechRecognition + pyttsx3
- Google Calendar API
- Context memory with Pickle

## 🧠 How It Works

1. User speaks request (e.g. “Book a meeting Friday evening”)
2. LLM parses vague/ambiguous requests, fills missing info
3. Checks availability with Calendar API
4. Confirms with user before scheduling
5. Event is added if confirmed

## 🚀 Setup Instructions

1. Clone repo and install requirements:
```bash
pip install -r requirements.txt
