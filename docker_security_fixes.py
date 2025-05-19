import json
import os

def harden_daemon_json():
    daemon_config = {
        "log-driver": "json-file",
        "log-opts": {"max-size": "10m", "max-file": "3"},
        "no-new-privileges": True,
        "userns-remap": "default"
    }
    with open('daemon.json', 'w') as f:
        json.dump(daemon_config, f, indent=2)

def update_dockerfile():
    dockerfile_content = """
# Stage 1: Build
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .
COPY .env .

# Create non-root user
RUN useradd -m appuser
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s CMD curl --fail http://localhost:5000/ || exit 1

ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000
CMD ["python", "app.py"]
"""
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile_content)

def update_compose():
    compose_content = """
version: '3.8'
services:
  web:
    build: .
    image: mywebapp
    ports:
      - "127.0.0.1:6000:5000"
    read_only: true
    security_opt:
      - no-new-privileges:true
    mem_limit: 256m
    pids_limit: 100
    environment:
      - PASSWORD=${PASSWORD}
    volumes:
      - ./.env:/app/.env:ro
    depends_on:
      - db
    networks:
      - frontend
  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    volumes:
      - db-data:/var/lib/postgresql/data
    read_only: true
    mem_limit: 512m
    pids_limit: 100
    networks:
      - backend
networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
volumes:
  db-data:
"""
    with open('docker-compose.yml', 'w') as f:
        f.write(compose_content)

if __name__ == "__main__":
    harden_daemon_json()
    update_dockerfile()
    update_compose()
    print("Docker configuration hardened successfully.")