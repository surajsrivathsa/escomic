# ESCOMIC: Project Structure

Complete overview of the ESCOMIC project directory and file organization.

## Root Directory

```
escomic/
├── README.md                          # Main documentation (START HERE)
├── LICENSE                            # Project license
├── .gitignore                         # Git ignore configuration
│
├── docs/                              # Documentation (📍 You are here)
│   ├── INSTALLATION_DOCKER_HUB.md     # Setup with pre-built images
│   ├── INSTALLATION_LOCAL.md          # Setup with local build
│   ├── SYSTEMS.md                     # Search systems info
│   ├── DOCKER_COMMANDS.md             # Docker reference
│   ├── TROUBLESHOOTING.md             # Known issues & solutions
│   └── FILE_STRUCTURE.md              # This file
│
├── python_backend_api/                # 🔧 Backend (FastAPI)
├── react_frontend_ui/                 # 🎨 Frontend (React)
│
├── docker-compose.yml                 # Development compose file
├── docker-compose.optimized.yml       # Production compose file
├── docker-compose.remote-pull.yaml    # Pre-built images compose
├── build_optimized.sh                 # Build script
│
├── DOCKER_OPTIMIZATION_GUIDE.md       # Docker optimization details
└── DOCKER_QUICK_REFERENCE.md          # Quick Docker reference
```

---

## Backend Structure

### python_backend_api/

```
python_backend_api/
├── README.md                          # Backend specific readme
├── requirements.txt                   # Python dependencies
├── Dockerfile                         # Development image
├── Dockerfile.optimized               # Production image (76% smaller)
│
├── fastapi_webserver/                 # 🌐 Main Application
│   ├── main.py                        # FastAPI app initialization
│   ├── search_main.py                 # Main search logic entry
│   ├── search_utils.py                # Search utility functions
│   ├── coarse_search_utils.py         # TF-IDF / CNN search
│   ├── interpretable_search_utils.py  # Explainable search
│   ├── local_explanation_utils.py     # Local explanations (LIME)
│   ├── explain_relevance_feedback.py  # Feedback explanations
│   ├── rerank_results.py              # Result reranking logic
│   ├── people.json                    # Character database
│   └── __pycache__/                   # Python cache
│
├── search/                            # 🔍 Search Algorithms
│   ├── coarse/
│   │   ├── coarse_search.py           # Fast approximate search
│   │   └── __pycache__/
│   │
│   └── interpretable/
│       ├── constrained_clustering.py  # Clustering algorithms
│       ├── facet_extraction.py        # Facet extraction
│       ├── explanations.py            # Explanation generation
│       └── __pycache__/
│
├── common_functions/                  # 📦 Utilities
│   ├── backend_utils.py               # General utilities
│   ├── img_to_text_extractor.py       # Image OCR extraction
│   ├── pdf_to_img_extractor.py        # PDF → image conversion
│   ├── main_pdf_to_img_converter.py   # PDF processing main
│   ├── main_img_to_txt_converter.py   # Image → text processing
│   └── __pycache__/
│
├── common_constants/                  # ⚙️ Configuration
│   ├── backend_constants.py           # Constants & config values
│   └── __pycache__/
│
├── features/                          # 📊 Pre-computed Features
│   ├── book_metadata.csv              # Book metadata
│   ├── occupations.csv                # Character occupations
│   ├── new_comic_book_metadata*.csv   # Comic book metadata
│   │
│   ├── coarse/                        # Approximate features
│   │   ├── cld_tf_idf_feat.csv        # Color descriptor features
│   │   ├── comic_book_cover_img_feat.csv    # Image features
│   │   ├── comic_book_cover_txt_feat.csv    # Text features
│   │   ├── edh_tf_idf_feat.csv        # Edge descriptor features
│   │   ├── hog_tf_idf_feat.csv        # HOG features
│   │   └── text_tf_idf_feat.csv       # TF-IDF text features
│   │
│   └── interpretable/                 # Explainability features
│       ├── all_features_combined.csv  # Combined features
│       ├── character_explanations.json# Character explanations
│       └── spellchecked_parsed_json_lst.json
│
├── data/                              # 📁 Data & Metadata
│   ├── comicnum_to_book_title.csv     # Comic ID → Title mapping
│   │
│   ├── metadata/                      # ⚠️ LARGE FILES (NOT in repo)
│   │   ├── comic_info_df.csv          # Comic metadata
│   │   ├── COMICS_ocr_file.csv        # OCR text extracted
│   │   ├── merged_df.csv              # Merged metadata
│   │   ├── max_page_per_book_df.csv   # Book page counts
│   │   ├── ocr_all_gp.csv             # All OCR grouped
│   │   └── dev_comic_info_df.csv      # Development data
│   │   → Download from: [Link provided]
│   │   → Extract to: python_backend_api/data/metadata/
│   │
│   ├── comics_data/                   # 📚 Comic Books (PDFs/Images)
│   │   ├── 3493/                      # Book 3493 pages/images
│   │   ├── 3494/                      # Book 3494 pages/images
│   │   ├── 3495/                      # Book 3495 pages/images
│   │   └── comic_books/               # Other comic formats
│   │
│   └── session_data/                  # 💾 User Sessions
│       └── <session_uuid>/            # Session-specific data
│           └── ...
│
└── __pycache__/                       # Python cache
```

