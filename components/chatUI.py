import streamlit as st
import io
from gtts import gTTS
# from utils.api import ask_question
# from audio.stt import recognize_speech_from_mic

def speak_text(text: str, lang: str = "id"):
    """
    Text-to-Speech menggunakan gTTS, memutar via Streamlit audio player.
    """
    try:
        # Buat buffer in-memory
        mp3_buffer = io.BytesIO()
        
        # Generate audio dengan gTTS dan tulis ke buffer
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.write_to_fp(mp3_buffer)
        mp3_buffer.seek(0)
        
        # Tampilkan audio player di browser user dengan autoplay
        st.audio(mp3_buffer.read(), format="audio/mp3", autoplay=True)
        
    except Exception as e:
        st.error(f"Error dalam TTS: {e}")

def ask_question(question):
    """Mock function untuk testing - ganti dengan implementasi sebenarnya"""
    import time
    time.sleep(1)  # Simulasi delay API
    
    class MockResponse:
        def __init__(self):
            self.status_code = 200
        
        def json(self):
            return {
                "response": f"Ini adalah jawaban mock untuk pertanyaan: '{question}'. Jawaban ini dibuat untuk testing interface chat.",
                "sources": ["document1.pdf", "document2.txt"]
            }
    
    return MockResponse()

def recognize_speech_from_mic():
    """Mock function untuk testing - ganti dengan implementasi sebenarnya"""
    return "Ini adalah teks mock dari speech recognition"

def render_chat():
    # Page config untuk layout yang lebih baik
    st.set_page_config(
        page_title="Chat with Documents",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS untuk styling yang diperbaiki
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Chat container styling */
    .chat-messages {
        height: 60vh;
        overflow-y: auto;
        padding: 1rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    /* Message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 0.8rem 0;
        margin-left: 20%;
        box-shadow: 0 3px 15px rgba(102, 126, 234, 0.3);
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        line-height: 1.5;
    }
    
    .assistant-message {
        background: white;
        color: #2c3e50;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 0.8rem 0;
        margin-right: 20%;
        box-shadow: 0 3px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #4ecdc4;
        font-family: 'Inter', sans-serif;
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 25px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        min-height: 50px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    /* Mic button */
    .mic-button button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%) !important;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3) !important;
    }
    
    .mic-button button:hover {
        background: linear-gradient(135deg, #ff5252 0%, #e53e3e 100%) !important;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.4) !important;
    }
    
    /* TTS button */
    .tts-button button {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%) !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 1rem !important;
        min-height: 40px !important;
        box-shadow: 0 3px 10px rgba(78, 205, 196, 0.3) !important;
    }
    
    .tts-button button:hover {
        background: linear-gradient(135deg, #3db5ad 0%, #3a8f7c 100%) !important;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.4) !important;
    }
    
    /* Input styling */
    .stChatInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e1e8ed;
        padding: 0.8rem 1.5rem;
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stChatInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Welcome message */
    .welcome-container {
        text-align: center;
        padding: 3rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: 2rem 1rem;
        background: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .header-title {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .header-subtitle {
        font-family: 'Inter', sans-serif;
        color: #666;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        font-weight: 400;
    }
    
    /* Spinner customization */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Toast styling */
    .stToast {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
        border-radius: 15px;
    }
    
    /* Audio player styling */
    audio {
        width: 100%;
        margin: 0.5rem 0;
        border-radius: 10px;
    }
    
    /* Sources styling */
    .sources-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        border-left: 4px solid #4ecdc4;
    }
    
    /* Scrollbar styling */
    .chat-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.1);
        border-radius: 10px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class='header-container'>
        <h1 class='header-title'>💬 Chat with Your Documents</h1>
        <p class='header-subtitle'>Ask questions about your uploaded documents using voice or text</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "mic_input" not in st.session_state:
        st.session_state.mic_input = ""
    
    if "processing" not in st.session_state:
        st.session_state.processing = False

    # Chat messages container
    st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
    
    if st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)
                
                # TTS button untuk assistant messages
                col1, col2, col3 = st.columns([1, 1, 8])
                with col1:
                    if st.button(
                        "🔊 Dengar", 
                        key=f"tts_{i}",
                        help="Bacakan jawaban ini",
                        use_container_width=True
                    ):
                        speak_text(msg["content"])
        
        # Show processing indicator
        if st.session_state.processing:
            st.markdown('<div class="assistant-message">🤔 Sedang berpikir...</div>', unsafe_allow_html=True)
    else:
        # Welcome message
        st.markdown("""
        <div class='welcome-container'>
            <h3 style='margin: 0; font-weight: 600;'>👋 Selamat datang!</h3>
            <p style='margin: 1rem 0 0 0; font-size: 1.1rem; opacity: 0.9;'>
                Mulai percakapan dengan mengetik pertanyaan atau menggunakan mikrofon
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Input section
    st.markdown("---")
    
    # Create columns for input layout
    input_col1, input_col2 = st.columns([5, 1])
    
    with input_col1:
        user_input = st.chat_input("💭 Ketik pertanyaan Anda di sini...")
    
    with input_col2:
        st.markdown('<div class="mic-button">', unsafe_allow_html=True)
        mic_clicked = st.button(
            "🎤", 
            key="mic_button",
            help="Klik untuk berbicara",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Handle microphone input
    if mic_clicked:
        with st.spinner("🎧 Mendengarkan..."):
            try:
                recognized = recognize_speech_from_mic()
                if recognized:
                    st.session_state.mic_input = recognized
                    st.success(f"🗣️ Terdeteksi: '{recognized}'")
                    # Auto-submit the recognized text
                    user_input = recognized
                else:
                    st.warning("❌ Tidak ada suara yang terdeteksi")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    # Process user input
    if user_input and not st.session_state.processing:
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Set processing flag
        st.session_state.processing = True
        
        # Clear mic input
        if "mic_input" in st.session_state:
            st.session_state.mic_input = ""
        
        # Rerun to show user message immediately
        st.rerun()

    # Process AI response jika sedang processing
    if st.session_state.processing:
        # Get the last user message
        last_user_message = next((msg["content"] for msg in reversed(st.session_state.messages) if msg["role"] == "user"), None)
        
        if last_user_message:
            try:
                response = ask_question(last_user_message)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["response"]
                    sources = data.get("sources", [])
                    
                    # Format answer dengan sources jika ada
                    full_answer = answer
                    if sources:
                        full_answer += "\n\n**📄 Sumber:**\n"
                        for i, src in enumerate(sources, 1):
                            full_answer += f"{i}. `{src}`\n"
                    
                    # Add assistant response to session state
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": full_answer
                    })
                    
                else:
                    error_msg = f"❌ Terjadi kesalahan: {response.text}"
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_msg
                    })
                    
            except Exception as e:
                error_msg = f"❌ Error sistem: {str(e)}"
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })
            
            # Reset processing flag
            st.session_state.processing = False
            
            # Rerun to show assistant response
            st.rerun()

    # Footer info
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem; padding: 1rem; 
                background: white; border-radius: 15px; margin-top: 1rem;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
        💡 <strong>Tips:</strong> Gunakan mikrofon untuk input suara atau ketik langsung. 
        Klik tombol 🔊 untuk mendengar jawaban.
    </div>
    """, unsafe_allow_html=True)

# Main execution
if __name__ == "__main__":
    render_chat()
