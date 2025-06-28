import streamlit as st
from gtts import gTTS
import io

def speak_text(text: str, lang: str = "id"):
    """
    Text-to-Speech menggunakan gTTS, memutar via Streamlit audio player.
    """
    try:
        # Generate audio bytes
        mp3_buffer = io.BytesIO()
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)

        # Tampilkan audio player di UI
        st.audio(mp3_buffer.read(), format="audio/mp3")

    except Exception as e:
        st.error(f"Error dalam TTS: {e}")
