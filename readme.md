# Description of Exam Review Bot

Exam Review Bot (ERB) is a custom intelligent retrieval and hybrid RAG system for final exam preparation. Specifically, it 

- Extracts specific lecture PDFs from your course schedule.

- Matches them to user questions (e.g., “What about transformers was discussed?”).

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


# To-Be-Implemented

- Custom Indexing + Custom Vectorstore database
- hybrid RAG system
- ...
