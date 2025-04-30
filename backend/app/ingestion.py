import requests
from bs4 import BeautifulSoup
import io
from urllib.parse import urljoin
from app.utils import extract_text_from_pdf
from app.retrieval import embed_documents

# METADATA: Lecture keyword mapping for intelligent labeling
LECTURE_TOPICS = {
    "transformers": "March 10",
    "rnn": "March 3",
    "ffnn": "February 19",
    "word embeddings": "February 12",
    "text classification": "February 10",
    # add more?
}

# This file handles pdf loading and embedding (aka ingestion logic)


def guess_topic_from_filename(filename: str):
    """
    Attempts to infer the lecture topic and date based on keywords found in the filename.
    Returns a tuple of (topic, date). Defaults to "Unknown" if no match is found.
    """
    for keyword, date in LECTURE_TOPICS.items():
        if keyword in filename.lower():
            return keyword.title(), date
    return "Unknown", "Unknown"



def ingest_pdf_from_upload(content: bytes, filename: str):
    """
    Handles ingestion of a single user-uploaded PDF file:
    - Extracts text from the PDF
    - Infers metadata (topic and date) from the filename
    - Embeds the text into the vector store with associated metadata
    """
    text = extract_text_from_pdf(content)
    topic, date = guess_topic_from_filename(filename)
    metadata = {"title": topic, "date": date, "filename": filename}
    embed_documents([text], [metadata])
    return f"Uploaded and embedded {filename} with topic '{topic}'"

def ingest_pdfs_from_website(website_url: str, keyword: str = ""):
    """
    Scrapes a website for PDF links, optionally filtering by keyword:
    - Downloads each matching PDF
    - Extracts text
    - Infers metadata (topic and date) from the PDF link
    - Embeds each PDF's text into the vector store with metadata
    """
    response = requests.get(website_url)
    if response.status_code != 200:
        return "Failed to load website."

    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = [link['href'] for link in soup.find_all('a', href=True) if link['href'].endswith('.pdf')]

    if keyword:
        pdf_links = [link for link in pdf_links if keyword.lower() in link.lower()]

    if not pdf_links:
        return "No matching PDFs found."

    for pdf_link in pdf_links:
        pdf_url = urljoin(website_url, pdf_link)
        pdf_response = requests.get(pdf_url)
        if pdf_response.status_code == 200:
            text = extract_text_from_pdf(pdf_response.content)
            topic, date = guess_topic_from_filename(pdf_link)
            metadata = {"title": topic, "date": date, "source": website_url}
            embed_documents([text], [metadata])

    return f"Successfully ingested {len(pdf_links)} PDFs from the website."
