from PyPDF2 import PdfReader
from typing import Dict, List, Tuple
import os
from datetime import datetime
import uuid

class PDFProcessor:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    async def process_pdf(self, file_content: bytes, filename: str) -> Dict:
        """Process a PDF file and extract its content."""
        try:
            # Save the file
            file_path = os.path.join(self.upload_dir, filename)
            with open(file_path, "wb") as f:
                f.write(file_content)

            # Extract text from PDF
            pdf = PdfReader(file_path)
            text_content = []
            for page in pdf.pages:
                text_content.append(page.extract_text())

            # Create document metadata
            doc_id = str(uuid.uuid4())
            document = {
                "id": doc_id,
                "title": filename,
                "content": "\n".join(text_content),
                "file_path": file_path,
                "page_count": len(pdf.pages),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }

            return document

        except Exception as e:
            # Clean up file if processing fails
            if os.path.exists(file_path):
                os.remove(file_path)
            raise Exception(f"Error processing PDF: {str(e)}")

    def extract_keywords(self, text: str) -> List[str]:
        """Extract key terms from text."""
        # Simple keyword extraction (can be enhanced with NLP)
        words = text.lower().split()
        # Remove common words and short terms
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        return list(set(keywords))[:10]  # Return top 10 unique keywords 