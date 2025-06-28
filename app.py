import streamlit as st
from components.upload import render_uploader
from components.history_download import render_history_download
from components.chatUI import render_chat

# Set page config
st.set_page_config(
    page_title="Chat with your Documents",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling global
st.markdown("""
<style>
/* Global styling */
.main {
    padding-top: 1rem;
}

/* Hide streamlit menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom header */
.custom-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 2rem;
}

/* Sidebar styling */
.css-1d391kg {
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class='custom-header'>
    <h1 style='margin: 0; color: white;'>📄 Document Chat Assistant</h1>
    <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>Upload PDF documents and chat with them using AI</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state untuk mengecek apakah ada vectorstore
if "vectorstore_ready" not in st.session_state:
    st.session_state.vectorstore_ready = False

# Main layout
def main():
    # Render sidebar uploader
    render_uploader()
    
    # Check if documents are uploaded
    if st.session_state.vectorstore_ready:
        # Render chat interface
        render_chat()
        
        # Render download history
        render_history_download()
    else:
        # Show welcome message
        st.markdown("""
            <div style='text-align: center; padding: 3rem; background: #f8f9ff; 
                        border-radius: 15px; margin: 2rem 0;'>
                <h2 style='color: #667eea; margin-bottom: 1rem;'>👋 Selamat Datang!</h2>
                <p style='color: #666; font-size: 1.1rem; margin-bottom: 2rem;'>
                    Untuk memulai, silakan upload dokumen PDF melalui sidebar di sebelah kiri.
                </p>
                <div style='background: white; padding: 2rem; border-radius: 10px; 
                            box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                    <h3 style='color: #333; margin-bottom: 1rem;'>📋 Cara Penggunaan:</h3>
                    <div style='text-align: left; max-width: 600px; margin: 0 auto;'>
                        <p style="color: #333;"><strong style="color: #000;">1.</strong> 📄 Upload file PDF melalui sidebar</p>
                        <p style="color: #333;"><strong style="color: #000;">2.</strong> ⏳ Tunggu proses indexing selesai</p>
                        <p style="color: #333;"><strong style="color: #000;">3.</strong> 💬 Mulai bertanya tentang isi dokumen</p>
                        <p style="color: #333;"><strong style="color: #000;">4.</strong> 🎤 Gunakan fitur voice input jika diperlukan</p>
                        <p style="color: #333;"><strong style="color: #000;">5.</strong> 🔊 Dengarkan jawaban dengan text-to-speech</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()