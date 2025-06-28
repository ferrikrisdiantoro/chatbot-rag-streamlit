import os
import streamlit as st
from pathlib import Path

UPLOAD_DIR = "./uploaded_pdfs"

def save_uploaded_files(files) -> list[str]:
    """
    Save uploaded Streamlit files to disk
    Args:
        files: List of Streamlit UploadedFile objects
    Returns:
        List of file paths
    """
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_paths = []
    
    for file in files:
        # Streamlit UploadedFile has different structure than FastAPI UploadFile
        file_path = os.path.join(UPLOAD_DIR, file.name)
        
        # Write file content to disk
        with open(file_path, "wb") as f:
            f.write(file.getvalue())  # Use getvalue() for Streamlit files
        
        file_paths.append(file_path)
    
    return file_paths