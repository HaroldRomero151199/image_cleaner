from pathlib import Path
from typing import List
from fastapi import UploadFile
import os
import uuid
from rembg import remove, new_session
from PIL import Image
import io
import logging
import threading

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Directory names
INPUT_DIR = "input"
OUTPUT_DIR = "output"

# Global session for rembg - always tries GPU first, falls back to CPU
_rembg_session = None
_session_lock = threading.Lock()


def _get_rembg_session():
    """Initialize rembg session with GPU priority (CUDA first, then CPU fallback)."""
    global _rembg_session
    
    if _rembg_session is not None:
        return _rembg_session
    
    with _session_lock:
        # Double-check inside lock to prevent race conditions
        if _rembg_session is not None:
            return _rembg_session
        
        providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
        
        try:
            logger.info("Initializing rembg session...")
            _rembg_session = new_session(model_name="u2net", providers=providers)
            
            # Check which provider is actually being used (access inner onnxruntime session)
            active_providers = _rembg_session.inner_session.get_providers()
            logger.info(f"rembg session initialized. ACTUALLY USING: {active_providers}")
            
            return _rembg_session
        except Exception as e:
            logger.error(f"FATAL: Failed to create rembg session: {str(e)}")
            raise RuntimeError(f"Cannot initialize background removal service: {str(e)}")


def get_hardware_status():
    """Get current hardware status for API response."""
    if _rembg_session is None:
        return {
            "provider": "Not initialized",
            "using_gpu": False,
            "using_cpu": False,
            "status": "Not initialized"
        }
    
    try:
        # Access the inner onnxruntime session to get active providers
        active_providers = _rembg_session.inner_session.get_providers()
        active_provider = active_providers[0] if active_providers else "Unknown"
        
        # Determine if using GPU
        is_gpu = "CUDA" in active_provider or "Dml" in active_provider or "TensorRT" in active_provider
        
        return {
            "provider": active_provider,
            "using_gpu": is_gpu,
            "using_cpu": not is_gpu,
            "status": "GPU acceleration" if is_gpu else "CPU processing"
        }
    except Exception as e:
        logger.warning(f"Could not get hardware status: {str(e)}")
        return {
            "provider": "Unknown",
            "using_gpu": False,
            "using_cpu": False,
            "status": "Unknown"
        }


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
    Always uses GPU (CUDA) if available, otherwise falls back to CPU.
    Returns list of processed file URLs.
    """
    # Get session (initializes with GPU priority if not already done)
    session = _get_rembg_session()
    
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

            # Remove background using session (GPU if available, CPU otherwise)
            logger.info(f"Removing background from: {input_path}")
            output_image = remove(input_image, session=session)
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
