import api from './api';
import { ChatMessage, ChatResponse } from '../types/api';

export const chatService = {
  // Send a message and get a response
  sendMessage: async (message: string, documentId?: string): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/chat', {
      message,
      document_id: documentId,
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