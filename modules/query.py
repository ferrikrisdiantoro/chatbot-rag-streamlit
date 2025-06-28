import streamlit as st
from modules.vectorstore import get_existing_vectorstore
from modules.llm import get_llm_chain

def query_chain(chain, question):
    """
    Query the chain with a question
    Args:
        chain: LangChain RetrievalQA chain
        question: User question string
    Returns:
        Dict with response and sources
    """
    try:
        result = chain({"query": question})
        
        # Extract answer
        answer = result.get("result", "Maaf, tidak dapat menemukan jawaban.")
        
        # Extract sources
        sources = []
        if "source_documents" in result:
            for doc in result["source_documents"]:
                if hasattr(doc, 'metadata') and 'source' in doc.metadata:
                    sources.append(doc.metadata['source'])
        
        return {
            "response": answer,
            "sources": list(set(sources))  # Remove duplicates
        }
    
    except Exception as e:
        st.error(f"Error during query: {str(e)}")
        return {
            "response": f"Terjadi kesalahan: {str(e)}",
            "sources": []
        }

@st.cache_data
def process_question(question):
    """
    Cached function to process questions
    Args:
        question: User question
    Returns:
        Dict with response and sources
    """
    try:
        # Get vectorstore
        vectorstore = get_existing_vectorstore()
        
        # Get LLM chain
        chain = get_llm_chain(vectorstore)
        
        # Process query
        result = query_chain(chain, question)
        
        return result
        
    except Exception as e:
        st.error(f"Error processing question: {str(e)}")
        return {
            "response": f"Terjadi kesalahan sistem: {str(e)}",
            "sources": []
        }