from pathlib import Path
from typing import List
from fastapi import UploadFile
import os
import uuid

# Directory names
INPUT_DIR = "input"
OUTPUT_DIR = "output"


def save_original_images(ean: str, files: List[UploadFile]) -> List[str]:
    """
    Save uploaded images to static/{ean}/input/ using the original filename.
    If no filename, use a UUID. Overwrites if the file already exists.
    Returns list of saved file paths.
    """
    saved_paths = []
    base_dir = Path("static") / ean / INPUT_DIR
    os.makedirs(base_dir, exist_ok=True)

    for file in files:
        filename = file.filename or f"{uuid.uuid4()}.png"
        file_path = base_dir / filename
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        saved_paths.append(str(file_path))
    return saved_paths


def process_images_with_rembg(ean: str, input_paths: List[str]) -> List[str]:
    """
    Process images with rembg and save to static/{ean}/output/ using the same filename as input.
    Returns list of processed file paths.
    """
    # TODO: Implement rembg logic
    pass
