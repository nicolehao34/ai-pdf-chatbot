# Exam Review Bot

Exam Review Bot (ERB) is a custom intelligent retrieval and hybrid RAG system for final exam preparation. Specifically, it 

- Extracts specific lecture PDFs from your course schedule.

- Matches them to user questions (e.g., "What about transformers was discussed?").

- Supplements with internet knowledge (external search).

- Summarizes and explain the content intelligently.


# Higher-level Architecture
[Your Documents: PDFs, Ed Posts, Images]
      ↓
[Loader modules]
      ↓
[Text Chunker (split large docs)]
      ↓
[Embedder (create vector embeddings)]
      ↓
[Vector Store (Chroma, FAISS, or similar)]
      ↓
[Retriever (search the database)]
      ↓
[LLM (OpenAI, Claude, or Local Model)]
      ↓
[Answer to your Question]


# Project Setup

## Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm 7 or higher

## Backend Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the backend directory:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

# Running the Demo

## Starting the Application
1. Start both frontend and backend concurrently:
   ```bash
   cd frontend
   npm run dev:all
   ```
   This will start:
   - Frontend at http://localhost:5173
   - Backend at http://localhost:8000

## Using the Demo

### 1. Uploading Documents
1. Navigate to the Demo page using the navigation bar
2. In the "Upload Document" section:
   - Click "Choose File" to select a PDF document
   - Click "Upload" to process the document
   - Wait for the upload confirmation
   - The document will appear in the "Uploaded Documents" list

### 2. Chatting with AI
1. In the "Chat with AI" section:
   - Type your question in the text field
   - Click "Send" or press Enter
   - Wait for the AI's response
   - The conversation history will be displayed below

### Features
- **Document Management**:
  - Upload PDF documents
  - View list of uploaded documents
  - Automatic document processing and indexing

- **AI Chat Interface**:
  - Real-time responses
  - Context-aware answers
  - Source references
  - Conversation history

- **User Experience**:
  - Loading indicators
  - Error handling
  - Responsive design
  - Real-time updates

## Troubleshooting

### Common Issues
1. **Upload Fails**:
   - Check file size (max 10MB)
   - Ensure file is PDF format
   - Check backend logs for errors

2. **Chat Not Working**:
   - Verify OpenAI API key in `.env`
   - Check internet connection
   - Ensure backend is running

3. **Frontend Not Loading**:
   - Clear browser cache
   - Check console for errors
   - Verify all dependencies are installed

### Getting Help
- Check the console for error messages
- Review backend logs
- Ensure all services are running
- Verify environment variables

# Development

## Backend Development
- The backend is built with FastAPI
- API documentation is available at `/docs` when running the server
- Use `uvicorn main:app --reload` for development

## Frontend Development
- The frontend uses Vite as the build tool
- Development server runs on `http://localhost:5173` by default
- Hot Module Replacement (HMR) is enabled for faster development

# To-Be-Implemented

- Custom Indexing + Custom Vectorstore database
- Hybrid RAG system
- File upload interface
- Chat interface
- Progress tracking
- User authentication
- 

# To-Dos
- ~~Setting up frontend~~
- ~~Backend frontend integration API service layer~~
- Get frontend + backend demo working PERFECTLY
- Figure out how to insert interative demo in personal website
