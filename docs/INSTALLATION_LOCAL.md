# ESCOMIC: Installation from Local Build

Build and run ESCOMIC directly from source code. Useful for development, modifications, or if you don't have Docker Hub access.

## Prerequisites

- Python 3.8+ (3.11+ recommended)
- Node.js 18+
- Docker & Docker Compose (recommended) OR
- System dependencies (Tesseract OCR, etc.)
- 8GB+ RAM
- 3GB+ disk space

## Full Setup with Docker (Recommended for Local)

This builds Docker images locally but provides a clean, reproducible environment.

### 1. Build Images

```bash
# Make build script executable
chmod +x build_optimized.sh

# Build both backend and frontend optimized images
./build_optimized.sh --both

# Or build individually
./build_optimized.sh --backend
./build_optimized.sh --frontend
```

### 2. Start Services

```bash
# Using optimized docker-compose (recommended)
docker-compose -f docker-compose.optimized.yml up -d

# Or standard version
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 3. Access Application

- **Frontend**: http://localhost:3000 or http://localhost:80
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## Manual Local Development (Without Docker)

For developers who want to work directly with source code.

### Backend Setup

```bash
# Navigate to backend
cd python_backend_api

# Create virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
cd fastapi_webserver
uvicorn search_main:app --host 0.0.0.0 --port 8000 --reload

# API will be available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Frontend Setup (New Terminal)

```bash
# Navigate to frontend
cd react_frontend_ui

# Install dependencies
npm install --legacy-peer-deps

# Start development server
npm start

# Opens http://localhost:3000 automatically
```

---

## Data Requirements

⚠️ **IMPORTANT**: Running locally requires additional data files NOT included in the repository due to size.

### 1. Comic Book Covers (REQUIRED)

Without covers, the UI will not display book images.

**Steps:**

1. Download covers from: `[Link to be provided]`
2. Extract the archive:
   ```bash
   unzip comic_covers.zip
   ```
3. Copy JPEG files:
   ```bash
   cp -r comic_covers_ui/*.jpeg react_frontend_ui/public/comic_book_covers_ui/
   ```

The folder should contain files like: `original_542_1.jpeg`, `original_564_1.jpeg`, etc.

### 2. Metadata Files (Optional but Recommended)

For full search functionality including OCR'ed texts and character information.

**These are large files (~500MB+) and were removed from GitHub.**

**Steps:**

1. Download metadata from: `[Link to be provided]`
2. Extract the archive:
   ```bash
   unzip metadata.zip
   ```
3. Copy CSV/XLSX files:
   ```bash
   cp -r metadata/*.csv python_backend_api/data/metadata/
   cp -r metadata/*.xlsx python_backend_api/data/metadata/
   ```

**Expected files in `python_backend_api/data/metadata/`:**
- `comic_info_df.csv` - Comic metadata
- `COMICS_ocr_file.csv` - OCR'ed text from comics
- `merged_df.csv` - Combined metadata
- `max_page_per_book_df.csv` - Page counts
- `occupations.csv` - Character occupations

---

## Folder Structure Check

After setup, verify these directories exist:

```
escomic/
├── react_frontend_ui/public/comic_book_covers_ui/
│   ├── original_542_1.jpeg
│   ├── original_564_1.jpeg
│   ├── original_1260_1.jpeg
│   └── ... (5000+ JPEG files)
│
└── python_backend_api/data/metadata/
    ├── comic_info_df.csv
    ├── COMICS_ocr_file.csv
    ├── merged_df.csv
    └── ... (other CSV/XLSX files)
```

---

## Quick Commands

```bash
# Rebuild images (local build)
docker-compose -f docker-compose.optimized.yml build --no-cache

# Restart services
docker-compose -f docker-compose.optimized.yml restart

# Stop services
docker-compose -f docker-compose.optimized.yml down

# View specific logs
docker-compose logs -f backend_optimized
docker-compose logs -f frontend_optimized

# Check image sizes
docker images | grep -E "(backend|frontend)"
```

## Development Workflow

### Frontend-Only Changes

```bash
npm start  # Hot reload enabled
```

### Backend-Only Changes

```bash
# With reload enabled
uvicorn search_main:app --reload
```

### Full Stack

```bash
# Terminal 1: Backend
cd python_backend_api/fastapi_webserver
uvicorn search_main:app --reload

# Terminal 2: Frontend
cd react_frontend_ui
npm start
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Comic covers not loading** | Check files exist in `react_frontend_ui/public/comic_book_covers_ui/` |
| **Search returns no results** | Ensure metadata CSV files are in `python_backend_api/data/metadata/` |
| **Backend connection error (frontend)** | Check backend is running on port 8000 |
| **Port already in use** | Use different port or kill existing process |
| **Memory issues** | Reduce other applications, or increase Docker memory allocation |

## Next Steps

- See [SYSTEMS.md](./SYSTEMS.md) to learn about different search systems
- Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for additional help
- Review [DOCKER_COMMANDS.md](./DOCKER_COMMANDS.md) for Docker operations
