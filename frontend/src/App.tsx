import { ThemeProvider, createTheme, CssBaseline, AppBar, Toolbar, Typography, Button, Box, Container } from '@mui/material';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import Home from './pages/Home';
import Demo from './pages/Demo';

// Create a theme instance
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const location = useLocation();

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Exam Review Bot
            </Typography>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Button 
                color="inherit" 
                component={Link} 
                to="/"
                sx={{ 
                  backgroundColor: location.pathname === '/' ? 'rgba(255, 255, 255, 0.1)' : 'transparent'
                }}
              >
                Home
              </Button>
              <Button 
                color="inherit" 
                component={Link} 
                to="/demo"
                sx={{ 
                  backgroundColor: location.pathname === '/demo' ? 'rgba(255, 255, 255, 0.1)' : 'transparent'
                }}
              >
                Demo
              </Button>
            </Box>
          </Toolbar>
        </AppBar>
        <Container component="main" sx={{ flexGrow: 1, py: 4 }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/demo" element={<Demo />} />
          </Routes>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;
