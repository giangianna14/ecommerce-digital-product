# 🌟 Fitur dan Implementasi - Platform E-commerce

Dokumentasi lengkap tentang fitur-fitur yang sudah diimplementasi dan yang bisa ditambahkan.

## 📋 Daftar Isi

1. [Fitur yang Sudah Ada](#-fitur-yang-sudah-ada)
2. [Fitur yang Bisa Ditambahkan](#-fitur-yang-bisa-ditambahkan)
3. [Contoh Implementasi](#-contoh-implementasi)
4. [Best Practices](#-best-practices)

## ✅ Fitur yang Sudah Ada

### 🔐 Sistem Autentikasi
- **JWT Token Authentication**
- **User Registration & Login**
- **Password Hashing dengan bcrypt**
- **Protected Routes**
- **Admin & User Roles**

```python
# Contoh penggunaan
from app.core.security import create_access_token, verify_password

# Login user
token = create_access_token(data={"sub": user.email})

# Verify password
is_valid = verify_password(plain_password, hashed_password)
```

### 🛍️ Manajemen Produk
- **CRUD Operations untuk Produk**
- **Kategori Produk**
- **Featured Products**
- **Search & Filter**
- **Pagination**

```python
# Endpoint contoh
GET /api/v1/products/              # Semua produk
GET /api/v1/products/featured      # Produk unggulan
GET /api/v1/products/categories    # Kategori
GET /api/v1/products/{id}          # Detail produk
```

### 🗄️ Database Management
- **SQLAlchemy ORM**
- **Alembic Migrations**
- **Model Relationships**
- **Database Indexing**

```python
# Model relationship contoh
class Product(Base):
    __tablename__ = "products"
    
    category_id = Column(Integer, ForeignKey("product_categories.id"))
    category = relationship("ProductCategory", back_populates="products")
```

### 🎨 Frontend UI
- **React 18 dengan TypeScript**
- **Tailwind CSS untuk styling**
- **Responsive Design**
- **Component-based Architecture**

```tsx
// Contoh komponen
const ProductCard: React.FC<{ product: Product }> = ({ product }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      <h3 className="text-lg font-semibold">{product.name}</h3>
      <p className="text-gray-600">${product.price}</p>
    </div>
  );
};
```

### 🔄 State Management
- **Redux Toolkit**
- **API Integration dengan Axios**
- **Error Handling**
- **Loading States**

## 🚀 Fitur yang Bisa Ditambahkan

### 1. 🛒 Shopping Cart System

**Backend Implementation:**
```python
# models/cart.py
class Cart(Base):
    __tablename__ = "carts"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
class CartItem(Base):
    __tablename__ = "cart_items"
    
    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    price = Column(Numeric(10, 2))
```

**Frontend Implementation:**
```tsx
// Redux slice for cart
const cartSlice = createSlice({
  name: 'cart',
  initialState: {
    items: [],
    total: 0,
    loading: false
  },
  reducers: {
    addToCart: (state, action) => {
      const existingItem = state.items.find(item => item.id === action.payload.id);
      if (existingItem) {
        existingItem.quantity += 1;
      } else {
        state.items.push({ ...action.payload, quantity: 1 });
      }
      state.total = calculateTotal(state.items);
    },
    removeFromCart: (state, action) => {
      state.items = state.items.filter(item => item.id !== action.payload);
      state.total = calculateTotal(state.items);
    }
  }
});
```

### 2. 💳 Payment Integration (Stripe)

**Backend Setup:**
```python
# requirements.txt
stripe==5.5.0

# services/payment_service.py
import stripe
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentService:
    def create_payment_intent(self, amount: int, currency: str = "usd"):
        return stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            metadata={"integration_check": "accept_a_payment"}
        )
    
    def confirm_payment(self, payment_intent_id: str):
        return stripe.PaymentIntent.confirm(payment_intent_id)
```

**Frontend Integration:**
```tsx
// npm install @stripe/stripe-js @stripe/react-stripe-js

import { loadStripe } from '@stripe/stripe-js';
import { Elements } from '@stripe/react-stripe-js';

const stripePromise = loadStripe('pk_test_...');

const CheckoutForm = () => {
  const [clientSecret, setClientSecret] = useState('');
  
  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    
    const response = await api.post('/payments/create-intent', {
      amount: totalAmount * 100 // Convert to cents
    });
    
    setClientSecret(response.data.client_secret);
  };
};
```

### 3. ⭐ Review & Rating System

**Database Schema:**
```python
# models/review.py
class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Constraints
    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5'),
        UniqueConstraint('user_id', 'product_id', name='unique_user_product_review')
    )
```

**API Endpoints:**
```python
# api/v1/endpoints/reviews.py
@router.post("/reviews/", response_model=ReviewResponse)
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return review_service.create_review(db, review, current_user.id)

@router.get("/products/{product_id}/reviews", response_model=List[ReviewResponse])
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    return review_service.get_reviews_by_product(db, product_id)
```

### 4. 📁 File Upload & Download System

**Backend Implementation:**
```python
# api/v1/endpoints/files.py
from fastapi import UploadFile, File
import os
import uuid

@router.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    file_id = str(uuid.uuid4())
    file_path = f"uploads/{file_id}_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return {"file_id": file_id, "filename": file.filename, "path": file_path}

@router.get("/download/{file_id}")
async def download_file(file_id: str, current_user = Depends(get_current_user)):
    # Verify user has purchased the product
    file_path = get_file_path(file_id)
    return FileResponse(file_path, filename=get_original_filename(file_id))
```

### 5. 🔍 Advanced Search & Filtering

**Backend Search:**
```python
# services/search_service.py
from sqlalchemy import or_, and_

class SearchService:
    def search_products(
        self, 
        db: Session, 
        query: str = None,
        category_id: int = None,
        min_price: float = None,
        max_price: float = None,
        is_free: bool = None
    ):
        products = db.query(Product)
        
        if query:
            products = products.filter(
                or_(
                    Product.name.ilike(f"%{query}%"),
                    Product.short_description.ilike(f"%{query}%")
                )
            )
        
        if category_id:
            products = products.filter(Product.category_id == category_id)
            
        if min_price:
            products = products.filter(Product.price >= min_price)
            
        if max_price:
            products = products.filter(Product.price <= max_price)
            
        if is_free is not None:
            products = products.filter(Product.is_free == is_free)
            
        return products.all()
```

**Frontend Search Component:**
```tsx
const SearchFilters: React.FC = () => {
  const [filters, setFilters] = useState({
    query: '',
    category: '',
    minPrice: '',
    maxPrice: '',
    isFree: false
  });

  const handleSearch = () => {
    dispatch(searchProducts(filters));
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow">
      <input
        type="text"
        placeholder="Cari produk..."
        value={filters.query}
        onChange={(e) => setFilters({...filters, query: e.target.value})}
        className="w-full p-2 border rounded"
      />
      
      <select 
        value={filters.category}
        onChange={(e) => setFilters({...filters, category: e.target.value})}
        className="w-full p-2 border rounded mt-2"
      >
        <option value="">Semua Kategori</option>
        {categories.map(cat => (
          <option key={cat.id} value={cat.id}>{cat.name}</option>
        ))}
      </select>
      
      <button onClick={handleSearch} className="bg-blue-500 text-white p-2 rounded mt-2">
        Cari
      </button>
    </div>
  );
};
```

### 6. 📧 Email Notifications

**Setup:**
```python
# services/email_service.py
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.username = settings.SMTP_USER
        self.password = settings.SMTP_PASSWORD
    
    def send_welcome_email(self, to_email: str, username: str):
        subject = "Selamat Datang di Digital Store!"
        body = f"""
        Halo {username},
        
        Selamat datang di platform e-commerce digital kami!
        Anda dapat mulai berbelanja produk digital berkualitas.
        
        Terima kasih,
        Tim Digital Store
        """
        
        self._send_email(to_email, subject, body)
    
    def send_purchase_confirmation(self, to_email: str, order_id: str, products: list):
        subject = f"Konfirmasi Pembelian - Order #{order_id}"
        body = f"""
        Terima kasih atas pembelian Anda!
        
        Detail Pesanan: {order_id}
        Produk yang dibeli:
        {chr(10).join([f"- {p['name']} (${p['price']})" for p in products])}
        
        Link download akan dikirim segera.
        """
        
        self._send_email(to_email, subject, body)
```

### 7. 👤 User Dashboard

**Components:**
```tsx
// pages/ProfilePage/ProfilePage.tsx
const ProfilePage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('profile');
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {/* Sidebar */}
        <div className="bg-white p-4 rounded-lg shadow">
          <nav className="space-y-2">
            <button 
              onClick={() => setActiveTab('profile')}
              className={`w-full text-left p-2 rounded ${activeTab === 'profile' ? 'bg-blue-100' : ''}`}
            >
              Profile Saya
            </button>
            <button 
              onClick={() => setActiveTab('orders')}
              className={`w-full text-left p-2 rounded ${activeTab === 'orders' ? 'bg-blue-100' : ''}`}
            >
              Riwayat Pembelian
            </button>
            <button 
              onClick={() => setActiveTab('downloads')}
              className={`w-full text-left p-2 rounded ${activeTab === 'downloads' ? 'bg-blue-100' : ''}`}
            >
              Download
            </button>
          </nav>
        </div>
        
        {/* Content */}
        <div className="md:col-span-3 bg-white p-6 rounded-lg shadow">
          {activeTab === 'profile' && <ProfileTab />}
          {activeTab === 'orders' && <OrderHistoryTab />}
          {activeTab === 'downloads' && <DownloadsTab />}
        </div>
      </div>
    </div>
  );
};
```

## 💡 Best Practices

### Security
```python
# Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/login")
@limiter.limit("5/minute")
def login(request: Request, ...):
    pass
```

### Performance Optimization
```python
# Database query optimization
def get_products_with_category(db: Session):
    return db.query(Product).options(joinedload(Product.category)).all()

# Caching with Redis
import redis
cache = redis.Redis(host='localhost', port=6379, db=0)

def get_featured_products(db: Session):
    cached = cache.get("featured_products")
    if cached:
        return json.loads(cached)
    
    products = db.query(Product).filter(Product.is_featured == True).all()
    cache.setex("featured_products", 300, json.dumps(products))  # 5 minutes
    return products
```

### Error Handling
```tsx
// Frontend error boundary
class ErrorBoundary extends React.Component {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <div className="error-fallback">Something went wrong.</div>;
    }

    return this.props.children;
  }
}
```

---

**🎯 Tip:** Mulai implementasi dari fitur yang paling dibutuhkan pengguna terlebih dahulu, seperti shopping cart dan payment system.
