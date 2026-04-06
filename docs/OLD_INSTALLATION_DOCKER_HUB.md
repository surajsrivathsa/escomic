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

Use the `docker-compose.remote-pull.yaml` file in your project root:

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
# Start services
docker-compose up -d

# Check if running
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Access Application

- **Frontend**: http://localhost:3000
- **APIs**: http://localhost:8000/docs

## Data Requirements

### Comic Book Covers (Required)

The pre-built images do **NOT** include comic book cover images (~1GB).

**Steps:**

1. Download covers from: `https://1drv.ms/u/c/ca9d6b4b08cafad5/IQAOXakqjpCoT6uoGtMJDYJ7AZ49rat6QJoCWk2XH8jpakI?e=hYwPQE`
2. Unzip the archive
3. Copy JPEG files to: `./react_frontend_ui/public/comic_book_covers_ui/`

```bash
unzip comic_covers.zip
cp -r comic_covers_ui/*.jpeg react_frontend_ui/public/comic_book_covers_ui/
```

### Metadata Files (Optional but Recommended)

For full functionality including OCR'ed texts and metadata:

1. Download metadata from: `https://1drv.ms/u/c/ca9d6b4b08cafad5/IQB5sn0zhH3PR4AxnKQsWkfbASejNBIrv0a4Ra-2lRGH8pk?e=3nR3pi`
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
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Remove everything (careful!)
docker-compose down -v
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
