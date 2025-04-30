# Handles retrieval + RAG answering + summarization

# llm_chain.py
from langchain.chat_models import ChatOpenAI
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from app.retrieval import retrieve_context
from dotenv import load_dotenv

load_dotenv()


# Initialize the GPT-4 model
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# Set up the Tavily internet search tool (make sure your API key is set via environment variable `TAVILY_API_KEY`)
search_tool = TavilySearchAPIWrapper()

def answer_question(query):
    """
    Answers a user query using hybrid RAG:
    - Retrieves course materials matching the query from the vector store
    - Performs a live internet search with Tavily for supplemental information
    - Combines both sources in a single GPT-4 prompt to produce the answer
    """
    # Retrieve internal course material
    docs = retrieve_context(query)
    context = "\n\n".join([doc.page_content for doc in docs])

    # Get external internet knowledge
    internet_info = search_tool.run(query)

    prompt = f"""
    Based on the course lecture materials and external knowledge, answer the following:

    --- COURSE MATERIAL ---
    {context}

    --- INTERNET KNOWLEDGE ---
    {internet_info}

    QUESTION:
    {query}
    """
    
    return llm.predict(prompt)

def summarize_content():
    """
    Summarizes all currently ingested course materials.
    Uses retrieved documents from the vector store to build a summary prompt.
    """
    docs = retrieve_context("Summarize all course content")
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"Summarize the following lecture material in key takeaways:\n\n{context}"
    return llm.predict(prompt)