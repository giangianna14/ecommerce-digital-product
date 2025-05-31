# 🔍 Panduan Troubleshooting - Platform E-commerce

Panduan lengkap untuk mengatasi masalah yang mungkin terjadi pada platform e-commerce.

## 📋 Daftar Masalah Umum

1. [Server Tidak Bisa Dijalankan](#-server-tidak-bisa-dijalankan)
2. [Database Error](#-database-error)
3. [API Error](#-api-error)
4. [Frontend Error](#-frontend-error)
5. [CORS Error](#-cors-error)
6. [Port Conflict](#-port-conflict)
7. [Dependency Issues](#-dependency-issues)

## 🚫 Server Tidak Bisa Dijalankan

### ❌ Masalah: Backend server gagal start

**Error yang mungkin muncul:**
```
ModuleNotFoundError: No module named 'app'
```

**🔧 Solusi:**
```bash
# 1. Pastikan PYTHONPATH di-set dengan benar
cd backend
export PYTHONPATH=/d/LEARN/ecommerce_digital_product_sonnet_ai/backend

# 2. Install dependencies yang hilang
pip install -r requirements.txt

# 3. Jalankan server dengan path yang benar
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### ❌ Masalah: Frontend server gagal start

**Error yang mungkin muncul:**
```
npm ERR! peer dep missing
```

**🔧 Solusi:**
```bash
# 1. Hapus node_modules dan install ulang
cd frontend
rm -rf node_modules package-lock.json
npm install

# 2. Atau gunakan npm ci
npm ci

# 3. Start server
npm start
```

## 🗄️ Database Error

### ❌ Masalah: Database connection failed

**Error yang mungkin muncul:**
```
sqlalchemy.exc.OperationalError: no such table: products
```

**🔧 Solusi:**
```bash
# 1. Cek apakah file database ada
ls -la backend/ecommerce.db

# 2. Jalankan migrasi database
cd backend
alembic upgrade head

# 3. Jika masih error, reset database
rm ecommerce.db
alembic upgrade head

# 4. Buat data sampel
python scripts/create_sample_data.py
```

### ❌ Masalah: Migration conflict

**Error yang mungkin muncul:**
```
alembic.util.exc.CommandError: Target database is not up to date
```

**🔧 Solusi:**
```bash
# 1. Cek status migrasi
alembic current

# 2. Cek history migrasi
alembic history

# 3. Upgrade ke versi terbaru
alembic upgrade head

# 4. Jika ada conflict, reset alembic
alembic stamp head
```

## 🔌 API Error

### ❌ Masalah: 404 Not Found pada endpoint

**Error yang mungkin muncul:**
```
{"detail":"Not Found"}
```

**🔧 Solusi:**
```bash
# 1. Cek endpoint yang benar
curl http://localhost:8000/api/v1/products/

# 2. Pastikan router di-import dengan benar di main.py
# 3. Cek log server untuk error detail
```

### ❌ Masalah: 500 Internal Server Error

**🔧 Cara debug:**
```bash
# 1. Cek log server terminal
# 2. Test endpoint secara manual
curl -X GET http://localhost:8000/api/v1/products/ -v

# 3. Cek database connection
python -c "from app.core.database import engine; print(engine.connect())"
```

## ⚛️ Frontend Error

### ❌ Masalah: Blank page atau loading terus

**🔧 Solusi:**
```bash
# 1. Buka browser console (F12) untuk lihat error
# 2. Cek network tab untuk failed requests
# 3. Pastikan backend berjalan di port 8000

# 4. Test API dari browser
# Buka: http://localhost:8000/api/v1/products/
```

### ❌ Masalah: TypeScript compilation error

**Error yang mungkin muncul:**
```
TS2307: Cannot find module '@/components'
```

**🔧 Solusi:**
```bash
# 1. Cek tsconfig.json untuk path mapping
# 2. Restart development server
cd frontend
npm start
```

## 🌐 CORS Error

### ❌ Masalah: CORS policy error

**Error yang mungkin muncul:**
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**🔧 Solusi:**

1. **Cek konfigurasi CORS di backend:**
```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. **Test CORS dengan curl:**
```bash
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://localhost:8000/api/v1/products/
```

## 🔌 Port Conflict

### ❌ Masalah: Port already in use

**Error yang mungkin muncul:**
```
Error: listen EADDRINUSE: address already in use :::8000
```

**🔧 Solusi:**

1. **Cek proses yang menggunakan port:**
```bash
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Linux/Mac
lsof -i :8000
lsof -i :3000
```

2. **Kill proses yang konflik:**
```bash
# Windows
taskkill /F /PID <PID_NUMBER>

# Linux/Mac
kill -9 <PID_NUMBER>
```

3. **Gunakan port alternatif:**
```bash
# Backend di port lain
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Frontend di port lain
PORT=3001 npm start
```

## 📦 Dependency Issues

### ❌ Masalah: Package version conflict

**🔧 Solusi Backend:**
```bash
# 1. Buat virtual environment baru
cd backend
python -m venv venv_new
source venv_new/bin/activate  # Linux/Mac
# atau
venv_new\Scripts\activate     # Windows

# 2. Install dependencies fresh
pip install -r requirements.txt

# 3. Update requirements jika perlu
pip freeze > requirements.txt
```

**🔧 Solusi Frontend:**
```bash
# 1. Clear npm cache
npm cache clean --force

# 2. Delete dan install ulang
rm -rf node_modules package-lock.json
npm install

# 3. Atau gunakan yarn sebagai alternatif
yarn install
```

## 🔧 Diagnostic Commands

### Cek Status Sistem

```bash
# Cek Python dan pip
python --version
pip --version

# Cek Node dan npm
node --version
npm --version

# Cek server status
curl http://localhost:8000/health
curl http://localhost:3000

# Cek database
cd backend
python -c "from app.core.database import engine; engine.connect()"

# Test API endpoints
curl http://localhost:8000/api/v1/products/ | jq .
```

### Debug Mode

**Backend debug:**
```python
# Tambah di main.py untuk debug
import logging
logging.basicConfig(level=logging.DEBUG)

# Atau jalankan dengan log verbose
uvicorn app.main:app --reload --log-level debug
```

**Frontend debug:**
```bash
# Jalankan dengan verbose
REACT_APP_DEBUG=true npm start

# Debug build
npm run build --verbose
```

## 🆘 Emergency Reset

### Reset Lengkap Jika Semua Gagal

```bash
# 1. Stop semua server
# Ctrl+C di terminal

# 2. Reset backend
cd backend
rm -rf __pycache__ app/__pycache__ app/api/__pycache__
rm ecommerce.db
pip install -r requirements.txt
alembic upgrade head
python scripts/create_sample_data.py

# 3. Reset frontend
cd ../frontend
rm -rf node_modules package-lock.json build
npm install

# 4. Start ulang
# Terminal 1:
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2:
cd frontend && npm start
```

## 📞 Mendapatkan Bantuan

### Log Files untuk Debug

**Backend logs:**
```bash
# Jalankan dengan output ke file
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1
```

**Frontend logs:**
```bash
# Browser console (F12 -> Console)
# Network tab untuk API errors
```

### Informasi yang Dibutuhkan untuk Support

Ketika melaporkan masalah, sertakan:

1. **Error message lengkap**
2. **Langkah reproduksi error**
3. **Environment info:**
   ```bash
   python --version
   node --version
   npm --version
   ```
4. **Log files atau screenshot**
5. **Konfigurasi yang diubah**

### Quick Health Check

```bash
# Jalankan script test integrasi
python test_integration.py

# Atau manual check
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/products/
curl http://localhost:3000
```

---

**💡 Tips:** Selalu backup database sebelum melakukan perubahan besar!

**🔍 Debug dengan sabar:** Baca error message dengan teliti, seringkali solusi sudah ada di pesan error.
