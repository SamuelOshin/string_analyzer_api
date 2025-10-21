from fastapi.responses import JSONResponse
from datetime import datetime

def create_error_response(error_type: str, message: str, status_code: int, path: str, details=None):
    """
    Create a standardized error response for API endpoints.

    Args:
        error_type (str): The type of error (e.g., "BAD_REQUEST", "NOT_FOUND").
        message (str): A human-readable error message.
        status_code (int): The HTTP status code for the response.
        path (str): The request path that caused the error.
        details (dict, optional): Additional error details.

    Returns:
        JSONResponse: A FastAPI JSONResponse object with the error details.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "error": error_type,
            "message": message,
            "details": details,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "path": path
        }
    )
