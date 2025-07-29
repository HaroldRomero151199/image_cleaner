from pathlib import Path
from typing import List
from fastapi import UploadFile
import os
import uuid
from rembg import remove
from PIL import Image
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    Process images with rembg and save to static/{ean}/output/ using PNG format to preserve transparency.
    Returns list of processed file URLs.
    """
    output_urls = []
    output_dir = Path("static") / ean / OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"Starting to process {len(input_paths)} images for EAN: {ean}")

    for input_path in input_paths:
        try:
            # Open image
            with open(input_path, "rb") as f:
                input_bytes = f.read()
            input_image = Image.open(io.BytesIO(input_bytes))

            # Remove background
            logger.info(f"Removing background from: {input_path}")
            output_image = remove(input_image)
            logger.info(f"Background removed successfully from: {input_path}")

            # Save output image as PNG to preserve transparency
            # Change extension to .png regardless of original format
            original_filename = Path(input_path).stem  # Get filename without extension
            output_filename = f"{original_filename}.png"
            output_path = output_dir / output_filename
            output_image.save(output_path, "PNG")
            output_urls.append(f"{base_url}static/{ean}/output/{output_filename}")
            logger.info(f"Saved processed image with transparency: {output_path}")
            
        except Exception as e:
            logger.error(f"Error processing {input_path}: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            continue
    
    logger.info(f"Processing complete. Successfully processed {len(output_urls)} out of {len(input_paths)} images")
    return output_urls
