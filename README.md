# Product Image Cleaner

A FastAPI-based web service for uploading, processing, and serving product images. It allows users to upload images, automatically removes backgrounds, and provides access to both original and processed images.

---

## Features
- Upload product images (input)
- Automatic background removal (output)
- List and download images by product EAN
- REST API endpoints
- Docker support

---

## Installation & Usage

### Requirements
- Python 3.10+
- pip
- (Optional) Docker

### 1. (Recommended) Create and activate a virtual environment
It is recommended to use a virtual environment to isolate project dependencies, but it is not strictly required:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# or
source .venv/bin/activate  # On Linux/Mac
```

### 2. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the application
```bash
uvicorn main:app --reload
```

### 4. Using Docker (optional)
```bash
docker build -t product-image-cleaner .
docker run -p 8000:8000 product-image-cleaner
```

---

## Folder Structure

- `app/` - Main application code
  - `routes/` - API endpoints
  - `services/` - Business logic
  - `utils/` - Utilities
- `static/` - Product images (input/output). **Content is git-ignored, only structure is tracked.**
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration

---

## Notes
- The `static/` folder is used to store uploaded and processed images. Its content is ignored by git, but the folder and its structure are included for clarity.
- See `static/README.md` for more info.

---
