import streamlit as st
from utils.api import ask_question
from audio.stt import recognize_speech_from_mic
from audio.tts import speak_text

def render_chat():
    # Custom CSS untuk styling yang lebih baik
    st.markdown("""
    <style>
    /* Hide default streamlit elements */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Main app styling */
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Custom button styling */
    .stButton > button {
        border-radius: 20px;
        border: none;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Mic button specific styling */
    .mic-button .stButton > button {
        background: linear-gradient(90deg, #ff6b6b 0%, #ee5a52 100%) !important;
        font-size: 1.2rem;
        padding: 0.75rem;
    }
    
    /* TTS button styling */
    .tts-button .stButton > button {
        background: linear-gradient(90deg, #4ecdc4 0%, #44a08d 100%) !important;
        font-size: 0.9rem !important;
        padding: 0.4rem 0.8rem !important;
        width: auto !important;
        min-width: 60px;
    }
    
    /* Chat input styling */
    .stChatInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
    }
    
    /* Chat message container */
    .chat-message {
        margin: 1rem 0;
    }
    
    /* Remove extra spacing */
    .element-container {
        margin-bottom: 0.5rem !important;
    }
    
    /* TTS button container */
    .tts-container {
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    
    /* Success message styling */
    .stSuccess {
        padding: 0.25rem;
        font-size: 0.8rem;
    }
    
    /* Spinner styling */
    .stSpinner {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header dengan emoji dan styling
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <h2 style='color: #667eea; margin: 0;'>💬 Chat with Your Documents</h2>
        <p style='color: #666; margin: 0.5rem 0;'>Ask questions about your uploaded documents</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "mic_input" not in st.session_state:
        st.session_state.mic_input = ""
    
    if "processing" not in st.session_state:
        st.session_state.processing = False

    # Display chat messages
    if st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
                # TTS button untuk assistant messages
                if msg["role"] == "assistant":
                    # Create a container for TTS button with custom styling
                    tts_container = st.container()
                    with tts_container:
                        st.markdown('<div class="tts-container">', unsafe_allow_html=True)
                        col1, col2 = st.columns([1, 9])
                        with col1:
                            st.markdown('<div class="tts-button">', unsafe_allow_html=True)
                            if st.button("🔊", key=f"tts_{i}", help="Bacakan jawaban ini"):
                                with st.spinner("🗣️ Sedang berbicara..."):
                                    try:
                                        speak_text(msg["content"])
                                        st.success("✅ Selesai!")
                                    except Exception as e:
                                        st.error(f"❌ Error: {str(e)}")
                            st.markdown('</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show processing indicator jika AI sedang berpikir
        if st.session_state.processing:
            with st.chat_message("assistant"):
                st.markdown("🤔 **Sedang berpikir...**")
                
    else:
        # Welcome message
        st.markdown("""
        <div style='text-align: center; padding: 3rem 1rem; color: #666; background: #f8f9fa; border-radius: 15px; margin: 2rem 0;'>
            <h4 style='color: #667eea; margin-bottom: 1rem;'>👋 Selamat datang!</h4>
            <p style='margin: 0;'>Mulai percakapan dengan mengetik pertanyaan atau menggunakan mikrofon</p>
        </div>
        """, unsafe_allow_html=True)

    # Input section dengan spacing yang proper
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create columns for input layout
    input_col1, input_col2 = st.columns([5, 1])
    
    with input_col1:
        user_input = st.chat_input("💭 Ketik pertanyaan Anda di sini...")
    
    with input_col2:
        st.markdown('<div class="mic-button">', unsafe_allow_html=True)
        mic_clicked = st.button("🎤", key="mic_button", help="Klik untuk berbicara")
        st.markdown('</div>', unsafe_allow_html=True)

    # Handle microphone input
    if mic_clicked and not st.session_state.processing:
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
        st.session_state.mic_input = ""
        
        # Rerun to show user message and start processing
        st.rerun()

    # Process AI response jika sedang processing
    if st.session_state.processing and st.session_state.messages:
        # Get the last user message
        last_user_message = None
        for msg in reversed(st.session_state.messages):
            if msg["role"] == "user":
                last_user_message = msg["content"]
                break
        
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
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.85rem; padding: 1rem; background: #f8f9fa; border-radius: 10px; margin-top: 1rem;'>
        💡 <strong>Tips:</strong> Gunakan mikrofon untuk input suara atau ketik langsung. 
        Klik tombol 🔊 untuk mendengar jawaban.
    </div>
    """, unsafe_allow_html=True)
