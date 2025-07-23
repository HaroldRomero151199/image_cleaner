from fastapi import APIRouter, Path, Body
from typing import List

router = APIRouter(
    prefix="",
    tags=["Accept"]
)

@router.post("/accept/{ean}")
def accept_images(
    ean: str = Path(..., description="Product EAN code"),
    accepted_images: List[str] = Body(..., embed=True, description="List of accepted image filenames")
):
    """
    Accept a list of images for a given EAN code, delete the rest, and notify external service.
    """
    pass
