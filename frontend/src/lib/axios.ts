/**
 * Axios configuration for AURORA Tax Classifier
 *
 * Configures axios with base URL and default headers
 */

import axios from 'axios';

// Get API base URL from environment variables
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add default API key header for all requests
api.interceptors.request.use((config) => {
  // Add API key from environment or use dev key
  const apiKey = import.meta.env.VITE_API_KEY || 'aurora-dev-key-change-in-production';

  // Debug logging
  console.log('API Key from env:', import.meta.env.VITE_API_KEY);
  console.log('API Key being used:', apiKey);

  config.headers['X-Aurora-Key'] = apiKey;

  // Don't set Content-Type for FormData - browser will set it with boundary
  if (!(config.data instanceof FormData)) {
    if (!config.headers['Content-Type']) {
      config.headers['Content-Type'] = 'application/json';
    }
  }

  return config;
});

export default api;
