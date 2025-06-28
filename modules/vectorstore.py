import os
import streamlit as st
from pathlib import Path
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter

from pinecone import Pinecone, ServerlessSpec

# ENV variables
PINECONE_API_KEY = st.secrets("PINECONE_API_KEY")
INDEX_NAME = st.secrets("PINECONE_DB_NAME")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

UPLOAD_DIR = "./uploaded_pdfs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@st.cache_data
def process_documents(file_paths):
    """Cache document processing untuk menghindari reload berulang"""
    docs = []
    for path in file_paths:
        loader = PyPDFLoader(path)
        docs.extend(loader.load())
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = splitter.split_documents(docs)
    
    return texts

def load_vectorstore(uploaded_files):
    """
    Load documents ke vectorstore dari Streamlit uploaded files
    Args:
        uploaded_files: List of Streamlit UploadedFile objects
    Returns:
        PineconeVectorStore object
    """
    
    # Save files to disk first
    file_paths = []
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.name
        with open(save_path, "wb") as f:
            f.write(file.getvalue())  # Streamlit file method
        file_paths.append(str(save_path))

    st.write("📁 File paths:", file_paths)

    # Process documents
    texts = process_documents(file_paths)
    st.write("✂️ Total chunks after split:", len(texts))

    # Initialize embeddings
    embeddings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")

    # HAPUS INDEX LAMA
    if INDEX_NAME in pc.list_indexes().names():
        pc.delete_index(INDEX_NAME)
        st.write(f"🗑️ Deleted existing index: {INDEX_NAME}")

    # BUAT ULANG INDEX
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    st.write(f"✅ Created new index: {INDEX_NAME}")

    # Create vectorstore
    vectorstore = PineconeVectorStore.from_documents(
        documents=texts,
        embedding=embeddings,
        index_name=INDEX_NAME
    )

    return vectorstore

def get_existing_vectorstore():
    """
    Get existing vectorstore untuk querying
    Returns:
        PineconeVectorStore object
    """
    embeddings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vectorstore = PineconeVectorStore.from_existing_index(
        index_name=INDEX_NAME,
        embedding=embeddings
    )
    
    return vectorstore
