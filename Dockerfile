# Stage 1: builder 
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies in isolation so they can be copied cleanly
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


# runtime 
FROM python:3.11-slim AS runtime

# Security: run as non-root user
RUN addgroup --system shopeasy && \
    adduser  --system --ingroup shopeasy shopeasy

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY shopeasy_bot/ ./shopeasy_bot/
COPY templates/    ./templates/
COPY app.py        .

# Ownership
RUN chown -R shopeasy:shopeasy /app

USER shopeasy

# Expose FastAPI port
EXPOSE 8000

# Health check — Docker will restart the container if the app becomes unhealthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Start the server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
