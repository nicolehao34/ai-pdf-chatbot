# this file is the main entrypoint
# sets up FastAPI and brings in all API routes

from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="Exam Review Bot (ERB)",
    description="Upload PDFs, extract website PDFs, ask questions, and summarize documents.",
    version="1.0.0"
)

# Include all API endpoints
app.include_router(router)