<<<<<<< HEAD
# Adaptive and Explainable Search for Comics 📚

An intelligent comic book search system that leverages domain-specific visual and textual facets to provide personalized, explainable search results enhanced with online adaptive relevance feedback.

## Overview

Comics are a versatile art form combining sequences of graphics and dialogue to tell compelling stories. Beyond entertainment, they're used in education, operation manuals, and diverse storytelling mediums. While they've profoundly influenced the movie industry, current comic book search engines focus primarily on metadata and popularity, neglecting content-based and context-aware retrieval.

This project addresses this gap by:

- **Extracting domain-specific facets**: 
  - Textual: genre, gender, topics, character names
  - Visual: book covers, color palettes, textures, artistic styles
  - Lower-level features: edge detection, shape analysis

- **Providing explainable search**: Users can understand *why* results were returned through:
  - Global explanations of the search system's logic
  - Local explanations comparing similar/dissimilar books
  - Visual and textual justifications

- **Adaptive online learning**: 
  - Real-time relevance feedback via mouse hover tracking
  - Non-obtrusive user interaction analysis
  - Personalization that learns user preferences

- **Addressing key user questions**:
  - "Why did we get these search results?"
  - "How are two books from the same results similar or dissimilar?"
  - "What does the search engine believe my likings are?"
  - "How did my previous activity impact current results?"

## Key Features

✨ **Content-Based Search**: Search beyond metadata using visual and textual analysis  
✨ **Explainable AI**: Understand why results are returned with local and global explanations  
✨ **Adaptive Personalization**: System learns from user interactions (hover tracking)  
✨ **Rich Faceting**: Filter by genre, color, texture, topics, character names, etc.  
✨ **Relevance Feedback**: Interactive feedback mechanism to refine results  
✨ **Visual Explanations**: See what contributes to each recommendation  

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.8+)
- **ML/AI**: 
  - scikit-learn (machine learning)
  - Transformers & Hugging Face Hub (embeddings)
  - Sentence-Transformers (semantic search)
  - PyTorch (deep learning inference)
  - LIME (local explanations)
  - Plotly (interactive visualizations)
- **Image Processing**: Pillow, PyTesseract
- **Data**: Pandas, NumPy
- **OCR**: Tesseract, PDFPlumber
- **Cache**: Redis (optional)

### Frontend
- **Framework**: React 18
- **UI Components**: Material-UI (MUI), React Widgets
- **Data Grid**: MUI Data Grid
- **Visualization**: Chart.js, Plotly
- **HTTP Client**: Axios
- **Routing**: React Router v6
- **Styling**: Styled Components, Material-UI Theming

### Deployment
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (production)
- **Node Server**: React Scripts (development)

## Project Structure

```
thesis_deployment/
├── python_backend_api/              # FastAPI Backend
│   ├── fastapi_webserver/           # Main application
│   ├── search/                      # Search algorithms
│   │   ├── coarse/                  # TF-IDF, CNN features
│   │   └── interpretable/           # Explainability & personalization
│   ├── common_functions/            # Utilities
│   ├── common_constants/            # Constants & configs
│   ├── features/                    # Pre-computed features
│   ├── data/                        # Datasets and metadata
│   │   ├── metadata/                # CSV files with book info
│   │   ├── session_data/            # User session histories
│   │   └── comics_data/             # Comic book PDFs/images
│   ├── requirements.txt             # Python dependencies
│   ├── Dockerfile                   # Development image
│   └── Dockerfile.optimized         # Production image (76% smaller)
│
├── react_frontend_ui/               # React Frontend
│   ├── src/
│   │   ├── components/              # React components
│   │   ├── pages/                   # Page components
│   │   ├── backend_api_calls/       # API integration
│   │   ├── routes/                  # Route definitions
│   │   ├── App.js                   # Main app component
│   │   └── index.js                 # Entry point
│   ├── public/
│   │   ├── index.html               # HTML template
│   │   └── comic_book_covers_ui/    # Cover images (1500+)
│   ├── package.json                 # Node dependencies
│   ├── Dockerfile                   # Development image
│   └── Dockerfile.optimized         # Production image (87% smaller)
│
├── docker-compose.yml               # Development compose
├── docker-compose.optimized.yml     # Production compose (recommended)
├── build_optimized.sh               # Build script for optimized images
├── DOCKER_OPTIMIZATION_GUIDE.md     # Docker optimization details
├── DOCKER_QUICK_REFERENCE.md        # Quick docker commands
└── README.md                        # This file
```

