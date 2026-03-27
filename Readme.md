# EVA – Enhanced Virtual Assistant

EVA is a futuristic desktop AI assistant built with Python and Tkinter.  
It combines a sci-fi style interface with voice input, text chat, text-to-speech, local memory, web actions, Mac controls, optional camera vision, and Gemini AI integration.

## Features

- Futuristic animated desktop interface
- Text-based chat input
- Voice input using microphone
- Spoken replies using text-to-speech
- Continuous voice conversation mode
- Local memory using SQLite
- Remembers basic user facts like name
- Optional Gemini AI support for smarter responses
- Local fallback mode when Gemini is unavailable
- Web search and browser shortcuts
- Open apps like Chrome, VS Code, and Spotify
- Mac system controls such as volume, mute, lock screen, and display sleep
- Optional camera preview using OpenCV
- Live CPU and RAM system display

## Technologies Used

- Python
- Tkinter
- SQLite3
- pyttsx3
- SpeechRecognition
- psutil
- OpenCV
- Google GenAI SDK

## Requirements

Make sure Python 3.10+ is installed.

Install the required libraries:

```bash
pip install psutil pyttsx3 SpeechRecognition opencv-python google-genai pyaudio