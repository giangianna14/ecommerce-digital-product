import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { User, LoginCredentials, RegisterData, AuthTokens } from '../../types';
import { authAPI } from '../../services/api';

interface AuthState {
  user: User | null;
  tokens: AuthTokens | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  tokens: localStorage.getItem('tokens') 
    ? JSON.parse(localStorage.getItem('tokens')!) 
    : null,
  isLoading: false,
  isAuthenticated: !!localStorage.getItem('tokens'),
  error: null,
};

// Async thunks
export const loginUser = createAsyncThunk<
  { user: User; tokens: AuthTokens },
  LoginCredentials,
  { rejectValue: string }
>(
  'auth/login',
  async (credentials, { rejectWithValue }) => {
    try {
      const tokens = await authAPI.login(credentials);
      const user = await authAPI.getCurrentUser(tokens.access_token);
      return { user, tokens };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Login failed');
    }
  }
);

export const registerUser = createAsyncThunk<
  { user: User; tokens: AuthTokens },
  RegisterData,
  { rejectValue: string }
>(
  'auth/register',
  async (userData, { rejectWithValue }) => {
    try {      const user = await authAPI.register(userData);
      const tokens = await authAPI.login({
        username: userData.username,
        password: userData.password,
      });
      return { user, tokens };
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Registration failed');
    }
  }
);

export const getCurrentUser = createAsyncThunk<
  User,
  void,
  { rejectValue: string }
>(
  'auth/getCurrentUser',
  async (_, { getState, rejectWithValue }) => {
    try {
      const state = getState() as any;
      const token = state.auth.tokens?.access_token;
      if (!token) {
        throw new Error('No token available');
      }
      return await authAPI.getCurrentUser(token);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to get user');
    }
  }
);

export const checkAuthStatus = createAsyncThunk<
  User | null,
  void,
  { rejectValue: string }
>(
  'auth/checkAuthStatus',
  async (_, { getState, rejectWithValue }) => {
    try {
      const state = getState() as any;
      const tokens = state.auth.tokens;
      
      if (!tokens?.access_token) {
        return null;
      }
      
      // Try to get current user with existing token
      const user = await authAPI.getCurrentUser(tokens.access_token);
      return user;
    } catch (error: any) {
      // Token is invalid, clear it
      localStorage.removeItem('tokens');
      return rejectWithValue('Invalid token');
    }
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      state.user = null;
      state.tokens = null;
      state.isAuthenticated = false;
      state.error = null;
      localStorage.removeItem('tokens');
    },
    clearError: (state) => {
      state.error = null;
    },
    setTokens: (state, action: PayloadAction<AuthTokens>) => {
      state.tokens = action.payload;
      state.isAuthenticated = true;
      localStorage.setItem('tokens', JSON.stringify(action.payload));
    },
  },
  extraReducers: (builder) => {
    builder
      // Login
      .addCase(loginUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload.user;
        state.tokens = action.payload.tokens;
        state.isAuthenticated = true;
        localStorage.setItem('tokens', JSON.stringify(action.payload.tokens));
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Login failed';
      })
      // Register
      .addCase(registerUser.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(registerUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload.user;
        state.tokens = action.payload.tokens;
        state.isAuthenticated = true;
        localStorage.setItem('tokens', JSON.stringify(action.payload.tokens));
      })
      .addCase(registerUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Registration failed';
      })
      // Get current user
      .addCase(getCurrentUser.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(getCurrentUser.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload;
      })
      .addCase(getCurrentUser.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Failed to get user';
        // If token is invalid, logout
        state.user = null;
        state.tokens = null;
        state.isAuthenticated = false;
        localStorage.removeItem('tokens');
      })
      // Check auth status
      .addCase(checkAuthStatus.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(checkAuthStatus.fulfilled, (state, action) => {
        state.isLoading = false;
        if (action.payload) {
          state.user = action.payload;
          state.isAuthenticated = true;
        } else {
          state.user = null;
          state.tokens = null;
          state.isAuthenticated = false;
          localStorage.removeItem('tokens');
        }
      })
      .addCase(checkAuthStatus.rejected, (state) => {
        state.isLoading = false;
        state.user = null;
        state.tokens = null;
        state.isAuthenticated = false;
        state.error = null;
        localStorage.removeItem('tokens');
      });
  },
});

export const { logout, clearError, setTokens } = authSlice.actions;
export default authSlice.reducer;
