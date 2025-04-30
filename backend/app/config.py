import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Directory to store the Chroma vector database
VECTOR_DB_DIR = "./chroma_db"

# API keys (loaded securely)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Other optional configuration settings
CHUNK_SIZE = 1000
OVERLAP_SIZE = 200
RETRIEVAL_TOP_K = 4
