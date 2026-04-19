# ESCOMIC 📚

**Adaptive and Explainable Search for Comics** — An intelligent comic book search system with personalization, explainable AI, and interactive relevance feedback.

## Overview

This is research-backed comic book search system that:

✨ **Searches Beyond Metadata** — Use visual & textual content, not just titles/genres

✨ **Explains Results** — Understand *why* results were returned with interactive explanations

✨ **Learns From You** — Personalization via implicit user feedback (mouse hover tracking)

✨ **6 Research Systems** — Compare different approaches: Wayne, Stark, Croft, Butcher, Gray, BM25

✨ **Production Ready** — Optimized Docker images, API documentation, full stack setup

**For setup instructions, see:**
- **Easiest:** [INSTALLATION_DOCKER_HUB.md](docs/INSTALLATION_DOCKER_HUB.md) — 5 minutes with pre-built images
- **Build Locally:** [INSTALLATION_LOCAL.md](docs/INSTALLATION_LOCAL.md) — Build from source

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

Select from Wayne, Stark, Croft, Butcher, Gray, or BM25:

- **Wayne** ⭐ (Recommended) - Full features
- **Stark** - Test comparison quality
- **Croft** - Test explanation quality
- **Butcher** - Baseline (no personalization)
- **Gray** - Random personalization control
- **BM25** 🆕 *(Added April 10 2026)* - Probabilistic text ranking + free-text search

> **BM25 variant note (April 10 2026):** A BM25-based search variant was added alongside a free-text search capability. Unlike all other variants which require selecting a book as the query, **any variant** can now accept raw text input in the search bar (e.g. "batman detective crime") — results are powered by BM25 ranking. The BM25 variant additionally uses BM25 for query-by-example book-click searches, replacing TF-IDF cosine similarity.

👉 **[System Details →](docs/SYSTEMS.md)**

## API Documentation

Interactive API docs available at `http://localhost:8000/docs` (Swagger UI)

### Search Endpoints

| Endpoint | Method | Used By | Description |
|----------|--------|---------|-------------|
| `/book_search` | POST | Wayne, Stark, Croft | Book-click search with personalization & reranking |
| `/book_search_with_no_personalization` | POST | Butcher | Book-click search, no personalization |
| `/book_search_with_random_serp_results` | POST | Gray | Book-click search, random reranking |
| `/book_search_with_random_explanation_feedback` | POST | Croft | Book-click search, random explanation |
| `/book_search_with_bm25` | POST | **BM25** | Book-click search using BM25 probabilistic ranking |

### Search Bar Endpoints

| Endpoint | Method | Used By | Description |
|----------|--------|---------|-------------|
| `/book_search_with_searchbar_inputs` | POST | Wayne, Stark, Croft, Butcher | Search bar (book select or free-text via BM25) |
| `/book_search_with_searchbar_inputs_and_random_serp` | POST | Gray | Search bar with random reranking (or free-text via BM25) |
| `/book_search_with_bm25_searchbar` | POST | **BM25** | Search bar with BM25 for both book-select and free-text |

> **Free-text search (all variants):** All searchbar endpoints accept `type: "free text"` queries — BM25 is used as the engine, all facet weights default to 1.0, and a random explanation is generated.

### Explanation & Utility Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/local_explanation` | POST | Explain similarity between two books |
| `/compare_books` | POST | Compare two books with explanation |
| `/compare_books_with_random` | POST | Compare two books, randomized explanation (Stark) |
| `/view_comic_book` | GET | Get full book details |
| `/start_session` | GET | Create new user session |

## ⚠️ Important: Large Files

Due to size (~1.5GB), are also provided separately to help local builds. If you are using dockerhub based docker images then this is not necessary for you as images and feature vector files are already included inside docker image on hub.

❌ **Comic Book Covers** (~1700+ JPEGs, 1GB)
→ Download from: [https://1drv.ms/u/c/ca9d6b4b08cafad5/IQAOXakqjpCoT6uoGtMJDYJ7AZ49rat6QJoCWk2XH8jpakI?e=hYwPQE](https://1drv.ms/u/c/ca9d6b4b08cafad5/IQAOXakqjpCoT6uoGtMJDYJ7AZ49rat6QJoCWk2XH8jpakI?e=hYwPQE)
→ Extract to: `react_frontend_ui/public/comic_book_covers_ui/`

❌ **Metadata Files** (CSV/XLSX, 300MB)
→ Download from: [https://1drv.ms/u/c/ca9d6b4b08cafad5/IQB5sn0zhH3PR4AxnKQsWkfbASejNBIrv0a4Ra-2lRGH8pk?e=3nR3pi](https://1drv.ms/u/c/ca9d6b4b08cafad5/IQB5sn0zhH3PR4AxnKQsWkfbASejNBIrv0a4Ra-2lRGH8pk?e=3nR3pi)
→ Extract to: `python_backend_api/data/metadata/`

👉 **[Setup instructions →](docs/INSTALLATION_LOCAL.md#data-requirements)**


See [DOCKER_OPTIMIZATION_GUIDE.md](./DOCKER_OPTIMIZATION_GUIDE.md) for details.




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

