import { Container, Typography, Box, Paper } from '@mui/material';

const Home = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom>
            Exam Review Bot
          </Typography>
          <Typography variant="h5" component="h2" gutterBottom>
            Your AI-Powered Study Assistant
          </Typography>
          <Typography variant="body1" paragraph>
            Upload your course materials and get intelligent answers to your questions.
          </Typography>
        </Paper>
      </Box>
    </Container>
  );
};

export default Home; 