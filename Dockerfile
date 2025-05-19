
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
