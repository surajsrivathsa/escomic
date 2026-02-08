# ESCOMIC: Installation from Docker Hub (Recommended) 🐳

This is the **quickest and easiest way** to run ESCOMIC without building anything locally.

## Prerequisites

- Docker & Docker Compose installed
- 4GB+ available RAM
- 2GB+ disk space for images

## Installation Steps

### 1. Pull Pre-Built Images

```bash
# Navigate to project directory
cd escomic

# Pull latest images from Docker Hub
docker pull ssubuntu/escomic-backend:latest
docker pull ssubuntu/escomic-frontend:latest
```

### 2. Create Compose File

Create a `docker-compose.remote-pull.yaml` file in your project root:

```yaml
version: '3.8'

services:
  backend:
    image: ssubuntu/escomic-backend:latest
    container_name: escomic-backend
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
      - PYTHONDONTWRITEBYTECODE=1
    volumes:
      - ./python_backend_api/data/metadata:/api/data/metadata
      - ./python_backend_api/features:/api/features
    networks:
      - escomic-network

  frontend:
    image: ssubuntu/escomic-frontend:latest
    container_name: escomic-frontend
    ports:
      - "3000:3000"
      - "80:80"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    volumes:
      - ./react_frontend_ui/public/comic_book_covers_ui:/mnt/comic_covers
    depends_on:
      - backend
    networks:
      - escomic-network

networks:
  escomic-network:
    driver: bridge
```

### 3. Start Services

```bash
# Start all services in background
docker-compose -f docker-compose.remote-pull.yaml up -d

# Check if services are running
docker-compose -f docker-compose.remote-pull.yaml ps

# View logs
docker-compose -f docker-compose.remote-pull.yaml logs -f
```

### 4. Access the Application

- **Frontend**: http://localhost:3000 or http://localhost:80
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Data Requirements

### Comic Book Covers (Required)

The pre-built images do **NOT** include comic book cover images (~1GB).

**Steps:**

1. Download covers from: `[Link to be provided]`
2. Unzip the archive
3. Copy JPEG files to: `./react_frontend_ui/public/comic_book_covers_ui/`

```bash
unzip comic_covers.zip
cp -r comic_covers_ui/*.jpeg react_frontend_ui/public/comic_book_covers_ui/
```

### Metadata Files (Optional but Recommended)

For full functionality including OCR'ed texts and metadata:

1. Download metadata from: `[Link to be provided]`
2. Unzip the archive
3. Copy CSV/XLSX files to: `./python_backend_api/data/metadata/`

```bash
unzip metadata.zip
cp -r metadata/*.csv python_backend_api/data/metadata/
cp -r metadata/*.xlsx python_backend_api/data/metadata/
```

## Quick Commands

```bash
# Stop all services
docker-compose -f docker-compose.remote-pull.yaml down

# View service logs
docker-compose -f docker-compose.remote-pull.yaml logs -f backend
docker-compose -f docker-compose.remote-pull.yaml logs -f frontend

# Check image sizes
docker images | grep ssubuntu

# Remove everything (careful!)
docker-compose -f docker-compose.remote-pull.yaml down -v
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Port 3000/8000 already in use** | Change ports in docker-compose file or kill existing process |
| **Images don't update** | Run `docker pull` again and rebuild |
| **Out of memory** | Ensure 4GB+ RAM available, close other apps |

## Next Steps

- See [SYSTEMS.md](./SYSTEMS.md) to learn about different search systems
- See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for known issues
- Check [DOCKER_COMMANDS.md](./DOCKER_COMMANDS.md) for advanced Docker commands
