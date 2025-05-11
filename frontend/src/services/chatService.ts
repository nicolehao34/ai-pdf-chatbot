import api from './api';
import { ChatMessage, ChatResponse } from '../types/api';

export const chatService = {
  // Send a message and get a response
  sendMessage: async (message: string, documentId?: string): Promise<ChatResponse> => {
    const formData = new FormData();
    formData.append('message', message);
    if (documentId) {
      formData.append('document_id', documentId);
    }

    const response = await api.post<ChatResponse>('/chat', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get chat history
  getChatHistory: async (): Promise<ChatMessage[]> => {
    const response = await api.get<ChatMessage[]>('/chat/history');
    return response.data;
  },

  // Clear chat history
  clearChatHistory: async (): Promise<void> => {
    await api.delete('/chat/history');
  },
}; 