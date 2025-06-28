import streamlit as st
from modules.vectorstore import load_vectorstore
from modules.query import process_question

class MockResponse:
    """Mock response class untuk meniru FastAPI response"""
    def __init__(self, status_code, data=None, text=""):
        self.status_code = status_code
        self._data = data
        self.text = text
    
    def json(self):
        return self._data

def upload_pdfs_api(files):
    """
    Process uploaded PDFs directly dalam Streamlit
    Args:
        files: List of Streamlit UploadedFile objects
    Returns:
        MockResponse object
    """
    try:
        # Process files langsung tanpa API call
        load_vectorstore(files)
        
        return MockResponse(
            status_code=200,
            data={"message": "Files processed and vectorstore updated"}
        )
        
    except Exception as e:
        st.error(f"Error during PDF upload: {str(e)}")
        return MockResponse(
            status_code=500,
            text=str(e)
        )

def ask_question(question):
    """
    Process question directly dalam Streamlit
    Args:
        question: User question string
    Returns:
        MockResponse object
    """
    try:
        # Process question langsung tanpa API call
        result = process_question(question)
        
        return MockResponse(
            status_code=200,
            data=result
        )
        
    except Exception as e:
        st.error(f"Error processing question: {str(e)}")
        return MockResponse(
            status_code=500,
            text=str(e)
        )