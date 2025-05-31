import axios from 'axios';
import { 
  LoginCredentials, 
  RegisterData, 
  AuthTokens, 
  User, 
  Product, 
  ProductCategory 
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const tokens = localStorage.getItem('tokens');
    if (tokens) {
      const { access_token } = JSON.parse(tokens);
      config.headers.Authorization = `Bearer ${access_token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const tokens = localStorage.getItem('tokens');
        if (tokens) {
          const { refresh_token } = JSON.parse(tokens);
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token,
          });
          
          const newTokens = response.data;
          localStorage.setItem('tokens', JSON.stringify(newTokens));
          
          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${newTokens.access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.removeItem('tokens');
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (credentials: LoginCredentials): Promise<AuthTokens> => {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);
    
    const response = await axios.post(`${API_BASE_URL}/auth/login`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  register: async (userData: RegisterData): Promise<User> => {
    const response = await axios.post(`${API_BASE_URL}/auth/register`, userData);
    return response.data;
  },

  getCurrentUser: async (token: string): Promise<User> => {
    const response = await axios.get(`${API_BASE_URL}/auth/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  },

  refreshToken: async (refreshToken: string): Promise<AuthTokens> => {
    const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
      refresh_token: refreshToken,
    });
    return response.data;
  },
};

// Product API
export const productAPI = {
  getProducts: async (params: {
    skip?: number;
    limit?: number;
    category_id?: number | null;
    is_featured?: boolean | null;
    is_free?: boolean | null;
    search?: string;
  }): Promise<Product[]> => {
    const response = await api.get('/products', { params });
    return response.data;
  },

  getFeaturedProducts: async (limit: number = 10): Promise<Product[]> => {
    const response = await api.get('/products/featured', {
      params: { limit },
    });
    return response.data;
  },

  getProductById: async (id: number): Promise<Product> => {
    const response = await api.get(`/products/${id}`);
    return response.data;
  },

  getProductBySlug: async (slug: string): Promise<Product> => {
    const response = await api.get(`/products/slug/${slug}`);
    return response.data;
  },

  getCategories: async (): Promise<ProductCategory[]> => {
    const response = await api.get('/products/categories');
    return response.data;
  },
};

// User API
export const userAPI = {
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/users/me');
    return response.data;
  },

  updateProfile: async (userData: Partial<User>): Promise<User> => {
    const response = await api.put('/users/me', userData);
    return response.data;
  },

  updatePassword: async (passwordData: {
    current_password: string;
    new_password: string;
  }): Promise<void> => {
    await api.put('/users/me/password', passwordData);
  },
};

export default api;
