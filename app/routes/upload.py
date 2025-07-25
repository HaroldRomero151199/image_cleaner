from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from typing import List
from app.services.image_service import save_original_images, process_images_with_rembg
from app.utils.helpers import extract_local_paths, extract_urls

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/{ean}")
async def upload_images(ean: str, request: Request, files: List[UploadFile] = File(...),):
    """
    Upload images for a given EAN. Saves originals and processes with rembg.
    """
    try:
        base_url = str(request.base_url)
        saved = save_original_images(ean, files, base_url)
        local_paths = extract_local_paths(saved)
        originals_urls = extract_urls(saved)
        processed_urls = process_images_with_rembg(ean, local_paths, base_url)
        return {
            "originals": originals_urls,
            "processed": processed_urls
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