---

## Frontend Structure

### react_frontend_ui/

```
react_frontend_ui/
├── README.md                          # Frontend specific readme
├── package.json                       # Node.js dependencies
├── Dockerfile                         # Development image
├── Dockerfile.optimized               # Production image (87% smaller)
├── nginx.conf                         # Nginx configuration (production)
├── constants.js                       # App constants & systems config
│
├── src/                               # 🔨 Source Code
│   ├── App.js                         # Main App component
│   ├── App.css                        # App styles
│   ├── App.test.js                    # App tests
│   ├── index.js                       # Application entry point
│   ├── index.css                      # Global styles
│   ├── book.css                       # Book display styles
│   ├── reportWebVitals.js             # Performance monitoring
│   ├── setupTests.js                  # Test configuration
│   │
│   ├── components/                    # 🧩 React Components
│   │   ├── Header.js                  # Header component
│   │   ├── SearchBar.js               # Search input
│   │   ├── BookGrid.js                # Book results grid
│   │   ├── BookCard.js                # Individual book card
│   │   ├── FilterPanel.js             # Filter controls
│   │   ├── ExplanationPanel.js        # Explanation display
│   │   ├── ComparisonView.js          # Book comparison
│   │   ├── SystemSelector.js          # Select Wayne/Stark/etc
│   │   └── ...more components...
│   │
│   ├── pages/                         # 📄 Page Components
│   │   ├── HomePage.js                # Landing page
│   │   ├── SearchPage.js              # Search interface
│   │   ├── BookDetailPage.js          # Book details
│   │   ├── ExplanationPage.js         # Explanations
│   │   └── ...
│   │
│   ├── routes/                        # 🛣️ Routing
│   │   ├── AppRoutes.js               # Route definitions
│   │   └── ProtectedRoute.js          # Auth-protected routes
│   │
│   └── backend_api_calls/             # 🌐 API Integration
│       ├── searchApi.js               # Search API calls
│       ├── explanationApi.js          # Explanation endpoints
│       ├── comparisonApi.js           # Comparison calls
│       ├── feedbackApi.js             # Feedback logging
│       └── apiClient.js               # HTTP client setup
│
├── public/                            # 📂 Static Files
│   ├── index.html                     # HTML template
│   ├── manifest.json                  # PWA manifest
│   ├── robots.txt                     # SEO robots file
│   │
│   ├── comic_book_covers_ui/          # ⚠️ LARGE FOLDER (NOT in repo)
│   │   ├── original_542_1.jpeg        # Comic cover #542
│   │   ├── original_564_1.jpeg        # Comic cover #564
│   │   ├── original_1260_1.jpeg       # Comic cover #1260
│   │   └── ...5000+ more JPEGs...
│   │   → Download from: [Link provided]
│   │   → Extract to: react_frontend_ui/public/comic_book_covers_ui/
│   │
│   └── ...other static assets...
│
├── node_modules/                      # 📦 Node dependencies (git ignored)
└── build/                             # 🏗️ Production build (git ignored)
```

---

## Key Files

### Configuration Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Development Docker setup |
| `docker-compose.optimized.yml` | Production Docker setup (recommended) |
| `docker-compose.remote-pull.yaml` | Pre-built images deployment |
| `build_optimized.sh` | Build script for optimized images |
| `.gitignore` | Git ignore rules |

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | **Start here** - main documentation |
| `docs/INSTALLATION_DOCKER_HUB.md` | Setup with pre-built images |
| `docs/INSTALLATION_LOCAL.md` | Local build setup |
| `docs/SYSTEMS.md` | Search systems info (Wayne/Stark/etc) |
| `docs/DOCKER_COMMANDS.md` | Docker command reference |
| `docs/TROUBLESHOOTING.md` | Known issues & solutions |
| `docs/FILE_STRUCTURE.md` | This file |
| `DOCKER_OPTIMIZATION_GUIDE.md` | Docker optimization details |
| `DOCKER_QUICK_REFERENCE.md` | Quick Docker reference |

### Backend Key Files

| File | Purpose |
|------|---------|
| `python_backend_api/fastapi_webserver/search_main.py` | Main search entry point |
| `python_backend_api/fastapi_webserver/coarse_search_utils.py` | TF-IDF/CNN search |
| `python_backend_api/fastapi_webserver/local_explanation_utils.py` | LIME explanations |
| `python_backend_api/requirements.txt` | Python dependencies |

