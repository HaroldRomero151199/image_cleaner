from fastapi import APIRouter
from app.services.image_service import save_original_images

router = APIRouter(prefix="/accept", tags=["accept"])

@router.get("/")
def accept():
    return {"message": "Accept endpoint"}
