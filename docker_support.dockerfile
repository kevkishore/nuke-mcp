# Optional Dockerfile for containerized deployment
# This is useful for studio environments or cloud deployments

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package
RUN pip install -e .

# Expose the MCP server port
EXPOSE 9876

# Environment variables
ENV PYTHONPATH=/app
ENV NUKE_MCP_ROOT=/app

# Run the MCP server
CMD ["python", "enhanced_nuke_mcp_server.py"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.connect(('localhost', 9876)); s.close()" || exit 1