# Product Image Cleaner

FastAPI web service to upload product images and remove the background automatically using rembg.

## Features

- Upload product images
- Remove the background automatically
- REST API to list and download images
- GPU support for faster processing

## Installation and Usage (Docker)

This project is meant to run with Docker. By default, it tries to use the GPU for optimal processing speed.

### Prerequisites

1.  **Docker** and **Docker Compose** installed.
2.  **(GPU mode only)**: NVIDIA drivers plus the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) installed on the host.

### How to run

1.  **Build and start the service:**
    ```bash
    docker-compose up --build
    ```

2.  **Check everything is working:**
    - API docs: http://localhost:8000/docs
    - Hardware status: http://localhost:8000/ (should report `"using_gpu": true` when the GPU is active)

### No GPU available? (CPU mode)

The `docker-compose.yml` file is configured to **require** an NVIDIA GPU. Without a GPU or the NVIDIA Container Toolkit, the container will not start.

To run on **CPU only**, edit `docker-compose.yml` and **comment or delete** the `deploy` section:

```yaml
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: all
    #           capabilities: [gpu]
```

## API usage

1.  Use the `/upload/{ean}` endpoint to upload images.
2.  Processed images will be stored in `/static/{ean}/output/`.

## Project structure

- `app/` - Application code
- `static/` - Uploaded and processed images
- `Dockerfile` - Docker image definition (CUDA 12.x ready)
- `docker-compose.yml` - Service configuration
