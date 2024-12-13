# Use an official Python runtime as the base image
FROM python:3.12.0-slim

# Install OpenGL and other required libraries
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Create the cache directory
RUN mkdir -p /root/.cache/torch/hub/checkpoints

# Copy the checkpoint into the container
COPY resnet152-f82ba261.pth /root/.cache/torch/hub/checkpoints/resnet152-f82ba261.pth

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application's port
EXPOSE 5000

# Define the command to run the application
CMD ["python", "backend.py"]
