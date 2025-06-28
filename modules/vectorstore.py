import os
from pathlib import Path
import streamlit as st
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# Ambil kredensial dari Streamlit secrets
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
INDEX_NAME = st.secrets["PINECONE_DB_NAME"]

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Direktori upload
UPLOAD_DIR = Path("./uploaded_pdfs")
UPLOAD_DIR.mkdir(exist_ok=True)

@st.cache_data
def process_documents(file_paths: list[str]) -> list:
    docs = []
    for path in file_paths:
        loader = PyPDFLoader(str(path))
        docs.extend(loader.load())
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_documents(docs)


def load_vectorstore(uploaded_files: list[st.uploaded_file_manager.UploadedFile]) -> PineconeVectorStore:
    # Simpan files ke disk
    file_paths = []
    for f in uploaded_files:
        dest = UPLOAD_DIR / f.name
        with open(dest, "wb") as out:
            out.write(f.getvalue())
        file_paths.append(dest)
    st.write("📁 File paths:", [str(p) for p in file_paths])

    # Proses dokumen
    texts = process_documents(file_paths)
    st.write(f"✂️ Total chunks: {len(texts)}")

    # Hapus index lama jika ada
    if INDEX_NAME in pc.list_indexes().names():
        pc.delete_index(INDEX_NAME)
        st.write(f"🗑️ Deleted index: {INDEX_NAME}")

    # Buat index baru
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    st.write(f"✅ Created index: {INDEX_NAME}")

    # Embedding & vectorstore
    embeddings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")
    vs = PineconeVectorStore.from_documents(
        documents=texts,
        embedding=embeddings,
        index_name=INDEX_NAME
    )
    return vs


def get_existing_vectorstore() -> PineconeVectorStore:
    """Ambil vectorstore dari index yang sudah ada"""
    embeddings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")
    return PineconeVectorStore.from_existing_index(
        index_name=INDEX_NAME,
        embedding=embeddings
    )
