# ESCOMIC: Installation from Local Build

Build and run ESCOMIC directly from source code using Docker Compose.

## Prerequisites

- Docker & Docker Compose
- 4GB+ RAM (8GB+ recommended)
- 2-3GB disk space

## Quick Start

```bash
# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access application:**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

---

## Data Requirements

⚠️ **IMPORTANT**: Running locally requires additional data files NOT included in the repository due to size.

### 1. Comic Book Covers (REQUIRED)

Without covers, the UI will not display book images.

**Steps:**

1. Download covers from: `https://1drv.ms/u/c/ca9d6b4b08cafad5/IQAOXakqjpCoT6uoGtMJDYJ7AZ49rat6QJoCWk2XH8jpakI?e=hYwPQE`
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

1. Download metadata from: `https://1drv.ms/u/c/ca9d6b4b08cafad5/IQB5sn0zhH3PR4AxnKQsWkfbASejNBIrv0a4Ra-2lRGH8pk?e=3nR3pi`
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
# Rebuild services
docker-compose build --no-cache

# Restart services
docker-compose restart

# View logs
docker-compose logs -f

# Check image sizes
docker images | grep -E "(backend|frontend|escomic)"
```

## For Manual Development (Advanced)

If you prefer not to use Docker and want to develop directly:

**Backend:**
```bash
cd python_backend_api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd fastapi_webserver
uvicorn search_main:app --reload
```

**Frontend:**
```bash
cd react_frontend_ui
npm install --legacy-peer-deps
npm start
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Comic covers not loading** | Check `react_frontend_ui/public/comic_book_covers_ui/` has files |
| **Search returns nothing** | Verify metadata in `python_backend_api/data/metadata/` exists |
| **Backend connection error** | Check `docker-compose ps` - backend should be running |
| **Port already in use** | Stop existing container or use different port |

---

## Next Steps

- [SYSTEMS.md](./SYSTEMS.md) — Learn about Wayne, Stark, Croft, Butcher, Gray
- [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) — Common issues and solutions
- [DOCKER_COMMANDS.md](./DOCKER_COMMANDS.md) — More Docker commands
