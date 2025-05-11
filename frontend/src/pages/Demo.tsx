import { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Alert,
  Divider,
} from '@mui/material';
import { useApi } from '../hooks/useApi';
import { documentService } from '../services/documentService';
import { chatService } from '../services/chatService';
import { Document, ChatMessage, ChatResponse } from '../types/api';

const Demo = () => {
  const [message, setMessage] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  
  // API hooks
  const { data: documents, loading: docsLoading, error: docsError, execute: fetchDocs } = useApi<Document[]>();
  const { data: chatHistory, loading: chatLoading, error: chatError, execute: fetchChat } = useApi<ChatMessage[]>();
  const { loading: uploadLoading, error: uploadError, execute: uploadDoc } = useApi<Document>();
  const { loading: sendLoading, error: sendError, execute: sendMsg } = useApi<ChatResponse>();

  // Handle file selection
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
    }
  };

  // Handle file upload
  const handleUpload = async () => {
    if (selectedFile) {
      await uploadDoc(() => documentService.uploadDocument(selectedFile));
      await fetchDocs(() => documentService.getDocuments());
      setSelectedFile(null);
    }
  };

  // Handle sending message
  const handleSendMessage = async () => {
    if (message.trim()) {
      await sendMsg(() => chatService.sendMessage(message));
      await fetchChat(() => chatService.getChatHistory());
      setMessage('');
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Exam Review Bot Demo
        </Typography>

        {/* Document Upload Section */}
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Upload Document
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            <Button
              variant="contained"
              component="label"
              disabled={uploadLoading}
            >
              Choose File
              <input
                type="file"
                hidden
                onChange={handleFileChange}
                accept=".pdf,.doc,.docx"
              />
            </Button>
            {selectedFile && (
              <Typography variant="body2">
                Selected: {selectedFile.name}
              </Typography>
            )}
            <Button
              variant="contained"
              onClick={handleUpload}
              disabled={!selectedFile || uploadLoading}
            >
              {uploadLoading ? <CircularProgress size={24} /> : 'Upload'}
            </Button>
          </Box>
          {uploadError && (
            <Alert severity="error" sx={{ mt: 2 }}>
              {uploadError}
            </Alert>
          )}
        </Paper>

        {/* Documents List Section */}
        <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Uploaded Documents
          </Typography>
          {docsLoading ? (
            <CircularProgress />
          ) : docsError ? (
            <Alert severity="error">{docsError}</Alert>
          ) : (
            <List>
              {documents?.map((doc) => (
                <ListItem key={doc.id}>
                  <ListItemText
                    primary={doc.title}
                    secondary={`Created: ${new Date(doc.created_at).toLocaleString()}`}
                  />
                </ListItem>
              ))}
            </List>
          )}
        </Paper>

        {/* Chat Section */}
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Chat with AI
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
            <TextField
              fullWidth
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask a question about your documents..."
              disabled={sendLoading}
            />
            <Button
              variant="contained"
              onClick={handleSendMessage}
              disabled={!message.trim() || sendLoading}
            >
              {sendLoading ? <CircularProgress size={24} /> : 'Send'}
            </Button>
          </Box>
          {sendError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {sendError}
            </Alert>
          )}
          <Divider sx={{ my: 2 }} />
          <Box sx={{ maxHeight: 400, overflow: 'auto' }}>
            {chatLoading ? (
              <CircularProgress />
            ) : chatError ? (
              <Alert severity="error">{chatError}</Alert>
            ) : (
              <List>
                {chatHistory?.map((msg, index) => (
                  <ListItem key={index}>
                    <ListItemText
                      primary={msg.role === 'user' ? 'You' : 'AI'}
                      secondary={msg.content}
                      sx={{
                        backgroundColor: msg.role === 'user' ? 'primary.light' : 'grey.100',
                        p: 1,
                        borderRadius: 1,
                      }}
                    />
                  </ListItem>
                ))}
              </List>
            )}
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default Demo; 