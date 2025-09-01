// API configuration for different environments
const getApiBaseUrl = () => {
  // Check if we're in development
  if (process.env.NODE_ENV === 'development') {
    return 'http://localhost:8000';
  }
  
  // For production (Netlify), use relative URLs
  return '';
};

export const API_BASE_URL = getApiBaseUrl();

export const API_ENDPOINTS = {
  UPLOAD: '/api/upload',
  DOWNLOAD: '/api/download',
  HEALTH: '/api/health'
};
