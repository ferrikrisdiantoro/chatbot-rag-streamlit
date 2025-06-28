from fastapi import FastAPI,UploadFile,File,Form,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from modules.vectorstore import load_vectorstore
from modules.llm import get_llm_chain
from modules.query import query_chain
from logger import logger
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import os
load_dotenv()

INDEX_NAME = os.getenv("PINECONE_DB_NAME")

app=FastAPI(title="Chatbot RAG")

# allow frontend

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def catch_exception_middleware(request:Request,call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception("UNHANDLED EXCEPTION")
        return JSONResponse(status_code=500,content={"error":str(exc)})
    
@app.post("/upload_pdfs/")
async def upload_pdfs(files:List[UploadFile]=File(...)):
    try:
        logger.info(f"recieved {len(files)} files")
        load_vectorstore(files)
        logger.info("documents added to chroma")
        return {"message":"Files processed and vectorstore updated"}
    except Exception as e:
        logger.exception("Error during pdf upload")
        return JSONResponse(status_code=500,content={"error":str(e)})

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"fuser query: {question}")
        embeddings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L12-v2")

        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        vectorstore = PineconeVectorStore.from_existing_index(
            index_name=INDEX_NAME,
            embedding=embeddings
        )

        chain = get_llm_chain(vectorstore)
        result = query_chain(chain, question)
        logger.info("query successfull")
        return result
    except Exception as e:
        logger.exception("error processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/test")
async def test():
    return {"message":"Testing successfull..."}