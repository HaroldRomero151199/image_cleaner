from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["Images"]
)

@router.get("/images/{ean}")
def get_images(ean: str):
    """
    Get lists of input and processed images for a given EAN code.
    """
    pass
