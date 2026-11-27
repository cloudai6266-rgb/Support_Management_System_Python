FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Show Python logs immediately
ENV PYTHONUNBUFFERED=1

# Copy dependency file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY . .

# Render provides the PORT environment variable
EXPOSE 8000

# Start FastAPI
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]