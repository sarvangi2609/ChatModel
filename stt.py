
# speech to text backend

from fastapi import UploadFile, File
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os
import re

def detect_audio_language(text_hint: str = ""):
    text_lower = text_hint.lower()
    if re.search(r"[અ-હ]", text_hint) or "gujarati" in text_lower:
        return "gu-IN"
    elif re.search(r"[अ-ह]", text_hint) or "hindi" in text_lower:
        return "hi-IN"
    return "en-IN"  # Default

def speech_to_text(file: UploadFile, lang_hint: str = "gujarati"):  # Default to Gujarati now
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_audio:
            content = file.file.read()
            temp_audio.write(content)
            temp_audio_path = temp_audio.name
        
        # Convert WebM to WAV
        wav_path = temp_audio_path.replace(".webm", ".wav")
        sound = AudioSegment.from_file(temp_audio_path, format="webm")
        sound.export(wav_path, format="wav")
        
        # Recognize speech
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Noise reduction add કર્યું
            audio_data = recognizer.record(source)
            language = detect_audio_language(lang_hint)
            print(f"Trying STT in language: {language}")  # Debug log
            text = recognizer.recognize_google(audio_data, language=language)
        
        # Cleanup
        os.remove(temp_audio_path)
        os.remove(wav_path)
        
        print(f"Recognized text: {text}")  # Debug
        return text
    except sr.UnknownValueError:
        print("STT: Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"STT: Google API error: {e}")
        return None
    except Exception as e:
        print(f"Speech recognition error: {e}")
        return None