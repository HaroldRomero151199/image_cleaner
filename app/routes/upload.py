from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.services.image_service import save_original_images, process_images_with_rembg

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/{ean}")
async def upload_images(ean: str, files: List[UploadFile] = File(...)):
    """
    Upload images for a given EAN. Saves originals and processes with rembg.
    """
    try:
        saved_paths = save_original_images(ean, files)
        processed_paths = process_images_with_rembg(ean, saved_paths)
        return {
            "originals": saved_paths,
            "processed": processed_paths
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
