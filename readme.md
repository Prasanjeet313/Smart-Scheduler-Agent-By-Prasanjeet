# Smart Scheduler AI Agent

A voice-enabled AI agent that helps users schedule meetings through natural conversation and integrates with Google Calendar.

## Features

- Voice-to-Text and Text-to-Speech
- Memory across conversation turns
- Gemini LLM-powered prompt reasoning
- Free/busy slot detection with Google Calendar API
- Smart suggestions and confirmation prompts
- Natural parsing of vague inputs (e.g. “after lunch tomorrow”)

## Tech Stack

- Python + Gemini 2.5 Flash
- SpeechRecognition + pyttsx3
- Google Calendar API
- Context memory with Pickle

## How It Works

1. User speaks request (e.g. “Book a meeting Friday evening”)
2. LLM parses vague/ambiguous requests, fills missing info
3. Checks availability with Calendar API
4. Confirms with user before scheduling
5. Event is added if confirmed
##  Design Choices
Orchestration in Python to control STT, TTS, Gemini, and Calendar.

Prompt design is flexible and includes available/busy slots in context.

State persistence via Pickle allows resuming interrupted conversations.

Fallback & conflict handling using Gemini retries and alternative slot suggestion logic.

Modular structure: Easily extendable to recurring events, reminders, or multiple calendars.

##  Setup Instructions

1. Clone repo and install requirements:
  ```pip install -r requirements.txt```
2. Setup environment variables:
  Create a .env file:
  ```GEMINI_API_KEY=your_gemini_api_key```
3. Add Google Calendar credentials ---> Go to Google Cloud Console---->Enable Google Calendar API---->Download ```credentials.json``` and place it in the project root
4. Run the assistant:
  ```python main.ipynb```
