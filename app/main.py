from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Import routers
from app.routes.upload import router as upload_router
from app.routes.images import router as images_router
from app.routes.accept import router as accept_router

app = FastAPI(title="Image Service API")

# Mount static folder to serve images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(upload_router)
app.include_router(images_router)
app.include_router(accept_router)

# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint for health check."""
    return {"message": "Image Service is running"}
