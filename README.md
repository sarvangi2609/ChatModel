
<h5>Chitti - Friendly Voice Chatbot <\h5>

Requirements :

    -Python 3.8+
    -Key Libraries:
        FastAPI & Uvicorn: For the web API server.
        requests: For Groq API calls (text responses).
        SpeechRecognition: For speech-to-text (STT).
        pydub: For audio conversion (WebM to WAV).
        gTTS: For text-to-speech (TTS).
        python-dotenv: For loading API keys from .env.


Install via :
    -pip install fastapi uvicorn requests SpeechRecognition pydub gTTS python-dotenv

Get a free Groq API key from console.groq.com and add to .env:
    -GROQ_API_KEY=your_key_here


Setup & Run :

    1.Clone or create project folder, add these files:
        main.py, ttt.py, stt.py, tts.py, index.html
        .env (with API key)
    2.Install dependencies (above).
    3.Run server:
        uvicorn main:app --reload or uvicorn main:app --reload --host 127.0.0.1 --port 8000
    4.Open http://127.0.0.1:8000/ in browser (Chrome/Firefox for voice).
        Type messages or use mic button for voice chat.
        Responses auto-play audio.

Usage :

    -Text: Enter message, hit send → Gets reply + audio.
    -Voice: Click 🎤 to record → STT converts, processes, plays response.
    -History saved in chat_history.json.

Troubleshooting :

    -STT fails? Check mic perms/internet.
    -API errors? Verify Groq key.
    -Full docs: See project notes or expand this README.

Enjoy chatting with Chitti! 😎 If issues, check console logs.
