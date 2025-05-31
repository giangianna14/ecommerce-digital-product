import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Product, ProductCategory } from '../../types';
import { productAPI } from '../../services/api';

interface ProductState {
  products: Product[];
  featuredProducts: Product[];
  categories: ProductCategory[];
  selectedProduct: Product | null;
  isLoading: boolean;
  error: string | null;
  filters: {
    search: string;
    category_id: number | null;
    is_featured: boolean | null;
    is_free: boolean | null;
  };
}

const initialState: ProductState = {
  products: [],
  featuredProducts: [],
  categories: [],
  selectedProduct: null,
  isLoading: false,
  error: null,
  filters: {
    search: '',
    category_id: null,
    is_featured: null,
    is_free: null,
  },
};

// Async thunks
export const fetchProducts = createAsyncThunk<
  Product[],
  { skip?: number; limit?: number; filters?: Partial<ProductState['filters']> },
  { rejectValue: string }
>(
  'products/fetchProducts',
  async ({ skip = 0, limit = 20, filters = {} }, { rejectWithValue }) => {
    try {
      return await productAPI.getProducts({ skip, limit, ...filters });
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch products');
    }
  }
);

export const fetchFeaturedProducts = createAsyncThunk<
  Product[],
  { limit?: number },
  { rejectValue: string }
>(
  'products/fetchFeaturedProducts',
  async ({ limit = 10 }, { rejectWithValue }) => {
    try {
      return await productAPI.getFeaturedProducts(limit);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch featured products');
    }
  }
);

export const fetchProductBySlug = createAsyncThunk<
  Product,
  string,
  { rejectValue: string }
>(
  'products/fetchProductBySlug',
  async (slug, { rejectWithValue }) => {
    try {
      return await productAPI.getProductBySlug(slug);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Product not found');
    }
  }
);

export const fetchProductById = createAsyncThunk<
  Product,
  number,
  { rejectValue: string }
>(
  'products/fetchProductById',
  async (id, { rejectWithValue }) => {
    try {
      return await productAPI.getProductById(id);
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Product not found');
    }
  }
);

export const fetchCategories = createAsyncThunk<
  ProductCategory[],
  void,
  { rejectValue: string }
>(
  'products/fetchCategories',
  async (_, { rejectWithValue }) => {
    try {
      return await productAPI.getCategories();
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch categories');
    }
  }
);

const productSlice = createSlice({
  name: 'products',
  initialState,
  reducers: {
    setFilters: (state, action: PayloadAction<Partial<ProductState['filters']>>) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    clearFilters: (state) => {
      state.filters = initialState.filters;
    },    clearSelectedProduct: (state) => {
      state.selectedProduct = null;
    },    clearError: (state) => {
      state.error = null;
    },
  },  extraReducers: (builder) => {
    builder
      // Fetch products
      // eslint-disable-next-line no-whitespace-before-property
      .addCase(fetchProducts.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchProducts.fulfilled, (state, action) => {
        state.isLoading = false;
        state.products = action.payload;
      })
      .addCase(fetchProducts.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Failed to fetch products';
      })
      // Fetch featured products
      .addCase(fetchFeaturedProducts.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchFeaturedProducts.fulfilled, (state, action) => {
        state.isLoading = false;
        state.featuredProducts = action.payload;
      })
      .addCase(fetchFeaturedProducts.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Failed to fetch featured products';
      })
      // Fetch product by slug
      .addCase(fetchProductBySlug.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })      .addCase(fetchProductBySlug.fulfilled, (state, action) => {
        state.isLoading = false;
        state.selectedProduct = action.payload;
      })
      .addCase(fetchProductBySlug.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Product not found';
      })
      // Fetch product by id
      .addCase(fetchProductById.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchProductById.fulfilled, (state, action) => {
        state.isLoading = false;
        state.selectedProduct = action.payload;
      })
      .addCase(fetchProductById.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Product not found';
      })
      // Fetch categories
      .addCase(fetchCategories.fulfilled, (state, action) => {
        state.categories = action.payload;
      });
  },
});

export const { setFilters, clearFilters, clearSelectedProduct, clearError } = productSlice.actions;
export default productSlice.reducer;
