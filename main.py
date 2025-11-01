

# main.py (all files includong)

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from ttt import get_chat_response
from stt import speech_to_text
from tts import text_to_speech

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve HTML frontend
@app.get("/", response_class=HTMLResponse)
def chat_page():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    else:
        return "<h1>index.html file not found! Create it in the project root.</h1>"

@app.post("/api/chat")
def chat_api(query: dict = {}):  # Accept dict
    user_message = query.get("message")
    if not user_message:
        return {"error": "No message provided"}
    return get_chat_response(user_message)

@app.post("/api/voice")
async def voice_api(file: UploadFile = File(...)):
    text = speech_to_text(file, lang_hint="gujarati")  # Add this
    if not text:
        return {"error": "Could not recognize speech"}
    
    response = get_chat_response(text)
    response["text"] = text
    return response