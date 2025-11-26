# Dockerfile with GPU support
# Uses an NVIDIA base image with CUDA 12.x and cuDNN
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

# Prevent .pyc creation and keep logs unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Python 3.10 and system dependencies
# libgl1-mesa-glx is required for opencv-python (used by rembg)
RUN apt-get update && \
    apt-get install -y python3.10 python3.10-dev python3-pip libgl1-mesa-glx && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install requirements first to leverage Docker cache
COPY requirements.txt .
# ISSUE: rembg installs onnxruntime (CPU) as a dependency, breaking onnxruntime-gpu
# FIX: Install everything, then force ONLY onnxruntime-gpu
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip uninstall -y onnxruntime && \
    pip install --no-cache-dir --force-reinstall onnxruntime-gpu

# Copy the entire app code
COPY . .

# Create the static directory if missing
RUN mkdir -p /app/static

# Expose the port
EXPOSE 8000

# Command to start the application
# Runs from /app, calling the app.main module
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
