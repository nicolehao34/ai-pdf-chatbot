from typing import Dict, List, Optional
import json
import os
from datetime import datetime

class DocumentStore:
    def __init__(self, storage_file: str = "documents.json"):
        self.storage_file = storage_file
        self.documents: Dict[str, Dict] = {}
        self.load_documents()

    def load_documents(self):
        """Load documents from storage file."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    self.documents = json.load(f)
            except Exception as e:
                print(f"Error loading documents: {e}")
                self.documents = {}

    def save_documents(self):
        """Save documents to storage file."""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.documents, f, indent=2)
        except Exception as e:
            print(f"Error saving documents: {e}")

    def add_document(self, document: Dict) -> str:
        """Add a new document to the store."""
        doc_id = document['id']
        self.documents[doc_id] = document
        self.save_documents()
        return doc_id

    def get_document(self, doc_id: str) -> Optional[Dict]:
        """Get a document by ID."""
        return self.documents.get(doc_id)

    def get_all_documents(self) -> List[Dict]:
        """Get all documents."""
        return list(self.documents.values())

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document by ID."""
        if doc_id in self.documents:
            # Delete the actual file
            doc = self.documents[doc_id]
            if 'file_path' in doc and os.path.exists(doc['file_path']):
                os.remove(doc['file_path'])
            
            # Remove from store
            del self.documents[doc_id]
            self.save_documents()
            return True
        return False

    def search_documents(self, query: str) -> List[Dict]:
        """Search documents by content."""
        query = query.lower()
        results = []
        for doc in self.documents.values():
            if query in doc['content'].lower():
                results.append(doc)
        return results 