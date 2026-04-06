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
| 💡 **Explainability** | Weights-based local explanations, feature importance analysis |
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
<td>FastAPI • Python 3.8+ • scikit-learn • Transformers • PyTorch </td>
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
<td>Sentence-Transformers • PyTorch • scikit-learn </td>
</tr>
<tr>
<td><strong>Data</strong></td>
<td>Pandas • NumPy • 1700+ Comic Books • 1700+ Cover Images</td>
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
- **6GB+ RAM** (8GB+ recommended)
- **8-10GB disk space** (more with data files)

### Quick Start

Choose your setup method:

**Option 1: Docker Hub Images (5 minutes - Easiest)**
```bash
docker-compose up -f ./docker-compose.remote-pull.yaml -d
```
👉 **[Full guide →](docs/INSTALLATION_DOCKER_HUB.md)**

**Option 2: Build Locally (30 minutes)**
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

⚠️ **Known Issues/Quirks**: 
1. The facet control filter switch is **sometimes** finicky and needs 2-3 clicks to toggle properly. This is a known bug of the research implementation.
2. If you hover on same book twice, then you may see different set of keywords. This is because we have mined multiple keywords based on 5W(Who/When/What/Why/Where)1H(How). Keywords shown randomly across each category.

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
```

## ⚠️ Important: Large Files

Due to size (~1.5GB), are also provided separately to help local builds.

❌ **Comic Book Covers** (~1700+ JPEGs, 1GB)
→ Download from: `[Link provided separately]`
→ Extract to: `react_frontend_ui/public/comic_book_covers_ui/`

❌ **Metadata Files** (CSV/XLSX, 300MB)
→ Download from: `[Link provided separately]`
→ Extract to: `python_backend_api/data/metadata/`

👉 **[Setup instructions →](docs/INSTALLATION_LOCAL.md#data-requirements)**


See [DOCKER_OPTIMIZATION_GUIDE.md](./DOCKER_OPTIMIZATION_GUIDE.md) for details.

## 📚 Documentation

All documentation is in the `docs/` folder:

| Document | Purpose |
|----------|----------|
| [COMPLETE_REFERENCE](docs/Master_Thesis_Suraj__final_version.pdf)| Additional information|
| [PRESENTATION_SLIDES](docs/Master_Thesis_Defense_v4.pdf)| Presentation Slides|
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


## 📄 Citation

```bibtex
@article{escomic_2026,
  title={ESCOMIC: User Adaptive Explainable Search for Comic Books},
  author={Suraj Shashidhar, Sayantan Polley, Mounit Roy, Andreas Nurnberger},
  journal={SIGIR 2026},
  year={2026}
}
```

## 📞 Support

- 📚 [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- 🐛 Create an issue on GitHub
- 📧 Contact maintainers

---

