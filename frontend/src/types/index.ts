export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  phone?: string;
  bio?: string;
  is_active: boolean;
  is_superuser: boolean;
  is_verified: boolean;
  avatar?: string;
  created_at: string;
  updated_at?: string;
  last_login?: string;
}

export interface Product {
  id: number;
  name: string;
  description?: string;
  short_description?: string;
  slug: string;
  price: number;
  original_price?: number;
  is_free: boolean;
  is_active: boolean;
  is_featured: boolean;
  is_digital: boolean;
  thumbnail?: string;
  images?: string;
  preview_file?: string;
  file_path?: string;
  file_size?: number;
  file_type?: string;
  download_limit: number;
  meta_title?: string;
  meta_description?: string;
  keywords?: string;
  download_count: number;
  view_count: number;
  purchase_count: number;
  rating: number;
  created_at: string;
  updated_at?: string;
  category?: ProductCategory;
}

export interface ProductCategory {
  id: number;
  name: string;
  description?: string;
  slug: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  full_name?: string;
  phone?: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface CartItem {
  product: Product;
  quantity: number;
}

export interface ApiError {
  detail: string;
  status_code?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}
