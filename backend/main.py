from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
import uuid

app = FastAPI(title="Exam Review Bot API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo
documents = {}
chat_history = []

class Document(BaseModel):
    id: str
    title: str
    content: str
    created_at: str
    updated_at: str

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: str

class ChatResponse(BaseModel):
    message: str
    sources: Optional[List[str]] = None
    confidence: float

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        # For demo purposes, we'll just store the filename
        doc_id = str(uuid.uuid4())
        documents[doc_id] = {
            "id": doc_id,
            "title": file.filename,
            "content": f"Content of {file.filename}",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        return {
            "success": True,
            "document_id": doc_id,
            "message": "Document uploaded successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def get_documents():
    return list(documents.values())

@app.get("/documents/{doc_id}")
async def get_document(doc_id: str):
    if doc_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    return documents[doc_id]

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    if doc_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    del documents[doc_id]
    return {"message": "Document deleted successfully"}

@app.post("/chat")
async def chat(message: str, document_id: Optional[str] = None):
    # For demo purposes, return a simple response
    response = {
        "message": f"Demo response to: {message}",
        "sources": ["Demo source 1", "Demo source 2"] if document_id else None,
        "confidence": 0.95
    }
    
    # Store in chat history
    chat_history.append({
        "role": "user",
        "content": message,
        "timestamp": datetime.now().isoformat()
    })
    chat_history.append({
        "role": "assistant",
        "content": response["message"],
        "timestamp": datetime.now().isoformat()
    })
    
    return response

@app.get("/chat/history")
async def get_chat_history():
    return chat_history

@app.delete("/chat/history")
async def clear_chat_history():
    chat_history.clear()
    return {"message": "Chat history cleared successfully"}
