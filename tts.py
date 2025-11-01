
# text to speech backend

import re
import base64
import io
from gtts import gTTS
import os  # Added for cleanup if needed

def clean_text_for_speech(text: str) -> str:
    """Remove emojis and non-speech elements from text"""
    text = re.sub(r'[^\w\s,\.!?;:()\-—–+*/=@#$%^&]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'([.!?]){2,}', r'\1', text)
    return text.strip()

def text_to_speech(text: str, language: str = "en"):
    try:
        clean_text = clean_text_for_speech(text)
        if not clean_text:
            clean_text = "No text available"
        lang_map = {
            "hindi": "hi",
            "gujarati": "gu",
            "english": "en"
        }
        tts_lang = lang_map.get(language, "en")
        tts = gTTS(text=clean_text, lang=tts_lang, slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
        return audio_base64
    except Exception as e:
        print(f"TTS Error: {e}")
        return None