# ---------- STAGE 1: Build dependencies ----------
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /install

# Only required to build Python wheels
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install CPU-only torch FIRST (smaller, controlled)
RUN python -m pip install --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    torch==2.9.1+cpu

# Install remaining dependencies
RUN python -m pip install --no-cache-dir -r requirements.txt


# ---------- STAGE 2: Runtime image ----------
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only installed Python packages (NO build tools)
COPY --from=builder /usr/local /usr/local

# Copy backend source code
COPY backend/ .

CMD uvicorn app.main:app --host 0.0.0.0 
