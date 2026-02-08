# ESCOMIC: Docker Commands Reference

Quick reference for common Docker and Docker Compose commands for ESCOMIC.

## Docker Compose Basics

### Start Services

```bash
# Start all services in background
docker-compose up -d

# Start with logs visible
docker-compose up

# Start with optimized images (recommended)
docker-compose -f docker-compose.optimized.yml up -d

# Start from Docker Hub images
docker-compose -f docker-compose.remote-pull.yaml up -d
```

### Stop & Remove Services

```bash
# Stop all services (data persists)
docker-compose down

# Stop and remove volumes (careful - data deleted)
docker-compose down -v

# Stop without removing containers
docker-compose stop

# Remove stopped containers
docker-compose rm
```

### View Status

```bash
# List running containers
docker-compose ps

# Detailed container info
docker-compose ps -a

# Check all Docker containers running
docker ps
docker ps -a
```

---

## Building Images

### Build Images Locally

```bash
# Build all images
docker-compose build

# Build without cache (fresh build)
docker-compose build --no-cache

# Build specific service
docker-compose build backend_optimized
docker-compose build frontend_optimized

# Build with progress output
docker-compose build --progress=plain
```

### Using Build Script

```bash
# Make executable
chmod +x build_optimized.sh

# Build both backend and frontend
./build_optimized.sh --both

# Build only backend
./build_optimized.sh --backend

# Build only frontend
./build_optimized.sh --frontend
```

---

## Logs & Debugging

### View Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend_optimized
docker-compose logs frontend_optimized

# View last 100 lines
docker-compose logs -n 100

# Follow logs in real-time
docker-compose logs -f

# Follow specific service
docker-compose logs -f backend_optimized

# View logs from specific time
docker-compose logs --since 10m  # Last 10 minutes
```

### Container Inspection

```bash
# Inspect container
docker inspect <container_name>

# Get container's IP
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_id>

# View environment variables
docker exec <container_id> printenv

# View running processes in container
docker exec <container_id> ps aux
```

---

## Individual Service Control

### Start Individual Services

```bash
# Start only backend (and dependencies)
docker-compose up backend_optimized

# Start only frontend
docker-compose up frontend_optimized

# Start and build
docker-compose up --build backend_optimized
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend_optimized
docker-compose restart frontend_optimized

# Full rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## Volume & Data Management

### List Volumes

```bash
# List all volumes
docker volume ls

# Inspect specific volume
docker volume inspect <volume_name>

# Check volume size/location
docker volume inspect escomic_data
```

### Copy Files to/from Containers

```bash
# Copy from host to container
docker cp ./comic_covers_ui/ backend_optimized:/api/data/

# Copy from container to host
docker cp backend_optimized:/api/output ./local_output/

# Using docker-compose
docker-compose exec backend_optimized cp /source /dest
```

### Mount Bind

```bash
# Verify bind mounts
docker inspect -f '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{end}}' <container_id>
```

---

## Network Troubleshooting

### Network Info

```bash
# List networks
docker network ls

# Inspect specific network
docker network inspect escomic-network

# Check container's network settings
docker inspect --format='{{.NetworkSettings.Networks}}' <container_id>
```

### Test Connectivity

```bash
# Ping from container to host/other container
docker-compose exec backend_optimized ping frontend_optimized

# Test port access
docker-compose exec backend_optimized curl http://frontend_optimized:3000

# From host to backend API
curl http://localhost:8000/docs
```

---

## Image Management

### List Images

```bash
# List all images
docker images

# Show image sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# Filter by name
docker images | grep escomic
```

### Pull Images

```bash
# Pull backend from Docker Hub
docker pull ssubuntu/escomic-backend:latest

# Pull frontend from Docker Hub
docker pull ssubuntu/escomic-frontend:latest

# Pull specific version/tag
docker pull ssubuntu/escomic-backend:v1.0
```

### Remove Images

```bash
# Remove specific image
docker rmi <image_id>

# Remove unused images
docker image prune

# Remove all unused (even dangerous ones)
docker image prune -a

# Force remove (careful!)
docker rmi -f <image_id>
```

---

## Resource Monitoring

### Check Resource Usage

```bash
# Real-time stats
docker stats

# Stats for specific container
docker stats backend_optimized frontend_optimized

# Non-streaming stats
docker stats --no-stream
```