## Getting Started

### Prerequisites

- Python 3.8+ (or 3.11+ for optimized builds)
- Node.js 18+
- Docker & Docker Compose (recommended)
- 8GB+ RAM (for ML models)
- Tesseract OCR (for backend)

### Installation & Running

#### Option 1: Docker (Recommended - Optimized) 🐳

**Fastest way to get started:**

```bash
# Navigate to project directory
cd thesis_deployment

# Make build script executable
chmod +x build_optimized.sh

# Build optimized images (76% smaller!)
./build_optimized.sh --both

# Start services with docker-compose
docker-compose -f docker-compose.optimized.yml up -d

# Check services are running
docker-compose -f docker-compose.optimized.yml ps

# View logs
docker-compose -f docker-compose.optimized.yml logs -f
```

**Access the application:**
- 🎨 Frontend: http://localhost:3000 or http://localhost:80
- 🔧 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/docs

#### Option 2: Docker (Standard Development)

```bash
# Build standard images
docker-compose build

# Start services
docker-compose up -d

# Access same ports as above
```

#### Option 3: Local Development (Without Docker)

**Backend:**
```bash
cd python_backend_api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
cd fastapi_webserver
uvicorn search_main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend (new terminal):**
```bash
cd react_frontend_ui

# Install dependencies
npm install --legacy-peer-deps

# Start development server
npm start

# Opens http://localhost:3000 automatically
```

### Quick Docker Commands

```bash
# View image sizes (check optimization)
docker images | grep -E "(frontend|backend)"

# Check running containers
docker ps

# View logs
docker logs -f <container_name>

# Stop all services
docker-compose -f docker-compose.optimized.yml down

# Rebuild and restart
docker-compose -f docker-compose.optimized.yml build --no-cache
docker-compose -f docker-compose.optimized.yml up -d
```

## Usage

### Search Interface

1. **Enter Query**: Type your search query (e.g., "superhero adventure")
2. **Browse Results**: View comic books ranked by relevance
3. **Apply Filters**: Filter by genre, color, topics, etc.
4. **Hover for Feedback**: Hover over results to indicate interest
5. **View Explanations**: 
   - Click on results to see local explanations
   - Understand why books are similar/dissimilar
   - Check predicted user preferences

### Features Walkthrough

**Content-Based Search**
- Search combines textual (OCR, NLP) and visual (CNN) features
- Results ranked by combined relevance

**Explainability**
- **Local Explanations**: Compare two books side-by-side
- **Global Explanations**: See what the system learned about you
- **Visual Justifications**: Heatmaps showing important features

**Personalization**
- System learns from mouse hover activity
- Adapts results based on your patterns
- Non-intrusive - no explicit feedback needed

## API Documentation

Interactive API docs available at `http://localhost:8000/docs` (Swagger UI)

### Key Endpoints

```
POST   /search                    - Search with query and filters
POST   /search/coarse            - Fast approximate search
POST   /search/interpretable     - Explainable search with local insights
POST   /explain/local            - Get explanation between two books
POST   /explain/global           - Get global system explanation
POST   /feedback/hover           - Log user hover interaction
POST   /session/create           - Create new user session
GET    /session/{session_id}     - Get session preferences
GET    /books/{book_id}          - Get detailed book information
```

## Configuration

### Environment Variables

Create `.env` file in project root (optional):

```env
# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1

# Frontend (set in docker-compose)
REACT_APP_API_URL=http://localhost:8000

# Cache (if using Redis)
REDIS_URL=redis://localhost:6379
```

### Data Configuration

Data files are mounted as volumes:
- Backend data: `/api/data` (mounted from `./python_backend_api/data`)
- Frontend images: `/mnt/comic_covers` (mounted from comic book covers directory)

