# Description of Exam Review Bot

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

## Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

The frontend is built with:
- React.js with TypeScript
- Material-UI for components
- React Router for navigation
- Axios for API calls

# Development

## Backend Development
- The backend is built with FastAPI
- API documentation is available at `/docs` when running the server

## Frontend Development
- The frontend uses Vite as the build tool
- Development server runs on `http://localhost:5173` by default
- Hot Module Replacement (HMR) is enabled for faster development

# To-Be-Implemented

- Custom Indexing + Custom Vectorstore database
- hybrid RAG system
- File upload interface
- Chat interface
- Progress tracking
- User authentication
