# ESCOMIC: Troubleshooting Guide

Solutions for common issues and known quirks.

## Known Issues

### ⚠️ Facet Control Flip Switch Behavior

**Issue:** The facet control filter switch is finicky and may require pressing **2-3 times** to toggle properly.

**Why:** 
- State synchronization delay between frontend UI and backend
- React re-render timing with filter application

**Solutions:**

1. **Quick Fix:** Click the switch 2-3 times in succession
2. **Workaround:** Toggle filter off, wait 1 second, then toggle on
3. **Workaround:** Refresh page and reapply filters

**Example:**
```
Click filter switch → No change seen
Click again → Filter starts applying
Click third time → Filter properly toggles
```

**Reported Status:** Known quirk, works as intended for research (testing user persistence)

---

## Installation Issues

### Comic Book Covers Not Displaying

**Symptoms:**
- Frontend loads but book covers show as broken images
- Grid shows placeholder images

**Solutions:**

1. **Check folder exists:**
   ```bash
   ls -la react_frontend_ui/public/comic_book_covers_ui/
   # Should show 5000+ JPEG files
   ```

2. **Verify file permissions:**
   ```bash
   chmod 644 react_frontend_ui/public/comic_book_covers_ui/*.jpeg
   ```

3. **Check Docker volume mount:**
   ```bash
   docker inspect frontend_optimized | grep -A 20 Mounts
   # Should show volume mapped to /mnt/comic_covers
   ```

4. **Rebuild and restart:**
   ```bash
   docker-compose down
   docker-compose up --build -d
   ```

5. **Check nginx config (if using production):**
   ```bash
   docker exec frontend_optimized cat /etc/nginx/conf.d/default.conf
   # Should include location for /comic_book_covers_ui/
   ```

---

### Search Returns No Results

**Symptoms:**
- Search works but always returns 0 results
- Error message or empty grid

**Solutions:**

1. **Check metadata files exist:**
   ```bash
   ls -la python_backend_api/data/metadata/
   # Should contain: comic_info_df.csv, COMICS_ocr_file.csv, etc.
   ```

2. **Verify CSV files aren't corrupted:**
   ```bash
   head python_backend_api/data/metadata/comic_info_df.csv
   # Should show readable data
   ```

3. **Check backend logs:**
   ```bash
   docker-compose logs backend_optimized | tail -50
   # Look for errors like "FileNotFoundError" or "pandas read error"
   ```

4. **Verify file permissions:**
   ```bash
   chmod 644 python_backend_api/data/metadata/*.csv
   ```

5. **Rebuild search index:**
   ```bash
   docker-compose down
   docker-compose up --build -d
   ```

---

### Backend API Connection Error

**Symptoms:**
- Frontend shows "Cannot connect to backend"
- Network error in browser console

**Solutions:**

1. **Check backend is running:**
   ```bash
   docker ps | grep backend
   # Should show running container
   ```

2. **Check port 8000 is accessible:**
   ```bash
   curl http://localhost:8000/docs
   # Should return Swagger UI page
   ```

3. **Check API health:**
   ```bash
   docker-compose logs backend_optimized | grep "Application startup complete"
   ```

4. **Check environment variables (Docker):**
   ```bash
   docker exec backend_optimized printenv | grep API
   ```

5. **Verify network connectivity:**
   ```bash
   docker network ls
   docker network inspect escomic-network
   ```

6. **Restart services:**
   ```bash
   docker-compose restart backend_optimized backend_optimized
   docker-compose logs backend_optimized
   ```

---

### Port Already in Use

**Symptoms:**
- Error: `Address already in use` when starting services
- Cannot bind to port 3000, 8000, or 80

**Solutions:**

1. **Find process using port:**
   ```bash
   lsof -i :3000    # Frontend
   lsof -i :8000    # Backend
   lsof -i :80      # Nginx
   ```

2. **Kill existing process:**
   ```bash
   kill -9 <PID>
   ```

3. **Or change ports in docker-compose:**
   ```bash
   # Edit docker-compose.yml
   ports:
     - "3001:3000"   # Changed from 3000:3000
     - "8001:8000"   # Changed from 8000:8000
   ```

4. **Use different Docker network:**
   ```bash
   docker-compose -f docker-compose.yml --project-name escomic2 up -d
   ```

---

### Memory Issues

**Symptoms:**
- Services crash unexpectedly
- Backend stops responding
- Docker container restarts repeatedly

**Solutions:**

1. **Check Docker memory allocation:**
   ```bash
   docker stats
   # Check if any container near limit
   ```

2. **Increase Docker memory (Desktop):**
   - Open Docker Desktop settings
   - Go to Resources
   - Increase Memory slider (recommend 8GB+)
   - Click Apply & Restart

