import os
import tempfile
import streamlit as st
from gtts import gTTS
from playsound import playsound
import io

def speak_text_gtts(text: str, lang='id'):
    """
    Text-to-Speech menggunakan Google TTS (gratis)
    """
    try:
        # Generate audio menggunakan gTTS
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Simpan ke temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            # Putar audio
            playsound(tmp_path)
        finally:
            # Hapus temporary file
            try:
                os.remove(tmp_path)
            except OSError:
                pass
                
    except Exception as e:
        st.error(f"Error dalam TTS: {e}")
