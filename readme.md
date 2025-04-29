# Description of this tool

Exam Review Bot (ERB) for Final Exam Prep 


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
