import axios from 'axios';

// Create an axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:8000', // FastAPI default port
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Enable sending cookies
});

// Add request interceptor for handling auth tokens
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Response error:', error);
    
    // Handle network errors
    if (!error.response) {
      console.error('Network error - is the backend server running?');
      return Promise.reject(new Error('Network error - please check if the backend server is running'));
    }

    // Handle specific error cases
    switch (error.response.status) {
      case 401:
        localStorage.removeItem('token');
        window.location.href = '/login';
        break;
      case 404:
        console.error('Resource not found:', error.response.data);
        break;
      case 500:
        console.error('Server error:', error.response.data);
        break;
      default:
        console.error('API error:', error.response.data);
    }

    return Promise.reject(error);
  }
);

export default api; 