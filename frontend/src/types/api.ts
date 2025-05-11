export interface Document {
  id: string;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
}

export interface Question {
  id: string;
  text: string;
  answer: string;
  created_at: string;
  document_id?: string;
}

export interface UploadResponse {
  success: boolean;
  document_id: string;
  message: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ChatResponse {
  message: string;
  sources?: string[];
  confidence: number;
}

export interface ErrorResponse {
  detail: string;
  status_code: number;
} 