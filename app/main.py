from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import get_settings
from app.database import Base, engine
from app.api.routes import product, category, customer, auth

settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Customer Order Services - Python FastAPI implementation of the JEE reference architecture",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    redirect_slashes=False,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(product.router, prefix=settings.api_prefix)
app.include_router(category.router, prefix=settings.api_prefix)
app.include_router(customer.router, prefix=settings.api_prefix)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    # Create tables if they don't exist (for development)
    # In production, use Alembic migrations
    if settings.debug:
        Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs": "/api/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for container orchestration."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