3. **Limit container memory:**
   ```bash
   # Edit docker-compose
   services:
     backend_optimized:
       mem_limit: 4g
     frontend_optimized:
       mem_limit: 2g
   ```

4. **Free up system memory:**
   ```bash
   # Close other applications
   docker system prune  # Remove unused images/containers
   ```

---

## Performance Issues

### Slow Search Results

**Symptoms:**
- Search takes 5+ seconds
- API responses are slow

**Solutions:**

1. **Check backend CPU usage:**
   ```bash
   docker stats backend_optimized
   ```

2. **Check if data files are on fast storage:**
   ```bash
   df -h python_backend_api/data/
   # Avoid slow network drives
   ```

3. **View backend logs for bottlenecks:**
   ```bash
   docker-compose logs backend_optimized | grep "took\|duration\|time"
   ```

4. **Consider using optimized images:**
   ```bash
   docker-compose -f docker-compose.optimized.yml up -d
   # Instead of standard version
   ```

---

### Frontend Lag

**Symptoms:**
- UI is slow to respond
- Typing search query feels laggy
- Filter switches respond slowly

**Solutions:**

1. **Check browser developer tools:**
   - Press F12
   - Go to Performance tab
   - Record interaction, check for long tasks

2. **Clear cache:**
   ```bash
   # Hard refresh in browser
   Ctrl+Shift+R (or Cmd+Shift+R on Mac)
   ```

3. **Check network tab:**
   - Look for slow API calls
   - Check image sizes

4. **Close browser tabs/extensions:**
   - Other tabs can slow performance
   - Try in incognito mode

---

## Docker Issues

### Images Not Updating

**Symptoms:**
- Changes don't appear after rebuilding
- Old version still running

**Solutions:**

```bash
# Full rebuild without cache
docker-compose build --no-cache

# Remove old images
docker rmi escomic-backend escomic-frontend

# Pull fresh images
docker pull ssubuntu/escomic-backend:latest
docker pull ssubuntu/escomic-frontend:latest

# Restart
docker-compose up -d
```

---

### Disk Space Issues

**Symptoms:**
- Cannot build images
- "No space left on device" error

**Solutions:**

```bash
# Check Docker disk usage
docker system df

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune -a

# Remove unused containers
docker container prune -a

# Clean everything (careful!)
docker system prune -a
```

---

## Getting Help

### Check Logs

Always start here:

```bash
# Backend logs
docker-compose logs backend_optimized -n 100

# Frontend logs
docker-compose logs frontend_optimized -n 100

# All logs
docker-compose logs -n 100

# Follow live logs
docker-compose logs -f
```

### Run Diagnostics

```bash
# Check all services
docker-compose ps

# Check image sizes
docker images | grep -E "(backend|frontend)"

# Check volumes
docker volume ls

# Check networks
docker network ls

# Full system check
docker system info
```

---

## System Switching Issues

### Can't Change Systems (Wayne/Stark/Croft/Butcher/Gray)

**Symptoms:**
- System selector missing
- Selection doesn't persist
- Always defaults to Wayne

**Solutions:**

1. **Check frontend state:**
   - Hard refresh browser (Ctrl+Shift+R)

2. **Check session storage:**
   - Open browser DevTools (F12)
   - Go to Application → Local Storage
   - Look for system preference key

3. **Check API endpoint mapping:**
   ```bash
   # In constants.js should have entries for all systems
   grep "SYSTEMS_TO_API_ENDPOINT" -A 30
   ```

---

## Advanced Troubleshooting

### Enable Debug Logging

**Backend:**
```bash
# Edit docker-compose to add debug flag
environment:
  - DEBUG=1
  - LOG_LEVEL=DEBUG
```

**Frontend:**
```bash
# Set in .env
REACT_APP_DEBUG=true
```

### SSH into Container

```bash
# Backend
docker exec -it backend_optimized /bin/bash

# Frontend
docker exec -it frontend_optimized /bin/bash
```

---

## Still Having Issues?

1. Check [INSTALLATION_DOCKER_HUB.md](./INSTALLATION_DOCKER_HUB.md) or [INSTALLATION_LOCAL.md](./INSTALLATION_LOCAL.md)
2. Review [DOCKER_COMMANDS.md](./DOCKER_COMMANDS.md) for command reference
3. Check [SYSTEMS.md](./SYSTEMS.md) for system-specific features
4. Review project README for general info

---

## Contact

For persistent issues or feature requests, please create an issue in the repository with:
- Steps to reproduce
- Docker logs output
- System information (OS, Docker version)
- Screenshots if applicable
