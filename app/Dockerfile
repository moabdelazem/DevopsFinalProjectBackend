# Stage 1: Builder Stage
FROM python:3.10-slim AS builder

WORKDIR /app

# Update package list
RUN apt-get update

# Install build dependencies
RUN apt-get install -y build-essential

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt

# Copy the application code
COPY . .

# Stage 2: Final Stage
FROM python:3.10-slim

WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /app /app
COPY --from=builder /app/deps /usr/local/lib/python3.10/site-packages

# Expose port 8000
EXPOSE 8000

# Command to run the FastAPI server using uvicorn
CMD ["python", "app.py"]