### System Info

```bash
# Docker system info
docker system info

# Disk usage
docker system df

# Disk usage detailed
docker system df -v
```

---

## Cleanup Commands

### Remove Everything Safely

```bash
# Stop all services
docker-compose down

# Remove unused containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# All at once
docker system prune
```

### Nuclear Option (Remove All)

```bash
# Remove stopped containers
docker rm $(docker ps -a -q)

# Remove all images
docker rmi $(docker images -a -q)

# Remove all volumes
docker volume rm $(docker volume ls -q)

# Full reset
docker system prune -a --volumes
```

---

## Running Direct Commands in Containers

### Backend Commands

```bash
# Run Python command
docker-compose exec backend_optimized python -c "import pandas; print(pandas.__version__)"

# Check installed packages
docker-compose exec backend_optimized pip list

# Run tests
docker-compose exec backend_optimized pytest

# Access Python shell
docker-compose exec backend_optimized python
```

### Frontend Commands

```bash
# Run npm commands
docker-compose exec frontend_optimized npm list

# Check Node version
docker-compose exec frontend_optimized node --version

# Run npm scripts
docker-compose exec frontend_optimized npm run build
```

### Bash Shell Access

```bash
# Backend shell
docker-compose exec backend_optimized /bin/bash

# Frontend shell
docker-compose exec frontend_optimized /bin/bash

# Check directory structure
docker-compose exec backend_optimized ls -la /api/data/
```

---

## Common Workflows

### Development Cycle

```bash
# 1. Make code changes locally
# 2. Rebuild without cache
docker-compose build --no-cache backend_optimized

# 3. Restart service
docker-compose restart backend_optimized

# 4. Check logs
docker-compose logs -f backend_optimized

# 5. Test
# Open browser or run curl commands
```

### Debug Production Issue

```bash
# 1. Check if running
docker-compose ps

# 2. View recent logs
docker-compose logs -n 50 backend_optimized

# 3. Check resource usage
docker stats

# 4. SSH into container
docker-compose exec backend_optimized /bin/bash

# 5. Restart if needed
docker-compose restart backend_optimized
```

### Data Backup

```bash
# Backup volumes
docker run --rm -v escomic_data:/data -v $(pwd):/backup alpine tar czf /backup/data-backup.tar.gz /data

# Restore volumes
docker run --rm -v escomic_data:/data -v $(pwd):/backup alpine tar xzf /backup/data-backup.tar.gz -C /
```

---

## Docker Compose Files

### Using Different Compose Files

```bash
# Use specific docker-compose file
docker-compose -f docker-compose.yml up -d
docker-compose -f docker-compose.optimized.yml up -d
docker-compose -f docker-compose.remote-pull.yaml up -d

# Use multiple compose files (merge)
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

# Multiple projects
docker-compose --project-name escomic1 up -d
docker-compose --project-name escomic2 up -d
```

---

## Performance Optimization

### Build Optimization

```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker-compose build

# Parallel builds
docker-compose build --parallel
```

### Runtime Optimization

```bash
# Use optimized images (smaller, faster)
docker-compose -f docker-compose.optimized.yml up -d

# Check image sizes
docker images | grep escomic
```

---

## Useful Shortcuts

Add to `.bashrc` or `.zshrc`:

```bash
# Start ESCOMIC
alias escomic-start="docker-compose -f docker-compose.optimized.yml up -d"

# Stop ESCOMIC
alias escomic-stop="docker-compose down"

# View logs
alias escomic-logs="docker-compose logs -f"

# Backend logs
alias escomic-backend-logs="docker-compose logs -f backend_optimized"

# Frontend logs
alias escomic-frontend-logs="docker-compose logs -f frontend_optimized"

# SSH into backend
alias escomic-backend-ssh="docker-compose exec backend_optimized /bin/bash"

# SSH into frontend
alias escomic-frontend-ssh="docker-compose exec frontend_optimized /bin/bash"
```

Then use: `escomic-start`, `escomic-logs`, etc.

---

## Next Steps

- See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues
- Check [INSTALLATION_LOCAL.md](./INSTALLATION_LOCAL.md) for setup
- Review [SYSTEMS.md](./SYSTEMS.md) for system info
- Go back to [README](../README.md)
