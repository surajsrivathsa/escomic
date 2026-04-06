# ESCOMIC: Installation from Docker Hub 🐳

The quickest way to run ESCOMIC. Pre-built images include all data and comic book covers.

## Prerequisites

- Docker & Docker Compose
- 6GB+ RAM
- 10GB+ disk space

## Quick Start

### 1. Pull Images

```bash
docker pull ssubuntu/escomic-backend:latest
docker pull ssubuntu/escomic-frontend:latest
```

### 2. Run with Docker Compose

```bash
# Use the provided compose file
docker compose -f docker-compose.remote-pull.yaml up -d

# Or start individually
docker run -d -p 8000:8000 ssubuntu/escomic-backend:latest
docker run -d -p 3000:3000 ssubuntu/escomic-frontend:latest
```

### 3. Access

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

## Common Commands

```bash
# Stop services
docker compose down

# View logs
docker compose logs -f backend    # Backend logs
docker compose logs -f frontend   # Frontend logs

# Restart
docker compose restart

# Clean up
docker compose down -v
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change port in compose file or: `docker ps` → `docker stop <container>` |
| Memory errors | Allocate more RAM to Docker |
| Stale images | `docker pull <image>` and rebuild |

## More Info

- [Systems Guide](./SYSTEMS.md)
- [Docker Commands](./DOCKER_COMMANDS.md)
- [Troubleshooting](./TROUBLESHOOTING.md)
