import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

load_dotenv()
LLM_API = st.secrets("LLM_API_KEY")

def get_llm_chain(vectorstore):
    # Inisialisasi LLM
    llm = ChatGroq(
        groq_api_key=LLM_API,
        model_name="llama3-70b-8192"
    )

    # Template prompt untuk memaksa model menjawab dalam Bahasa Indonesia
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
Kamu adalah asisten AI yang cerdas dan sopan. Jawablah semua pertanyaan dalam **Bahasa Indonesia** berdasarkan konteks berikut:

Konteks:
{context}

Pertanyaan:
{question}

Jawaban dalam Bahasa Indonesia:
"""
    )

    # Konversi vectorstore menjadi retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Buat chain dengan custom prompt
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt_template},
        return_source_documents=True
    )

    return qa_chain
