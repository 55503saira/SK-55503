# Base image: the same one we pre-pulled (docker pull python:3.11-slim)
FROM python:3.11-slim

# Print Python output immediately so `docker logs` shows it
ENV PYTHONUNBUFFERED=1

# All following instructions run inside /app in the image
WORKDIR /app

# Copy requirements first -> Docker caches the pip layer unless this file changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Documentation only: the app listens on 5000 inside the container
EXPOSE 5000

# Default command when the container starts
CMD ["python", "app.py"]