from pathlib import Path
from typing import List
from fastapi import UploadFile
import os
import uuid
from rembg import remove
from PIL import Image
import io

# Directory names
INPUT_DIR = "input"
OUTPUT_DIR = "output"


def save_original_images(ean: str, files: List[UploadFile], base_url: str) -> List[tuple]:
    """
    Save uploaded images to static/{ean}/input/ using the original filename.
    If no filename, use a UUID. Overwrites if the file already exists.
    Returns list of tuples: (local_path, url).
    """
    saved = []
    base_dir = Path("static") / ean / INPUT_DIR
    os.makedirs(base_dir, exist_ok=True)

    for file in files:
        filename = file.filename or f"{uuid.uuid4()}.png"
        file_path = base_dir / filename
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        url = f"{base_url}static/{ean}/input/{filename}"
        saved.append((str(file_path), url))
    return saved


def process_images_with_rembg(ean: str, input_paths: List[str], base_url: str) -> List[str]:
    """
    Process images with rembg and save to static/{ean}/output/ using the same filename as input.
    Returns list of processed file URLs.
    """
    output_urls = []
    output_dir = Path("static") / ean / OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    for input_path in input_paths:
        try:
            # Open image
            with open(input_path, "rb") as f:
                input_bytes = f.read()
            input_image = Image.open(io.BytesIO(input_bytes))

            # Remove background
            output_image = remove(input_image)

            # Save output image with same filename in output dir
            filename = Path(input_path).name
            output_path = output_dir / filename
            output_image.save(output_path)
            output_urls.append(f"{base_url}static/{ean}/output/{filename}")
        except Exception as e:
            # Optionally, log error or skip file
            continue
    return output_urls
