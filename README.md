# ESCOMIC 📚

**Adaptive and Explainable Search for Comics** — An intelligent comic book search system with personalization, explainable AI, and interactive relevance feedback.

## Overview

This is research-backed comic book search system that:

✨ **Searches Beyond Metadata** — Use visual & textual content, not just titles/genres

✨ **Explains Results** — Understand *why* results were returned with interactive explanations

✨ **Learns From You** — Personalization via implicit user feedback (mouse hover tracking)

✨ **5 Research Systems** — Compare different approaches: Wayne, Stark, Croft, Butcher, Gray

✨ **Production Ready** — Optimized Docker images, API documentation, full stack setup

**For setup instructions, see:**
- **Easiest:** [INSTALLATION_DOCKER_HUB.md](docs/INSTALLATION_DOCKER_HUB.md) — 5 minutes with pre-built images
- **Local Build:** [INSTALLATION_LOCAL.md](docs/INSTALLATION_LOCAL.md) — Build from source

## Key Features

| Feature | Details |
|---------|---------|
| 🔍 **Content Search** | Search by text, visual features, color, texture, artistic style |
| 💡 **Explainability** | LIME-based local explanations, feature importance analysis |
| 👤 **Personalization** | Learns from hover patterns, adapts results per user |
| 🎚️ **Rich Faceting** | Filter by genre, character, year, color palette, topics |
| 📊 **Comparison** | Compare books side-by-side with explanations |
| 🗣️ **Feedback** | Non-obtrusive relevance feedback via UI interactions |

## Technology Stack

<table>
<tr>
<th>Layer</th>
<th>Technologies</th>
</tr>
<tr>
<td><strong>Backend</strong></td>
<td>FastAPI • Python 3.8+ • scikit-learn • Transformers • PyTorch • LIME</td>
</tr>
<tr>
<td><strong>Frontend</strong></td>
<td>React 18 • Material-UI • Axios • React Router</td>
</tr>
<tr>
<td><strong>Deployment</strong></td>
<td>Docker • Docker Compose • Nginx • Ubuntu/Linux</td>
</tr>
<tr>
<td><strong>ML/AI</strong></td>
<td>Sentence-Transformers • PyTorch • scikit-learn • LIME</td>
</tr>
<tr>
<td><strong>Data</strong></td>
<td>Pandas • NumPy • 7000+ Comic Books • 5000+ Cover Images</td>
</tr>
</table>

## Project Structure

```
escomic/
├── README.md                 ← Start here
├── docs/                     ← All documentation
│   ├── INSTALLATION_DOCKER_HUB.md      (recommended setup)
│   ├── INSTALLATION_LOCAL.md           (local build setup)
│   ├── SYSTEMS.md                      (Wayne/Stark/Croft/etc)
│   ├── TROUBLESHOOTING.md              (known issues)
│   ├── DOCKER_COMMANDS.md              (Docker reference)
│   └── FILE_STRUCTURE.md               (detailed directory guide)
│
├── python_backend_api/       ← FastAPI Backend
├── react_frontend_ui/        ← React Frontend
└── docker-compose*.yml       ← Docker configs
```

👉 **[Full Directory Guide →](docs/FILE_STRUCTURE.md)**

## 🚀 Getting Started

### Prerequisites

- **Docker & Docker Compose** (easiest option) OR
- **Python 3.8+** + **Node.js 18+** (local development)
- **4GB+ RAM** (8GB+ recommended)
- **2-3GB disk space** (more with data files)

### Quick Start

Choose your setup method:

**Option 1: Docker Hub Images (5 minutes - Easiest)**
```bash
docker-compose up -f ./docker-compose.remote-pull.yaml -d
```
👉 **[Full guide →](docs/INSTALLATION_DOCKER_HUB.md)**

**Option 2: Build Locally (20 minutes)**
```bash
docker-compose up -d
```
👉 **[Full guide →](docs/INSTALLATION_LOCAL.md)**