### Frontend Key Files

| File | Purpose |
|------|---------|
| `react_frontend_ui/constants.js` | System mappings & constants |
| `react_frontend_ui/src/App.js` | Main app component |
| `react_frontend_ui/package.json` | Node dependencies |
| `react_frontend_ui/nginx.conf` | Production web server config |

---

## Data Organization

### What's In the Repository

✅ Code files (Python/JavaScript)
✅ Configuration files (Docker, package.json)
✅ Documentation files
✅ Feature extraction code

### What's NOT in the Repository (Due to Size)

❌ **Comic book covers** (~1GB, 5000+ JPEGs)
- Location: `react_frontend_ui/public/comic_book_covers_ui/`
- Download from: [Link provided]

❌ **Metadata CSV/XLSX files** (~500MB)
- Location: `python_backend_api/data/metadata/`
- Download from: [Link provided]

❌ **Pre-computed feature files** (some)
- Location: `python_backend_api/features/`
- Partially included, large ones may need download

---

## Important Folders

### For Running the Application

**Absolute Requirements:**
- `python_backend_api/fastapi_webserver/` - Backend code
- `react_frontend_ui/src/` - Frontend code
- `react_frontend_ui/public/comic_book_covers_ui/` - Comic images ⚠️ DOWNLOAD THIS

**For Full Functionality:**
- `python_backend_api/data/metadata/` - Search data ⚠️ DOWNLOAD THIS
- `python_backend_api/features/` - Feature extraction

### For Development

- `docs/` - All documentation
- `python_backend_api/common_functions/` - Utilities
- `react_frontend_ui/src/components/` - React components

---

## File Size Guidance

### Total Project Size

| Component | Size | Notes |
|-----------|------|-------|
| Source code | ~50MB | Python + JavaScript |
| Features | ~200MB | Pre-computed features |
| Covers (need to download) | ~1GB | 5000+ JPEG files |
| Metadata (need to download) | ~500MB | CSV/XLSX files |
| **TOTAL with downloads** | **~1.7GB** | After getting large files |

---

## System Features by File

### Wayne System (Full Featured)

- `fastapi_webserver/main.py` - All endpoints enabled
- `fastapi_webserver/local_explanation_utils.py` - Smart explanations
- `fastapi_webserver/rerank_results.py` - Personalization engine
- `react_frontend_ui/src/components/SystemSelector.js` - Wayne selected

### Stark System (Comparison Baseline)

- `fastapi_webserver/rerank_results.py` - Reranking (same as Wayne)
- `fastapi_webserver/coarse_search_utils.py` - Random comparison logic

### Croft System (Explanation Baseline)

- `fastapi_webserver/explain_relevance_feedback.py` - Random feedback
- Others same as Wayne

### Butcher System (No Personalization)

- `fastapi_webserver/coarse_search_utils.py` - No personalization logic
- `fastapi_webserver/main.py` - Endpoints without reranking

### Gray System (Random Control)

- `fastapi_webserver/main.py` - Random APIs
- `fastapi_webserver/rerank_results.py` - Randomized

---

## Navigation Guide

**First time?**
→ Start with [../README.md](../README.md)

**Want to install?**
→ Choose: [INSTALLATION_DOCKER_HUB.md](./INSTALLATION_DOCKER_HUB.md) or [INSTALLATION_LOCAL.md](./INSTALLATION_LOCAL.md)

**Need help?**
→ See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

**Docker commands?**
→ Check [DOCKER_COMMANDS.md](./DOCKER_COMMANDS.md)

**System info?**
→ Read [SYSTEMS.md](./SYSTEMS.md)

---

## Quick File Paths

### Essential Directories

```bash
# Comic covers location (need to download here)
react_frontend_ui/public/comic_book_covers_ui/

# Metadata location (need to download here)
python_backend_api/data/metadata/

# Search algorithms
python_backend_api/search/

# React components
react_frontend_ui/src/components/

# API integration
react_frontend_ui/src/backend_api_calls/
```

### Log Locations (in Docker)

```bash
# Backend logs
/var/log/escomic/backend/

# Frontend logs (Nginx)
/var/log/nginx/
```

---

## For Contributors

If adding new features:

1. **Backend**: Add code to `python_backend_api/`
2. **Frontend**: Add components to `react_frontend_ui/src/components/`
3. **APIs**: Update endpoints in `fastapi_webserver/main.py`
4. **Documentation**: Update relevant doc file in `docs/`
5. **Tests**: Add tests alongside code

---

## File Permissions

After extracting downloaded files:

```bash
# Comic covers
chmod 644 react_frontend_ui/public/comic_book_covers_ui/*.jpeg

# Metadata
chmod 644 python_backend_api/data/metadata/*.csv
chmod 644 python_backend_api/data/metadata/*.xlsx
```

---

**Last Updated:** February 2026
