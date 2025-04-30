import io
from PyPDF2 import PdfReader

# You can extend this later to support OCR if needed.
def extract_text_from_pdf(content: bytes) -> str:
    """
    Extracts text from a PDF file content in bytes.

    Args:
        content (bytes): PDF file content.

    Returns:
        str: Extracted plain text from the PDF.
    """
    reader = PdfReader(io.BytesIO(content))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    return text