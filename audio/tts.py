import io
import streamlit as st
from gtts import gTTS

def speak_text(text: str, lang: str = "id"):
    """
    Text-to-Speech menggunakan gTTS, memutar via Streamlit audio player.
    """
    try:
        # 1) Buat buffer in-memory
        mp3_buffer = io.BytesIO()
        
        # 2) Generate audio dengan gTTS dan tulis ke buffer
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)
        
        # 3) Tampilkan audio player di browser user
        st.audio(mp3_buffer.read(), format="audio/mp3")
        
    except Exception as e:
        st.error(f"Error dalam TTS: {e}")
