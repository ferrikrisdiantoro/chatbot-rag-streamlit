import io
import streamlit as st
from gtts import gTTS

def speak_text(text: str, lang: str = "id"):
    try:
        mp3_buffer = io.BytesIO()
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)
        
        # Tambahan autoplay=True untuk langsung memutar
        st.audio(mp3_buffer.read(), format="audio/mp3", autoplay=True)
        
    except Exception as e:
        st.error(f"Error dalam TTS: {e}")
