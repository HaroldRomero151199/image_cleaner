from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from typing import List
from services.image_service import save_original_images, process_images_with_rembg

router = APIRouter(
    prefix="",
    tags=["Upload"]
)

@router.post("/upload")
def upload_images(
    ean: str = Form(..., description="Product EAN code"),
    files: List[UploadFile] = File(..., description="List of images to upload")
):
    """
    Upload images for a given EAN code. Images are saved and processed.
    """
    if not ean or not ean.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="EAN code is required.")
    if not files or len(files) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one image is required.")

    # Save original images
    try:
        input_paths = save_original_images(ean, files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving images: {str(e)}")

    # Process images with rembg
    try:
        output_paths = process_images_with_rembg(ean, input_paths)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing images: {str(e)}")

    return {
        "input_images": input_paths,
        "processed_images": output_paths
    }
