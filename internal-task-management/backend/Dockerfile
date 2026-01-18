# Use Python slim image
FROM python:3.11.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY app ./app

COPY frontend ./frontend 

# Expose port for FastAPI
EXPOSE 8000

# Default command (overridden in docker-compose for reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
