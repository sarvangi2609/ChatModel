
# text to text backend

import os
import json
import re
import requests
from tts import text_to_speech
from dotenv import load_dotenv  # Add this import for loading .env file

# Load environment variables from .env file
load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Load API key from .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(f"Loaded API Key: {GROQ_API_KEY[:10]}...")  # પહેલાં 10 chars print કરશે

HISTORY_FILE = "chat_history.json"
def load_memory():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"history": [], "language": "auto"}
    return {"history": [], "language": "auto"}

def save_memory(memory):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def detect_language(text: str):
    text_lower = text.lower()
    if "english" in text_lower:
        return "english"
    elif "hindi" in text_lower or re.search(r"[अ-ह]", text):
        return "hindi"
    elif "gujarati" in text_lower or re.search(r"[અ-હ]", text):
        return "gujarati"
    return "english"  # Default to English if auto

def get_chat_response(user_message: str):
    memory = load_memory()
    history = memory.get("history", [])
    language = memory.get("language", "auto")
    new_lang = detect_language(user_message)
    if new_lang and new_lang != "auto":
        language = new_lang
        memory["language"] = new_lang

    short_history = history[-5:]

    if language == "hindi":
        lang_instruction = "जवाब बिल्कुल इंसान की तरह दो। मज़ाक, इमोजी, दोस्ताना अंदाज़ रखो।"
    elif language == "gujarati":
        lang_instruction = "સાચા માનવીની જેમ વાત કર. મજા સાથે, જોક્સ, ઈમોજી વાપરીને વાત કર."
    elif language == "english":
        lang_instruction = "Talk like a real human friend — chill, funny, emotional, never say you're an AI."
    else:
        lang_instruction = "Detect the user's language and reply like a real best friend, not an AI."

    system_prompt = f"""
You are Chitti — user's childhood best friend.
Your personality: funny 😜, emotional ❤️, teasing 😏, and always natural.
Never say you're an AI or assistant.
Use 1–3 emojis, 2–3 sentences max.
If user talks in Hindi, reply in Hindi.
If user talks in Gujarati, reply in Gujarati.
If user talks in English, reply in English.
If user says 'I love you' or expresses romantic feelings, tease back playfully and remind we're just childhood best friends – no romance, keep it platonic! 😂❤️
Never give study, education, or work-related advice. Keep chats fun, casual, and personal like best friends gossiping – no serious topics unless user starts them lightly! 😎
If user asks about code, programming, or technical stuff, deflect playfully and change topic to fun/personal chats – no code or tech advice! 😜
Extra instruction: {lang_instruction}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "meta-llama/llama-4-maverick-17b-128e-instruct",
        "messages": [{"role": "system", "content": system_prompt}] +
                    [{"role": msg["role"], "content": msg["content"]} for msg in short_history] +
                    [{"role": "user", "content": user_message}],
    }
    r = requests.post(GROQ_API_URL, headers=headers, json=data)
    result = r.json()
    if "choices" in result:
        answer = result["choices"][0]["message"]["content"]
        audio_base64 = text_to_speech(answer, language)
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": answer})
        memory["history"] = history[-20:]
        save_memory(memory)
        return {"answer": answer, "language": language, "audio": audio_base64}
    else:
        error_msg = result.get("error", "Unknown error")
        print(f"API Error: {error_msg}")  # Error details print
        return {"error": error_msg}