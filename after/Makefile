# Pre-build security checks
check:
	docker run --rm -v $(shell pwd):/app python:3.9-alpine sh -c "pip install bandit && bandit -r /app"
	docker run --rm -v $(shell pwd):/app python:3.9-alpine sh -c "pip install pip-audit && pip-audit -r /app/requirements.txt"

# Host security check
host-security:
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker/docker-bench-security

# Build Docker image after security checks
dbuild: check
	docker build -t mywebapp .

# Run the container
run:
	docker run --env-file .env -p 127.0.0.1:15000:5000 mywebapp

# Scan the built image for vulnerabilities
scan:
	docker scout recommendations mywebapp:latest

# Docker Compose commands
build:
	docker compose --env-file .env build

start:
	docker compose --env-file .env up -d

stop:
	docker compose down

logs:
	docker compose logs -f

clean:
	docker system prune -f

restart: stop start
