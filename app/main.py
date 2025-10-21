from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime

from app.config import settings
from app.routers import strings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

# Include routers
app.include_router(strings.router)

# Global exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Request validation failed",
            "details": exc.errors(),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "path": str(request.url.path)
        }
    )

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "String Analysis API",
        "version": settings.app_version,
        "endpoints": {
            "create": "POST /strings",
            "get_one": "GET /strings/{string_value}",
            "get_all": "GET /strings",
            "filter_nl": "GET /strings/filter-by-natural-language",
            "delete": "DELETE /strings/{string_value}"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }