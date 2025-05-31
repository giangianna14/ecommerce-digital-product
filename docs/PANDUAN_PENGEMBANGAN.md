# 🔧 Panduan Pengembangan - Platform E-commerce

Panduan lengkap untuk pengembangan dan kustomisasi platform e-commerce produk digital.

## 📋 Daftar Isi

1. [Setup Development Environment](#-setup-development-environment)
2. [Arsitektur Sistem](#-arsitektur-sistem)
3. [Backend Development](#-backend-development)
4. [Frontend Development](#-frontend-development)
5. [Database Management](#-database-management)
6. [Testing](#-testing)
7. [Deployment](#-deployment)

## 🛠️ Setup Development Environment

### Prasyarat
```bash
# Cek versi yang diperlukan
node --version    # >= 16.0.0
npm --version     # >= 8.0.0
python --version  # >= 3.8
```

### Environment Variables
Buat file `.env` di folder `backend/`:

```env
# Database
DATABASE_URL=sqlite:///./ecommerce.db
TEST_DATABASE_URL=sqlite:///./test.db

# Security
SECRET_KEY=dev-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# Email (Development)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-dev-email@gmail.com
SMTP_PASSWORD=your-app-password

# File Upload
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=pdf,zip,rar,doc,docx

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Development
DEBUG=true
```

### VS Code Settings
Buat file `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "editor.formatOnSave": true,
  "typescript.preferences.importModuleSpecifier": "relative"
}
```

## 🏗️ Arsitektur Sistem

### Backend Architecture

```
app/
├── api/                    # API Routes
│   ├── v1/                # Version 1 endpoints
│   │   ├── endpoints/     # Individual route files
│   │   └── router.py      # Main router
│   └── auth/              # Authentication routes
├── core/                   # Core configurations
│   ├── config.py          # Settings
│   ├── security.py        # Security utilities
│   └── database.py        # Database connection
├── db/                     # Database related
│   └── base.py            # Import all models
├── models/                 # SQLAlchemy models
│   ├── user.py
│   ├── product.py
│   ├── order.py
│   └── payment.py
├── schemas/                # Pydantic schemas
│   ├── user.py
│   └── product.py
├── services/               # Business logic
│   ├── user_service.py
│   └── product_service.py
└── utils/                  # Utility functions
```

### Frontend Architecture

```
src/
├── components/             # Reusable components
│   ├── Navbar/
│   ├── Footer/
│   └── ProtectedRoute/
├── pages/                  # Page components
│   ├── HomePage/
│   ├── ProductsPage/
│   ├── ProductDetailPage/
│   ├── CartPage/
│   ├── CheckoutPage/
│   ├── LoginPage/
│   ├── RegisterPage/
│   └── ProfilePage/
├── hooks/                  # Custom React hooks
├── services/               # API integration
│   └── api.ts
├── store/                  # Redux store
│   ├── store.ts
│   └── slices/
├── types/                  # TypeScript definitions
│   └── index.ts
└── utils/                  # Utility functions
```

## 🐍 Backend Development

### Menambah Model Baru

1. **Buat model di `models/`**:
```python
# models/review.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    
    # Relationships
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
```

2. **Import di `db/base.py`**:
```python
from app.models.review import Review  # noqa
```

3. **Buat schema di `schemas/`**:
```python
# schemas/review.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    product_id: int

class ReviewResponse(ReviewBase):
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

4. **Buat service di `services/`**:
```python
# services/review_service.py
from sqlalchemy.orm import Session
from app.models.review import Review
from app.schemas.review import ReviewCreate

class ReviewService:
    def create_review(self, db: Session, review: ReviewCreate, user_id: int):
        db_review = Review(**review.dict(), user_id=user_id)
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review
```

5. **Buat endpoint di `api/v1/endpoints/`**:
```python
# api/v1/endpoints/reviews.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.review_service import ReviewService

router = APIRouter()
review_service = ReviewService()

@router.post("/reviews/", response_model=ReviewResponse)
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return review_service.create_review(db, review, current_user.id)
```

### Database Migration

```bash
# Buat migrasi
cd backend
alembic revision --autogenerate -m "Add reviews table"

# Review file migrasi di alembic/versions/

# Jalankan migrasi
alembic upgrade head

# Rollback jika ada error
alembic downgrade -1
```

### Testing Backend

```python
# tests/test_reviews.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_review():
    review_data = {
        "rating": 5,
        "comment": "Great product!",
        "product_id": 1
    }
    response = client.post("/api/v1/reviews/", json=review_data)
    assert response.status_code == 200
    assert response.json()["rating"] == 5
```

## ⚛️ Frontend Development

### Menambah Page Baru

1. **Buat komponen page**:
```tsx
// pages/ReviewsPage/ReviewsPage.tsx
import React from 'react';

const ReviewsPage: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Reviews</h1>
      {/* Content here */}
    </div>
  );
};

export default ReviewsPage;
```

2. **Export di index**:
```tsx
// pages/index.ts
export { default as ReviewsPage } from './ReviewsPage/ReviewsPage';
```

3. **Tambah route**:
```tsx
// App.tsx
import { ReviewsPage } from './pages';

<Route path="/reviews" element={<ReviewsPage />} />
```

### State Management dengan Redux

1. **Buat slice**:
```tsx
// store/slices/reviewSlice.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const fetchReviews = createAsyncThunk(
  'reviews/fetchReviews',
  async (productId: number) => {
    const response = await api.get(`/reviews/product/${productId}`);
    return response.data;
  }
);

const reviewSlice = createSlice({
  name: 'reviews',
  initialState: {
    reviews: [],
    loading: false,
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchReviews.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchReviews.fulfilled, (state, action) => {
        state.loading = false;
        state.reviews = action.payload;
      })
      .addCase(fetchReviews.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  }
});

export default reviewSlice.reducer;
```

2. **Tambah ke store**:
```tsx
// store/store.ts
import reviewReducer from './slices/reviewSlice';

export const store = configureStore({
  reducer: {
    // ...existing reducers
    reviews: reviewReducer,
  },
});
```

### Custom Hooks

```tsx
// hooks/useReviews.ts
import { useSelector, useDispatch } from 'react-redux';
import { fetchReviews } from '../store/slices/reviewSlice';

export const useReviews = (productId: number) => {
  const dispatch = useDispatch();
  const { reviews, loading, error } = useSelector(state => state.reviews);

  const loadReviews = () => {
    dispatch(fetchReviews(productId));
  };

  return { reviews, loading, error, loadReviews };
};
```

## 🗄️ Database Management

### Backup Database

```bash
# SQLite backup
cp backend/ecommerce.db backend/ecommerce_backup_$(date +%Y%m%d).db

# PostgreSQL backup
pg_dump -h localhost -U username dbname > backup_$(date +%Y%m%d).sql
```

### Seeding Data

```python
# scripts/seed_data.py
from app.core.database import SessionLocal
from app.models.product import Product, ProductCategory

def seed_categories():
    db = SessionLocal()
    categories = [
        {"name": "Web Templates", "slug": "web-templates"},
        {"name": "Mobile Apps", "slug": "mobile-apps"},
        {"name": "Graphics", "slug": "graphics"},
    ]
    
    for cat_data in categories:
        category = ProductCategory(**cat_data)
        db.add(category)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_categories()
```

### Database Optimization

```sql
-- Index untuk performa
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_featured ON products(is_featured);
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_products_price ON products(price);
```

## 🧪 Testing

### Backend Testing

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)
```

### Frontend Testing

```tsx
// tests/components/ProductCard.test.tsx
import { render, screen } from '@testing-library/react';
import { ProductCard } from '../components/ProductCard';

const mockProduct = {
  id: 1,
  name: 'Test Product',
  price: '19.99',
  // ... other properties
};

test('renders product name', () => {
  render(<ProductCard product={mockProduct} />);
  expect(screen.getByText('Test Product')).toBeInTheDocument();
});
```

### Integration Testing

```bash
# Jalankan test integrasi
python test_integration.py

# Test dengan coverage
pytest --cov=app --cov-report=html
```

## 🚀 Deployment

### Docker Deployment

```dockerfile
# Dockerfile.backend
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Dockerfile.frontend
FROM node:16-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
EXPOSE 80
```

### Production Environment

```env
# .env.production
DATABASE_URL=postgresql://user:password@db:5432/ecommerce_prod
SECRET_KEY=super-secret-production-key
DEBUG=false
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### CI/CD dengan GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r backend/requirements.txt
      - run: pytest backend/tests/

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: docker build -t myapp .
      - run: docker push myregistry/myapp
```

## 📝 Best Practices

### Code Quality
- Gunakan linter (flake8, eslint)
- Tulis docstring untuk fungsi
- Implement error handling yang proper
- Gunakan type hints
- Write unit tests

### Security
- Validasi semua input
- Gunakan prepared statements
- Hash password dengan bcrypt
- Implement rate limiting
- Sanitasi output

### Performance
- Gunakan database indexing
- Implement caching
- Optimize query database
- Lazy loading untuk data besar
- Image optimization

---

**Happy Coding! 🚀**
