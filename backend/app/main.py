from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent
sys.path.append(str(app_dir))

from rag.chat_engine import ChatEngine
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the chat engine
def init_chat_engine():
    try:
        # Get the path to the vectorstore
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_dir = os.path.join(current_dir, "rag", "vectorstore")
        
        # Load the existing vector store
        vector_store = Chroma(
            persist_directory=db_dir,
            embedding_function=OpenAIEmbeddings()
        )
        
        return ChatEngine(vector_store)
    except Exception as e:
        print(f"Error initializing chat engine: {str(e)}")
        raise

chat_engine = init_chat_engine()

class ChatRequest(BaseModel):
    message: str
    chat_history: List[dict] = []

class ChatResponse(BaseModel):
    response: str
    sources: List[str]

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Process the chat request
        result = chat_engine.chat(request.message)
        
        return ChatResponse(
            response=result["response"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 