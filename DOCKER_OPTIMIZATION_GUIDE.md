# Docker Image Optimization Guide

## Overview
This guide explains the optimized Dockerfiles and how to use them to reduce image sizes from ~7.84GB combined to approximately ~2GB combined.

## Key Optimizations

### Frontend (React) - Dockerfile.optimized

**Problem**: Original image was ~3.38GB due to:
- Full node_modules (dev dependencies)
- All book cover images (~1.5GB+)
- Build artifacts

**Solution**: 
1. **Multi-stage build**: 
   - Stage 1: Build app in Node container with dependencies
   - Stage 2: Deploy only built artifacts to lightweight Nginx
   
2. **Volume mounting for images**:
   - Comic book covers served from mounted volume instead of embedded in image
   - Reduces image size from ~3.38GB to ~400-500MB

3. **Nginx advantages**:
   - Much smaller base (25MB vs 300MB+ Node)
   - Built-in compression and caching headers
   - Better performance for static content
   - Production-ready

**Estimated size reduction**: 3.38GB → ~450MB

### Backend (Python) - Dockerfile.optimized

**Problem**: Original image was ~4.46GB due to:
- All dependencies including heavy ML packages
- No separation of build and runtime dependencies
- Included data files

**Solution**:
1. **Multi-stage build**:
   - Stage 1: Build wheels with all dependencies
   - Stage 2: Install only runtime dependencies on clean base
   
2. **Python 3.11-slim base**:
   - Smaller than 3.8-slim
   - Better performance
   - Reduced layer size

3. **Volume mounting for data**:
   - data/ folder mounted as volume
   - models/ folder can be mounted separately
   - Reduces image size from ~4.46GB to ~1.2-1.5GB

**Estimated size reduction**: 4.46GB → ~1.4GB

---

## Building the Optimized Images

### Option 1: Using the optimized docker-compose file

```bash
# Build optimized images
docker-compose -f docker-compose.optimized.yml build

# Start services
docker-compose -f docker-compose.optimized.yml up -d
```

### Option 2: Manual build

**Frontend:**
```bash
cd react_frontend_ui
docker build -f Dockerfile.optimized -t frontend:optimized .
```

**Backend:**
```bash
cd python_backend_api
docker build -f Dockerfile.optimized -t backend:optimized .
```

---

## Running with Volumes

### Using docker-compose
The `docker-compose.optimized.yml` already includes proper volume configuration.

### Manual volume mounting

**Frontend:**
```bash
docker run -d \
  --name frontend_optimized \
  -p 3000:3000 \
  -p 80:80 \
  -v $(pwd)/react_frontend_ui/public/comic_book_covers_ui:/mnt/comic_covers:ro \
  frontend:optimized
```

**Backend:**
```bash
docker run -d \
  --name backend_optimized \
  -p 8000:8000 \
  -v $(pwd)/python_backend_api/data:/api/data \
  -v backend_models_cache:/root/.cache \
  backend:optimized
```

---

## Nginx Configuration

The `nginx.conf` provides:
- Proper React Router handling (SPA support)
- Gzip compression for all text assets
- Long-term caching for static files (JS, CSS, images)
- Volume-based serving for comic covers

To update frontend URL or add API proxy:

```nginx
location /api/ {
    proxy_pass http://backend:8000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

---

## Size Comparison

| Component | Original | Optimized | Reduction |
|-----------|----------|-----------|-----------|
| Frontend | 3.38GB | ~450MB | 86.7% |
| Backend | 4.46GB | ~1.4GB | 68.6% |
| **Total** | **7.84GB** | **~1.85GB** | **76.4%** |

---

## Benefits

1. **Faster deployment**: ~6GB smaller images = faster push/pull to registries
2. **Less storage**: Dramatic reduction in disk usage
3. **Better performance**: Nginx is more efficient than Node for static content
4. **Production-ready**: Using slim base images and production server
5. **Scalability**: Smaller images mean more containers fit per node
6. **Cost reduction**: Smaller images save on storage and bandwidth

---

## Data Management

### Data Volumes
Keep data external to images:

```bash
# Create named volume for backend data
docker volume create thesis_data

# Mount when running
docker run -v thesis_data:/api/data backend:optimized
```

### Model Caching
For Hugging Face and sentence-transformers models:

```bash
# Pre-download models locally
mkdir -p ./models
# Models in ./models get mounted to /root/.cache in container
docker run -v $(pwd)/models:/root/.cache backend:optimized
```

---

## Troubleshooting

**Frontend images not loading?**
- Verify volume is mounted: `docker inspect frontend_optimized | grep -i mounts`
- Check permissions on comic_book_covers_ui directory
- Verify nginx.conf location is correct

**Backend can't find data?**
- Ensure data folder is mounted: `docker volume inspect thesis_data`
- Check file permissions in mounted volume
- Verify path in CMD environment matches mount point

**Need development mode?**
- Use original Dockerfile for development (npm start rebuilds on changes)
- Use optimized Dockerfile only for production

---

## Next Steps

1. Replace old docker-compose.yml or create separate for production
2. Test optimized builds locally
3. Push optimized images to your registry
4. Update deployment scripts
5. Monitor performance metrics

## Additional Notes

- The .dockerignore files prevent unnecessary files from being copied
- Layer caching is optimized for faster rebuilds
- Both images can be further reduced by removing unused dependencies
- Consider implementing docker build cache for even faster builds