See `docker-compose.optimized.yml` for volume configuration.


See [DOCKER_OPTIMIZATION_GUIDE.md](./DOCKER_OPTIMIZATION_GUIDE.md) for details.

## Research Contributions

This project implements findings from research on:

- **Feature Extraction**: Domain-specific facets for comics
- **Explainable AI**: LIME-based local explanations, feature importance
- **Online Learning**: Adaptive personalization via implicit feedback
- **User Studies**: Evaluation against baseline search methods

### Key Findings

✓ Domain-based facets retrieved more relevant results  
✓ Local explanations effective for comparing books  
✓ User feedback significantly improved subsequent results  
✓ Explaining personalization had limited effectiveness  

## Citation

```bibtex
@article{comics_search_2024,
  title={Adaptive and Explainable Search for Comics},
  author={Your Name},
  journal={Your Journal/Conference},
  year={2024},
  url={https://www.researchgate.net/publication/396999207_Adaptive_and_Explainable_Search_for_Comics}
}
```

## Project Files Reference

- 📄 [DOCKER_QUICK_REFERENCE.md](./DOCKER_QUICK_REFERENCE.md) - Quick Docker commands
- 📚 [DOCKER_OPTIMIZATION_GUIDE.md](./DOCKER_OPTIMIZATION_GUIDE.md) - Detailed optimization guide
- 🔨 [build_optimized.sh](./build_optimized.sh) - Build script
- 🐳 [docker-compose.optimized.yml](./docker-compose.optimized.yml) - Production compose
- 🐳 [docker-compose.yml](./docker-compose.yml) - Development compose

## Troubleshooting

### Frontend images not loading
```bash
# Check volume mount
docker inspect frontend_optimized | grep -i mounts

# Check nginx logs
docker logs frontend_optimized
```

### Backend API connection errors
```bash
# Check backend is running
docker ps | grep backend

# Check API health
curl http://localhost:8000/docs

# View backend logs
docker logs -f backend_optimized
```

### Port already in use
```bash
# Find and kill process
lsof -i :3000  # Frontend
lsof -i :8000  # Backend

# Or change ports in docker-compose.optimized.yml
```

### Out of memory
Ensure 8GB+ available RAM. Close other applications or increase Docker's memory allocation in Docker Desktop settings.

## Development

### Adding Dependencies

**Backend:**
```bash
# Add to requirements.txt, then rebuild
pip install -r python_backend_api/requirements.txt
```

**Frontend:**
```bash
# Add with npm, then rebuild
npm install --save <package-name> --legacy-peer-deps
```

### Running Tests

See individual `README.md` files in `python_backend_api/` and `react_frontend_ui/` directories.

## Performance Tips

- Use optimized Docker images for production
- Pre-compute features for large datasets
- Enable Redis caching for frequently accessed books
- Use Nginx gzip compression (enabled by default)
- Batch similarity computations

## Future Enhancements

- [ ] Mobile responsive design
- [ ] Advanced filtering with more facets
- [ ] Collaborative filtering
- [ ] Real-time collaborative search sessions
- [ ] Model retraining pipeline
- [ ] A/B testing framework
- [ ] Analytics dashboard

## License

[Add your license here]

## Authors

- **Lead Developer**: [Your Name]
- **Research Advisor**: [Advisor Name]
- **Institution**: [Your University/Organization]

## Acknowledgments

- Comic book dataset contributors
- ResearchGate community for feedback
- User study participants
- Open-source community (FastAPI, React, scikit-learn, etc.)

## Support & Contact

- 📧 Email: [your.email@example.com]
- 🐛 Issues: [GitHub Issues Link]
- 💬 Discussions: [GitHub Discussions Link]

---

**Last Updated**: February 2026  
**Status**: Active Development  
**Python Version**: 3.8+  
**Node Version**: 18+  
**Docker**: Recommended for deployment
=======
# escomic
ESCOMIC is an adaptive, explainable comic search system that blends visual, textual, and high-level comic facets. It uses implicit feedback to refine results and offers clear global and local explanations, improving effectiveness, trust, and user satisfaction.
>>>>>>> origin/main
