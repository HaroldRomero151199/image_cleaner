from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.services.image_service import _get_rembg_session, get_hardware_status

# Import routers
from app.routes.upload import router as upload_router
from app.routes.images import router as images_router
from app.routes.accept import router as accept_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize rembg session on startup with GPU priority."""
    try:
        session = _get_rembg_session()
        hardware = get_hardware_status()
        
        if hardware["using_gpu"]:
            print(f"✓ rembg initialized with GPU: {hardware['provider']}")
        else:
            print(f"✓ rembg initialized with CPU: {hardware['provider']}")
    except Exception as e:
        print(f"✗ Error initializing rembg session: {str(e)}")
        print("  Application will attempt to initialize session on first use")
    
    yield  # Application runs here
    
    # Cleanup on shutdown (if needed in the future)
    print("Shutting down...")


app = FastAPI(title="Image Service API", lifespan=lifespan)

# Mount static folder to serve images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(upload_router)
app.include_router(images_router)
app.include_router(accept_router)


# Root endpoint
@app.get("/")
def read_root():
    """Root endpoint for health check with hardware status."""
    hardware = get_hardware_status()
    return {
        "message": "Image Service is running",
        "hardware": hardware
    }