**Option 3: Manual Development (Advanced)**
- Backend: `cd python_backend_api && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- Frontend: `cd react_frontend_ui && npm install && npm start`

👉 **[Full guide →](docs/INSTALLATION_LOCAL.md)**

### After Starting

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Check status**: `docker-compose ps`

## 🎮 Using ESCOMIC

### Basic Workflow

1. **Search**: Enter book (e.g., "book name")
2. **Browse**: See results with explanations
3. **Filter**: Apply facet filters (genre, color, etc.)
4. **Interact**: Hover over results to provide feedback
5. **Explore**: Click for detailed explanations

### Features

- **Content-Based**: Search visual & textual features
- **Explainable**: Understand why results appear
- **Personalized**: System learns from your interactions
- **Comparable**: Side-by-side book comparisons
- **Faceted**: Rich filtering options

⚠️ **Note**: The facet control filter switch is finicky and needs 2-3 clicks to toggle properly. This is a known quirk of the research implementation.

### Systems to Choose From

Select from Wayne, Stark, Croft, Butcher, or Gray:

- **Wayne** ⭐ (Recommended) - Full features
- **Stark** - Test comparison quality
- **Croft** - Test explanation quality
- **Butcher** - Baseline (no personalization)
- **Gray** - Random personalization control

👉 **[System Details →](docs/SYSTEMS.md)**

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
## 🔧 API

Interactive docs: `http://localhost:8000/docs` (after starting)

Key endpoints:
- `POST /book_search_with_searchbar_inputs` - Search
- `POST /local_explanation` - Explain books
- `POST /compare_books` - Compare two books
- `POST /view_comic_book` - View details

## ⚠️ Important: Large Files

Due to size (~1.5GB), these are NOT in the repository:

❌ **Comic Book Covers** (~5000 JPEGs, 1GB)
→ Download from: `[Link provided separately]`
→ Extract to: `react_frontend_ui/public/comic_book_covers_ui/`

❌ **Metadata Files** (CSV/XLSX, 500MB)
→ Download from: `[Link provided separately]`
→ Extract to: `python_backend_api/data/metadata/`

👉 **[Setup instructions →](docs/INSTALLATION_LOCAL.md#data-requirements)**


See [DOCKER_OPTIMIZATION_GUIDE.md](./DOCKER_OPTIMIZATION_GUIDE.md) for details.

## 📚 Documentation

All documentation is in the `docs/` folder:

| Document | Purpose |
|----------|----------|
| [INSTALLATION_DOCKER_HUB.md](docs/INSTALLATION_DOCKER_HUB.md) | Quick setup with pre-built images |
| [INSTALLATION_LOCAL.md](docs/INSTALLATION_LOCAL.md) | Local build & development setup |
| [SYSTEMS.md](docs/SYSTEMS.md) | Wayne, Stark, Croft, Butcher, Gray explained |
| [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Known issues & solutions |
| [DOCKER_COMMANDS.md](docs/DOCKER_COMMANDS.md) | Docker command reference |
| [FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md) | Detailed directory guide |

## 🆘 Need Help?

- **Setup issues?** → [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **Docker commands?** → [DOCKER_COMMANDS.md](docs/DOCKER_COMMANDS.md)
- **System selection?** → [SYSTEMS.md](docs/SYSTEMS.md)
- **File structure?** → [FILE_STRUCTURE.md](docs/FILE_STRUCTURE.md)

## ⚡ Quick Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Check status
docker-compose ps
```

## 🎓 Research

This implements research on:
- **Feature Extraction**: Domain-specific facets for comics
- **Explainable AI**: LIME-based explanations
- **Online Learning**: Adaptive personalization
- **User Studies**: Evaluation vs. baselines

## 📄 Citation

```bibtex
@article{escomic_2024,
  title={ESCOMIC: Adaptive and Explainable Search for Comics},
  author={Your Name},
  journal={Your Journal},
  year={2024}
}
```

## 📞 Support

- 📚 [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- 🐛 Create an issue on GitHub
- 📧 Contact maintainers

---

<div align="center">

**🚀 [Get Started →](docs/INSTALLATION_DOCKER_HUB.md)**

Quick setup with docker-compose in 5 minutes

</div>
