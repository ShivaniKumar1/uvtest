# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv==0.7.10

# Copy project files
COPY . .

# Install dependencies with uv
RUN uv sync --frozen

# Expose port
EXPOSE 8080

# Set environment variable
ENV PORT=8080

# Run the application
CMD ["uv", "run", "server.py"]
