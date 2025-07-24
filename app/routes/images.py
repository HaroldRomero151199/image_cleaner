from fastapi import APIRouter
from app.services.file_service import list_images_by_ean
from fastapi import HTTPException, Request

router = APIRouter(
    prefix="",
    tags=["Images"]
)

@router.get("/images/{ean}")
def get_images(ean: str, request: Request):
    """
    Get lists of input and processed images for a given EAN code.
    """
    try:
        images = list_images_by_ean(ean, str(request.base_url))
        return images
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
