from typing import List, Dict, Optional
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        openai.api_key = self.openai_api_key
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.vector_store = None
        self.qa_chain = None
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    def process_document(self, content: str) -> None:
        """Process document content and create vector store."""
        # Split text into chunks
        chunks = self.text_splitter.split_text(content)
        
        # Create or update vector store
        if self.vector_store is None:
            self.vector_store = Chroma.from_texts(
                chunks,
                self.embeddings,
                persist_directory="./chroma_db"
            )
        else:
            self.vector_store.add_texts(chunks)

        # Initialize QA chain
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(temperature=0.7),
            retriever=self.vector_store.as_retriever(),
            memory=self.memory,
            return_source_documents=True
        )

    async def get_response(self, question: str) -> Dict:
        """Get AI response for a question."""
        if not self.qa_chain:
            return {
                "message": "Please upload a document first to enable AI responses.",
                "sources": None,
                "confidence": 0.0
            }

        try:
            # Get response from QA chain
            result = self.qa_chain({"question": question})
            
            # Extract sources
            sources = []
            if result.get("source_documents"):
                for doc in result["source_documents"]:
                    if hasattr(doc, "metadata") and "source" in doc.metadata:
                        sources.append(doc.metadata["source"])

            return {
                "message": result["answer"],
                "sources": sources,
                "confidence": 0.95  # This could be calculated based on similarity scores
            }
        except Exception as e:
            return {
                "message": f"Error generating response: {str(e)}",
                "sources": None,
                "confidence": 0.0
            }

    def clear_memory(self) -> None:
        """Clear conversation memory."""
        self.memory.clear() 