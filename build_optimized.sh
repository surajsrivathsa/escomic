#!/bin/bash

# Docker Image Optimization Build Script
# Builds optimized Docker images with volume mounts for large files

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Docker Image Optimization Build Script${NC}\n"

# Default values
BUILD_FRONTEND=false
BUILD_BACKEND=false
BUILD_BOTH=false
PUSH_TO_REGISTRY=false
REGISTRY=""
TAG="optimized"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --frontend)
      BUILD_FRONTEND=true
      shift
      ;;
    --backend)
      BUILD_BACKEND=true
      shift
      ;;
    --both)
      BUILD_BOTH=true
      shift
      ;;
    --push)
      PUSH_TO_REGISTRY=true
      REGISTRY="$2"
      shift 2
      ;;
    --tag)
      TAG="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# If no specific option, build both
if [ "$BUILD_FRONTEND" = false ] && [ "$BUILD_BACKEND" = false ] && [ "$BUILD_BOTH" = false ]; then
  BUILD_BOTH=true
fi

# Build Frontend
if [ "$BUILD_FRONTEND" = true ] || [ "$BUILD_BOTH" = true ]; then
  echo -e "${YELLOW}Building Frontend (React + Nginx)...${NC}"
  cd react_frontend_ui
  
  docker build -f Dockerfile.optimized -t frontend:${TAG} .
  
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Frontend built successfully${NC}"
    docker images | grep "frontend" | grep ${TAG}
  else
    echo -e "${YELLOW}✗ Frontend build failed${NC}"
    exit 1
  fi
  
  cd ..
fi

# Build Backend
if [ "$BUILD_BACKEND" = true ] || [ "$BUILD_BOTH" = true ]; then
  echo -e "\n${YELLOW}Building Backend (Python + FastAPI)...${NC}"
  cd python_backend_api
  
  docker build -f Dockerfile.optimized -t backend:${TAG} .
  
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backend built successfully${NC}"
    docker images | grep "backend" | grep ${TAG}
  else
    echo -e "${YELLOW}✗ Backend build failed${NC}"
    exit 1
  fi
  
  cd ..
fi

# Push to registry if specified
if [ "$PUSH_TO_REGISTRY" = true ] && [ ! -z "$REGISTRY" ]; then
  echo -e "\n${YELLOW}Pushing images to registry: ${REGISTRY}${NC}"
  
  if [ "$BUILD_FRONTEND" = true ] || [ "$BUILD_BOTH" = true ]; then
    docker tag frontend:${TAG} ${REGISTRY}/frontend:${TAG}
    docker push ${REGISTRY}/frontend:${TAG}
    echo -e "${GREEN}✓ Frontend pushed${NC}"
  fi
  
  if [ "$BUILD_BACKEND" = true ] || [ "$BUILD_BOTH" = true ]; then
    docker tag backend:${TAG} ${REGISTRY}/backend:${TAG}
    docker push ${REGISTRY}/backend:${TAG}
    echo -e "${GREEN}✓ Backend pushed${NC}"
  fi
fi

# Show image sizes
echo -e "\n${BLUE}Image Sizes:${NC}"
docker images | grep -E "(frontend|backend)" | grep ${TAG}

echo -e "\n${GREEN}Build completed successfully!${NC}"
echo -e "\n${BLUE}Next steps:${NC}"
echo "1. Start services with: docker-compose -f docker-compose.optimized.yml up"
echo "2. Check that volumes are mounted correctly"
echo "3. Access frontend at: http://localhost:3000"
echo "4. Access backend API at: http://localhost:8000"
