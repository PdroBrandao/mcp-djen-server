FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY openapi.yaml .
COPY start_server.py .

# Create logs directory
RUN mkdir -p logs

# Make startup script executable
RUN chmod +x start_server.py

# Expose port
EXPOSE 8000

# Run the application with startup script
CMD ["python", "start_server.py"] 