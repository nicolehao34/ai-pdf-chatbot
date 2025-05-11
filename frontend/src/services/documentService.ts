import api from './api';
import { Document, UploadResponse } from '../types/api';

export const documentService = {
  // Upload a new document
  uploadDocument: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post<UploadResponse>('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get all documents
  getDocuments: async (): Promise<Document[]> => {
    const response = await api.get<Document[]>('/documents');
    return response.data;
  },

  // Get a specific document
  getDocument: async (id: string): Promise<Document> => {
    const response = await api.get<Document>(`/documents/${id}`);
    return response.data;
  },

  // Delete a document
  deleteDocument: async (id: string): Promise<void> => {
    await api.delete(`/documents/${id}`);
  },

  // Search documents
  searchDocuments: async (query: string): Promise<Document[]> => {
    const response = await api.get<Document[]>(`/documents/search?query=${encodeURIComponent(query)}`);
    return response.data;
  },
}; 