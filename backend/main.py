from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
import uuid

from app.pdf_processor import PDFProcessor
from app.document_store import DocumentStore
from app.ai_service import AIService

app = FastAPI(title="Exam Review Bot API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
pdf_processor = PDFProcessor()
document_store = DocumentStore()
ai_service = AIService()

class Document(BaseModel):
    id: str
    title: str
    content: str
    created_at: str
    updated_at: str
    page_count: int
    file_path: str

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
        # Read file content
        content = await file.read()
        
        # Process PDF
        document = await pdf_processor.process_pdf(content, file.filename)
        
        # Process document with AI service
        ai_service.process_document(document['content'])
        
        # Store document
        doc_id = document_store.add_document(document)
        
        return {
            "success": True,
            "document_id": doc_id,
            "message": "Document uploaded and processed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def get_documents():
    return document_store.get_all_documents()

@app.get("/documents/{doc_id}")
async def get_document(doc_id: str):
    doc = document_store.get_document(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: str):
    if document_store.delete_document(doc_id):
        return {"message": "Document deleted successfully"}
    raise HTTPException(status_code=404, detail="Document not found")

@app.post("/chat")
async def chat(message: str = Form(...), document_id: Optional[str] = Form(None)):
    try:
        # Get AI response
        response = await ai_service.get_response(message)
        
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history")
async def get_chat_history():
    return chat_history

@app.delete("/chat/history")
async def clear_chat_history():
    chat_history.clear()
    ai_service.clear_memory()
    return {"message": "Chat history cleared successfully"}

# Initialize chat history
chat_history = []
