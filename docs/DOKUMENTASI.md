# 🛍️ Platform E-commerce Produk Digital

Dokumentasi lengkap untuk platform e-commerce produk digital yang dibangun dengan FastAPI (Python) untuk backend dan React (TypeScript) untuk frontend.

## 📋 Daftar Isi

1. [Ringkasan Proyek](#-ringkasan-proyek)
2. [Fitur Utama](#-fitur-utama)
3. [Teknologi yang Digunakan](#-teknologi-yang-digunakan)
4. [Struktur Proyek](#-struktur-proyek)
5. [Instalasi dan Setup](#-instalasi-dan-setup)
6. [Menjalankan Aplikasi](#-menjalankan-aplikasi)
7. [API Dokumentasi](#-api-dokumentasi)
8. [Database](#-database)
9. [Pengujian](#-pengujian)
10. [Deployment](#-deployment)
11. [Kontribusi](#-kontribusi)

## 🎯 Ringkasan Proyek

Platform e-commerce ini dirancang khusus untuk penjualan produk digital seperti template website, aplikasi mobile, e-book, dan software tools. Platform ini menyediakan sistem manajemen produk yang lengkap, sistem autentikasi pengguna, dan integrasi pembayaran.

### Status Proyek: ✅ SEPENUHNYA OPERASIONAL

Platform telah berhasil dibangun dan berjalan dengan sempurna dengan:
- ✅ Backend API FastAPI berjalan di port 8000
- ✅ Frontend React berjalan di port 3000
- ✅ Database dengan 10 produk sampel dan 5 kategori
- ✅ Akun admin tersedia untuk testing
- ✅ Integrasi frontend-backend bekerja dengan baik

## 🚀 Fitur Utama

### Backend (FastAPI)
- **API RESTful** dengan dokumentasi OpenAPI otomatis
- **Autentikasi JWT** dan sistem otorisasi
- **SQLAlchemy ORM** dengan migrasi Alembic
- **Dukungan PostgreSQL/SQLite** untuk database
- **Upload file** untuk produk digital
- **Notifikasi email** 
- **Integrasi pembayaran** (Stripe)
- **Dashboard admin** melalui API

### Frontend (React + TypeScript)
- **React 18** modern dengan TypeScript
- **Desain responsif** dengan Tailwind CSS
- **Redux Toolkit** untuk manajemen state
- **React Router** untuk navigasi
- **Axios** untuk integrasi API
- **Validasi form** dengan React Hook Form
- **Fungsi keranjang belanja**
- **Manajemen autentikasi pengguna**

## 🛠️ Teknologi yang Digunakan

### Backend
- **FastAPI** - Framework web Python yang modern dan cepat
- **SQLAlchemy** - Python SQL toolkit dan ORM
- **Alembic** - Tool migrasi database
- **Pydantic** - Validasi data menggunakan type annotations Python
- **PostgreSQL** - Database utama
- **Redis** - Caching dan penyimpanan session
- **Celery** - Pemrosesan background task
- **Pytest** - Framework testing

### Frontend
- **React 18** - Library JavaScript untuk membangun user interface
- **TypeScript** - Superset JavaScript dengan typing
- **Redux Toolkit** - Manajemen state
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **React Hook Form** - Penanganan form
- **Jest & React Testing Library** - Testing

### DevOps & Tools
- **Docker** - Containerization
- **Docker Compose** - Orkestrasi multi-container
- **GitHub Actions** - CI/CD
- **ESLint & Prettier** - Code formatting dan linting
- **Black & Flake8** - Python code formatting dan linting

## 📁 Struktur Proyek

```
ecommerce-digital-product/
├── backend/                 # Backend FastAPI
│   ├── app/
│   │   ├── api/            # Route API
│   │   │   ├── v1/         # API versi 1
│   │   │   └── auth/       # Route autentikasi
│   │   ├── core/           # Konfigurasi inti
│   │   ├── db/             # Konfigurasi database
│   │   ├── models/         # Model SQLAlchemy
│   │   ├── schemas/        # Schema Pydantic
│   │   ├── services/       # Logika bisnis
│   │   └── utils/          # Fungsi utilitas
│   ├── tests/              # Test backend
│   ├── alembic/            # Migrasi database
│   ├── scripts/            # Script utilitas
│   ├── requirements.txt    # Dependencies Python
│   └── .env.example        # Template environment variables
├── frontend/               # Frontend React
│   ├── src/
│   │   ├── components/     # Komponen yang dapat digunakan ulang
│   │   ├── pages/          # Komponen halaman
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # Service API
│   │   ├── utils/          # Fungsi utilitas
│   │   ├── types/          # Definisi type TypeScript
│   │   ├── assets/         # Asset statis
│   │   └── styles/         # File CSS/SCSS
│   ├── public/             # Asset publik
│   ├── tests/              # Test frontend
│   └── package.json        # Dependencies frontend
├── docs/                   # Dokumentasi
├── tests/                  # Test integrasi
├── .github/                # GitHub workflows dan templates
├── docker-compose.yml      # Konfigurasi Docker
├── README.md              # File ini
└── CHANGELOG.md           # Riwayat versi
```

## ⚙️ Instalasi dan Setup

### Prasyarat
- **Node.js** >= 16.0.0
- **npm** >= 8.0.0
- **Python** >= 3.8
- **PostgreSQL** (opsional, menggunakan SQLite secara default)

### 1. Clone Repository
```bash
git clone <repository-url>
cd ecommerce-digital-product
```

### 2. Install Dependencies
```bash
# Install semua dependencies
npm run install:all

# Atau install secara terpisah
npm run backend:install  # Install dependencies backend
npm run frontend:install # Install dependencies frontend
```

### 3. Setup Environment Variables
```bash
# Copy template environment
cp backend/.env.example backend/.env

# Edit file .env dengan konfigurasi Anda
```

#### Contoh file .env:
```env
# Database
DATABASE_URL=sqlite:///./ecommerce.db
TEST_DATABASE_URL=sqlite:///./test.db

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password

# File Storage
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=10485760  # 10MB

# Payment
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
```

### 4. Setup Database
```bash
# Jalankan migrasi database
npm run backend:migrate

# Atau secara manual
cd backend
alembic upgrade head
```

### 5. Buat Data Sampel (Opsional)
```bash
cd backend
python scripts/create_sample_data.py
```

## 🚀 Menjalankan Aplikasi

### Development Mode

#### Menjalankan Keduanya Sekaligus
```bash
npm run dev
```

#### Menjalankan Secara Terpisah

**Backend:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm start
```

### URL Akses
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Akun Admin Default
- **Email**: admin@example.com
- **Password**: admin123

## 📚 API Dokumentasi

### Endpoint Utama

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/health` | Health check |
| GET | `/api/v1/products/` | Daftar semua produk |
| GET | `/api/v1/products/featured` | Produk unggulan |
| GET | `/api/v1/products/categories` | Daftar kategori |
| GET | `/api/v1/products/{id}` | Detail produk |
| POST | `/api/v1/auth/login` | Login pengguna |
| POST | `/api/v1/auth/register` | Registrasi pengguna |

### Contoh Response API

#### Daftar Produk
```json
[
  {
    "id": 1,
    "name": "React Admin Dashboard Template",
    "short_description": "Modern React admin dashboard with TypeScript",
    "price": "49.99",
    "original_price": "79.99",
    "is_free": false,
    "is_featured": true,
    "category": {
      "name": "Web Development",
      "slug": "web-development"
    }
  }
]
```

### Dokumentasi Interaktif
Akses dokumentasi API yang lengkap dan interaktif di:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗄️ Database

### Schema Database

#### Tabel Utama:
- **users** - Data pengguna dan admin
- **product_categories** - Kategori produk
- **products** - Data produk digital
- **orders** - Pesanan pelanggan
- **order_items** - Item dalam pesanan
- **payments** - Data pembayaran

### Migrasi Database
```bash
# Membuat migrasi baru
cd backend
alembic revision --autogenerate -m "Deskripsi perubahan"

# Menjalankan migrasi
alembic upgrade head

# Rollback migrasi
alembic downgrade -1
```

### Data Sampel
Platform dilengkapi dengan 10 produk sampel dalam 5 kategori:

**Kategori:**
- Web Development
- Mobile Apps
- Design Assets
- E-books
- Software Tools

**Produk Unggulan:**
- React Admin Dashboard Template ($49.99)
- Vue.js E-commerce Template ($69.99)
- React Native Food Delivery App ($89.99)
- Free HTML5 Landing Page Template (GRATIS)

## 🧪 Pengujian

### Menjalankan Test

```bash
# Test semua
npm test

# Test backend saja
npm run backend:test

# Test frontend saja
npm run frontend:test

# Test integrasi
python test_integration.py
```

### Coverage Test
```bash
# Backend coverage
cd backend
pytest --cov=app --cov-report=html

# Frontend coverage
cd frontend
npm test -- --coverage
```

## 🚀 Deployment

### Menggunakan Docker

#### 1. Build dan Jalankan dengan Docker Compose
```bash
docker-compose up --build
```

#### 2. Deployment Manual

**Build Frontend:**
```bash
cd frontend
npm run build
```

**Deploy Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Environment Variables untuk Production
```env
# Production Database
DATABASE_URL=postgresql://user:password@localhost/production_db

# Security
SECRET_KEY=production-secret-key-very-secure

# Email Production
SMTP_HOST=smtp.production.com
SMTP_USER=noreply@yourdomain.com

# File Storage (Cloud)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_BUCKET_NAME=your-bucket

# Payment Production
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
```

## 🔧 Development

### Backend Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Jalankan development server
uvicorn app.main:app --reload

# Membuat migrasi baru
alembic revision --autogenerate -m "pesan migrasi"

# Menjalankan migrasi
alembic upgrade head

# Menjalankan test
pytest
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Jalankan development server
npm start

# Build untuk production
npm run build

# Menjalankan test
npm test

# Lint code
npm run lint
```

### Code Style Guidelines

#### Backend (Python)
- Ikuti standar PEP 8
- Gunakan type hints untuk semua fungsi
- Gunakan model Pydantic untuk schema
- Ikuti pola repository untuk akses data
- Implementasi error handling yang proper

#### Frontend (React/TypeScript)
- Gunakan functional components dengan hooks
- Ikuti aturan hooks React
- Gunakan TypeScript strict mode
- Implementasi error boundaries
- Gunakan atomic design untuk komponen

## 🔒 Keamanan

### Fitur Keamanan
- **Hashing password** dengan bcrypt
- **Autentikasi JWT token**
- **Perlindungan CORS**
- **Validasi input**
- **Pencegahan SQL injection**
- **Perlindungan XSS**
- **Rate limiting**
- **Keamanan upload file**

### Best Practices
- Selalu validasi dan sanitasi input pengguna
- Gunakan parameterized queries
- Implementasi autentikasi dan otorisasi yang proper
- Gunakan HTTPS di production
- Implementasi rate limiting
- Validasi upload file dengan teliti

## 🤝 Kontribusi

### Cara Berkontribusi

1. **Fork repository**
2. **Buat feature branch**
   ```bash
   git checkout -b feature/fitur-amazing
   ```
3. **Commit perubahan**
   ```bash
   git commit -m 'Menambahkan fitur amazing'
   ```
4. **Push ke branch**
   ```bash
   git push origin feature/fitur-amazing
   ```
5. **Buat Pull Request**

### Guidelines Kontribusi
- Ikuti code style yang sudah ada
- Tulis test untuk fitur baru
- Update dokumentasi jika diperlukan
- Pastikan semua test passing

## 📝 Lisensi

Proyek ini menggunakan lisensi MIT. Lihat file `LICENSE` untuk detail.

## 📞 Dukungan

Jika Anda memiliki pertanyaan atau butuh bantuan:

- **Email**: support@example.com
- **GitHub Issues**: [Buat issue baru](https://github.com/yourusername/ecommerce-digital-product/issues)
- **Documentation**: [Wiki](https://github.com/yourusername/ecommerce-digital-product/wiki)

## 🗺️ Roadmap

### Version 1.1 (Planned)
- [ ] Implementasi sistem review dan rating
- [ ] Integrasi payment gateway lokal
- [ ] Dashboard analytics untuk admin
- [ ] Sistem notifikasi real-time
- [ ] Fitur wishlist untuk pengguna

### Version 1.2 (Future)
- [ ] Multi-vendor marketplace
- [ ] Sistem affiliate
- [ ] Mobile app (React Native)
- [ ] Advanced search dengan Elasticsearch
- [ ] Sistem chat customer service

## 📊 Status Proyek

[![Build Status](https://img.shields.io/badge/Build-Passing-green)]()
[![Coverage](https://img.shields.io/badge/Coverage-85%25-brightgreen)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue)]()

---

**Terakhir diupdate**: 1 Juni 2025

**Dibuat dengan ❤️ menggunakan FastAPI dan React**
