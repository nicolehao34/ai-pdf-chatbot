# in API.py, in tendem to main.py, which is the main entrypoint to the backend API
# we define all the API endpoints based on user actions 

from fastapi import APIRouter, UploadFile, File
from app.ingestion import ingest_pdf_from_upload, ingest_pdfs_from_website
from app.llm_chain import answer_question, summarize_content


router = APIRouter()

# define endpoints below

# POST: process info
# GET: retrieve infor
# DELETE: delete info
# PUT: replace
# Upload pdf from User
@router.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # async function to wait for user input
    # wait for user to upload file
    content = await file.read()
    
    # calls function from ingestion logic (ingestion.py) to process and embed pdf into vectorstore
    message = ingest_pdf_from_upload(content, file.filename)
    
    # send JSON response back to user, confirming the upload was sucessful
    return {"message": message}
    

# Extract PDFs from specified website upon request
@router.post("/extract_pdfs_from_website")
async def extract_pdfs_from_website(website_url: str, keyword: str = ""):
    message = ingest_pdfs_from_website(website_url, keyword)
    return {"message": message}
    
# User ask questions about the knowledge base
@router.post("/ask")
async def ask_question_endpoint(query: str):
    # generate answer from llm
    answer = answer_question(query)
    return {"answer": answer}


# User asks bot to summarize content
@router.get("/summarize")
async def summarize_endpoint():
    summary = summarize_content()
    return {"summary": summary}