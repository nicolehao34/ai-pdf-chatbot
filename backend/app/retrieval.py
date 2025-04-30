from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from app.config import VECTOR_DB_DIR

# Initialize embedding model
embedding_model = OpenAIEmbeddings()

# Initialize persistent vectorstore (saved locally)
vectorstore = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embedding_model)

def embed_documents(texts, metadatas=None):
    """
    Embeds a list of texts with optional associated metadata into the vector store.
    Args:
        texts (list): List of text strings to embed.
        metadatas (list of dict, optional): List of metadata dictionaries matching each text.
    """
    if metadatas:
        vectorstore.add_texts(texts, metadatas=metadatas)
    else:
        vectorstore.add_texts(texts)

def retrieve_context(query, k=4):
    """
    Retrieves the top-k most relevant documents from the vectorstore given a query.
    Args:
        query (str): User input question or keyword.
        k (int): Number of documents to retrieve.

    Returns:
        list: Relevant documents as LangChain Document objects.
    """
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever.get_relevant_documents(query)