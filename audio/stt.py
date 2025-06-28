import streamlit as st
import speech_recognition as sr
import os
from streamlit_audio_recorder import audio_recorder
import io
import tempfile

def is_cloud_environment():
    """Deteksi apakah running di cloud environment"""
    return (
        os.getenv('STREAMLIT_SHARING_MODE') or 
        os.getenv('STREAMLIT_CLOUD') or
        'streamlit.app' in os.getenv('HOSTNAME', '') or
        'herokuapp.com' in os.getenv('HOSTNAME', '')
    )

def has_pyaudio():
    """Check apakah PyAudio tersedia"""
    try:
        import pyaudio
        return True
    except ImportError:
        return False

def recognize_speech_from_mic():
    """Original function - hanya untuk local development"""
    if is_cloud_environment() or not has_pyaudio():
        st.error("🚨 Mikrofon tidak tersedia di cloud environment")
        return None
    
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎤 Silakan bicara...")
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        
        with st.spinner("🤔 Memproses suara..."):
            text = r.recognize_google(audio, language="id-ID")
            return text
            
    except sr.UnknownValueError:
        return "Maaf, tidak bisa mengenali suara."
    except sr.RequestError as e:
        return f"Error dengan STT: {e}"
    except Exception as e:
        return f"Error: {e}"

def recognize_speech_from_recorder():
    """Menggunakan streamlit-audio-recorder untuk cloud"""
    
    audio_bytes = audio_recorder(
        text="🎤 Klik untuk merekam",
        recording_color="#ff6b6b",
        neutral_color="#667eea",
        icon_name="microphone",
        icon_size="2x",
        key="speech_recorder"
    )
    
    if audio_bytes:
        try:
            # Save audio bytes to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_bytes)
                tmp_file_path = tmp_file.name
            
            # Process with speech recognition
            r = sr.Recognizer()
            with sr.AudioFile(tmp_file_path) as source:
                audio = r.record(source)
            
            # Clean up temp file
            os.unlink(tmp_file_path)
            
            # Recognize speech
            with st.spinner("🤔 Memproses suara..."):
                text = r.recognize_google(audio, language="id-ID")
                return text
                
        except sr.UnknownValueError:
            return "Maaf, tidak bisa mengenali suara."
        except sr.RequestError as e:
            return f"Error dengan STT: {e}"
        except Exception as e:
            return f"Error: {e}"
    
    return None

def recognize_speech_from_upload():
    """Upload file audio untuk STT"""
    
    uploaded_file = st.file_uploader(
        "📁 Upload file audio", 
        type=['wav', 'mp3', 'm4a', 'ogg'],
        help="Upload file audio untuk diconvert ke teks"
    )
    
    if uploaded_file is not None:
        try:
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name
            
            # Process with speech recognition
            r = sr.Recognizer()
            
            # Convert to wav if needed using pydub
            if not uploaded_file.name.endswith('.wav'):
                try:
                    from pydub import AudioSegment
                    audio_segment = AudioSegment.from_file(tmp_file_path)
                    wav_path = tmp_file_path.replace(tmp_file_path.split('.')[-1], 'wav')
                    audio_segment.export(wav_path, format="wav")
                    os.unlink(tmp_file_path)
                    tmp_file_path = wav_path
                except ImportError:
                    st.warning("⚠️ Untuk format selain WAV, install pydub: pip install pydub")
            
            with sr.AudioFile(tmp_file_path) as source:
                audio = r.record(source)
            
            # Clean up temp file
            os.unlink(tmp_file_path)
            
            # Recognize speech
            with st.spinner("🤔 Memproses file audio..."):
                text = r.recognize_google(audio, language="id-ID")
                return text
                
        except sr.UnknownValueError:
            return "Maaf, tidak bisa mengenali suara dari file."
        except sr.RequestError as e:
            return f"Error dengan STT: {e}"
        except Exception as e:
            return f"Error: {e}"
    
    return None

def get_speech_input():
    """Main function untuk mendapatkan input suara dengan multiple options"""
    
    st.markdown("### 🎤 Input Suara")
    
    # Tab untuk different input methods
    tab1, tab2 = st.tabs(["🎙️ Rekam Suara", "📁 Upload File"])
    
    with tab1:
        if is_cloud_environment() or not has_pyaudio():
            st.info("🌐 Menggunakan audio recorder (cocok untuk cloud)")
            return recognize_speech_from_recorder()
        else:
            st.info("🖥️ Menggunakan mikrofon langsung (local development)")
            if st.button("🎤 Mulai Rekam", key="mic_button"):
                return recognize_speech_from_mic()
    
    with tab2:
        return recognize_speech_from_upload()
    
    return None
