Here you go — I’ve converted your RTF into clean, readable **Markdown** and kept the structure and commands intact 👍

---

# Docker Commands

## Step 1: Create Image for Backend

```bash
cd git/thesis_deployment/python_backend_api
```

**Python:**

```bash
docker build . -t backend
```

---

## Step 2: Create Image for Frontend

```bash
cd git/thesis_deployment/react_frontend_ui
```

**UI:**

```bash
# add this to requirements.txt before building huggingface_hub==0.13.4 to load sentence transformer correctly
docker build . -t frontend
```

---

## Step 3: Create Network

```bash
docker network create frontend_backend_connection
```

---

## Step 4: Run Images

### Backend (Python)

```bash
cd git/thesis_deployment/python_backend_api
docker run --rm --name backend \
  --network frontend_backend_connection \
  -p 8000:8000 backend
```

### Frontend (UI)

```bash
cd git/thesis_deployment/react_frontend_ui
docker run --rm --name frontend \
  --network frontend_backend_connection \
  -p 3000:3000 frontend
```

---

## Step 5: Forward Ports of Remote to Local

*(Not useful for running on local)*

### SSH Login

```bash
ssh shashidh@dke110.cs.uni-magdeburg.de
```

### Connect App to Localhost

```bash
ssh -L 3000:localhost:3000 shashidh@dke110.cs.uni-magdeburg.de
```

---

