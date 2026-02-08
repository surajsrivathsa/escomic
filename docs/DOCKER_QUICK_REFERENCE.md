# Docker Optimization Quick Reference

## Problem
- **Frontend**: 3.38GB (includes all node_modules + 1500+ comic book images)
- **Backend**: 4.46GB (includes all Python packages + large ML models)
- **Total**: 7.84GB

## Solution
Multi-stage builds + Volume mounting for large assets

## Quick Start

### 1. Make build script executable
```bash
chmod +x build_optimized.sh
```

### 2. Build optimized images
```bash
# Build both
./build_optimized.sh --both

# Or specific ones
./build_optimized.sh --frontend
./build_optimized.sh --backend
```

### 3. Run with docker-compose
```bash
docker-compose -f docker-compose.optimized.yml up -d
```

### 4. Verify services
```bash
# Check images
docker images | grep optimized

# Check containers
docker ps | grep optimized

# Frontend: http://localhost:3000 or http://localhost:80
# Backend API: http://localhost:8000
```

---

## Expected Size Reduction

| Component | Before | After | Saved |
|-----------|--------|-------|-------|
| Frontend | 3.38GB | ~450MB | 2.93GB (86.7%) |
| Backend | 4.46GB | ~1.4GB | 3.06GB (68.6%) |
| **Total** | **7.84GB** | **~1.85GB** | **~6GB (76.4%)** |

---

## Files Created

1. **react_frontend_ui/Dockerfile.optimized**
   - Multi-stage build with Node → Nginx
   - Removes all node_modules from final image
   - Serves static built assets

2. **react_frontend_ui/nginx.conf**
   - SPA routing configuration
   - Gzip compression enabled
   - Long-term caching for assets
   - Volume mount for comic covers (as /mnt/comic_covers)

3. **react_frontend_ui/.dockerignore.optimized**
   - Excludes comic book cover images from build context
   - Prevents copy of node_modules, build artifacts

4. **python_backend_api/Dockerfile.optimized**
   - Multi-stage build to separate build and runtime
   - Python 3.11-slim base (smaller than 3.8)
   - Only installs runtime dependencies

5. **python_backend_api/.dockerignore**
   - Excludes data directories
   - Excludes Python cache files
   - Prevents copy of unnecessary files

6. **docker-compose.optimized.yml**
   - Configured with volume mounts
   - Services connected via network
   - Proper port mappings

---

## Volume Mounts Explanation

### Frontend
```yaml
volumes:
  - ./react_frontend_ui/public/comic_book_covers_ui:/mnt/comic_covers:ro
```
- Mounts comic book images as read-only volume
- Served by Nginx from /mnt/comic_covers path
- **Saves ~1.5GB in image size**

### Backend  
```yaml
volumes:
  - ./python_backend_api/data:/api/data
```
- Mounts data folder as volume
- App accesses CSV files and other data
- **Allows dynamic data updates without rebuilding**

---

## API Configuration

If you need to access backend API from frontend, update the frontend build environment variable. In docker-compose.optimized.yml, the REACT_APP_API_URL is set to:

```yaml
REACT_APP_API_URL=http://backend:8000
```

This works within the Docker network. For external access, you might need to adjust based on your deployment.

---

## Development vs Production

### For Development (use original Dockerfile)
- Includes hot reload capability
- Access to node_modules
- Development server with better error messages

### For Production (use Dockerfile.optimized)
- Smaller images
- Better performance with Nginx
- Read-only file systems for security
- Volume-based data management

---

## Common Operations

### Check image sizes
```bash
docker images | grep -E "(frontend|backend)"
```

### View volume mounts
```bash
docker inspect <container_id> | grep -A 10 Mounts
```

### Remove old images
```bash
docker rmi frontend:latest backend:latest
```

### Rebuild and restart
```bash
docker-compose -f docker-compose.optimized.yml build --no-cache
docker-compose -f docker-compose.optimized.yml down
docker-compose -f docker-compose.optimized.yml up -d
```

---

## Troubleshooting

### Frontend images not loading
- Check nginx.conf location path
- Verify volume is readable: `ls -la react_frontend_ui/public/comic_book_covers_ui/`
- Check container logs: `docker logs frontend_optimized`

### Backend file not found errors  
- Ensure data volume is mounted: `docker volume ls`
- Verify file exists in local path
- Check permissions on data folder

### Port already in use
```bash
# Change ports in docker-compose.optimized.yml
# Or kill existing container
docker stop <container_id>
```

### Need to see container logs
```bash
docker logs -f <container_id>
```

---

## Advanced: Push to Registry

```bash
# Build and push to registry
./build_optimized.sh --both --push your-registry.com/myapp --tag v1.0
```

---

## Notes

- The `.dockerignore` files prevent large files from being copied during build
- Layer caching is optimized for faster rebuilds
- Both images use Alpine-based minimal distributions
- Data persistence is handled via volumes, not image layers
- Images are production-ready and follow Docker best practices

---

## Contact / Support

For issues with the optimized builds:
1. Check the DOCKER_OPTIMIZATION_GUIDE.md for detailed documentation
2. Review nginx.conf for routing issues
3. Check volume mount permissions
4. Verify all services are healthy: `docker-compose -f docker-compose.optimized.yml logs`
