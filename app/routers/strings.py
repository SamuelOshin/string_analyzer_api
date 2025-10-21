from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime
from urllib.parse import unquote

from app.schemas.requests import CreateStringRequest
from app.schemas.responses import (
    StringResponseSchema, 
    StringListResponseSchema,
    NaturalLanguageResponseSchema,
    InterpretedQuerySchema
)
from app.services.analyzer import StringAnalyzer
from app.services.filters import FilterService
from app.services.nl_parser import NaturalLanguageParser
from app.models.string_model import StringModel
from app.database import db

router = APIRouter(prefix="/strings", tags=["strings"])

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

@router.post("", status_code=201, response_model=StringResponseSchema)
async def create_string(request: Request, body: CreateStringRequest):
    """
    Analyze and store a new string.

    This endpoint accepts a string value, analyzes its properties (length, palindrome status,
    unique characters, word count, SHA-256 hash, and character frequency), and stores it
    in the database if it doesn't already exist.

    Args:
        request (Request): The incoming HTTP request object.
        body (CreateStringRequest): The request body containing the string to analyze.

    Returns:
        dict: A dictionary representation of the created StringModel.

    Raises:
        HTTPException: Returns 409 if the string already exists, 400 if the value is empty,
                       or 422 if the data type is invalid.
    """
    try:
        # Check if string already exists
        if db.exists(body.value):
            existing = db.get_by_value(body.value)
            return create_error_response(
                error_type="CONFLICT",
                message="String already exists in the system",
                status_code=409,
                path=str(request.url.path),
                details={
                    "existing_id": existing.id,
                    "value": body.value,
                    "created_at": existing.created_at
                }
            )
        
        # Check for empty value
        if not body.value:
            return create_error_response(
                error_type="BAD_REQUEST",
                message="Invalid request body or missing 'value' field",
                status_code=400,
                path=str(request.url.path),
                details={
                    "field": "value",
                    "error": "value cannot be empty"
                }
            )
        
        # Analyze the string
        properties = StringAnalyzer.analyze(body.value)
        
        # Create and store the model
        string_model = StringModel(value=body.value, properties=properties)
        db.create(string_model)
        
        return string_model.to_dict()
    
    except ValueError as e:
        return create_error_response(
            error_type="UNPROCESSABLE_ENTITY",
            message="Invalid data type for 'value' field",
            status_code=422,
            path=str(request.url.path),
            details={
                "field": "value",
                "error": str(e)
            }
        )

@router.get("", response_model=StringListResponseSchema)
async def get_all_strings(
    request: Request,
    is_palindrome: Optional[bool] = Query(None),
    min_length: Optional[int] = Query(None, ge=0),
    max_length: Optional[int] = Query(None, ge=0),
    word_count: Optional[int] = Query(None, ge=0),
    contains_character: Optional[str] = Query(None, min_length=1, max_length=1)
):
    """
    Retrieve all stored strings with optional filtering.

    This endpoint allows querying the database of analyzed strings with various filters
    such as palindrome status, length constraints, word count, and character presence.

    Args:
        request (Request): The incoming HTTP request object.
        is_palindrome (Optional[bool]): Filter for palindrome strings if True.
        min_length (Optional[int]): Minimum string length (inclusive).
        max_length (Optional[int]): Maximum string length (inclusive).
        word_count (Optional[int]): Exact number of words in the string.
        contains_character (Optional[str]): Single character that must be present in the string.

    Returns:
        dict: A dictionary containing the filtered list of strings, count, and applied filters.

    Raises:
        HTTPException: Returns 400 if filter combinations are invalid.
    """
    # Build filters dictionary
    filters = {}
    if is_palindrome is not None:
        filters['is_palindrome'] = is_palindrome
    if min_length is not None:
        filters['min_length'] = min_length
    if max_length is not None:
        filters['max_length'] = max_length
    if word_count is not None:
        filters['word_count'] = word_count
    if contains_character is not None:
        filters['contains_character'] = contains_character
    
    # Validate filter conflicts
    is_valid, error_msg = FilterService.validate_filter_conflicts(filters)
    if not is_valid:
        return create_error_response(
            error_type="BAD_REQUEST",
            message="Invalid filter combination",
            status_code=400,
            path=str(request.url.path),
            details={"conflict": error_msg, "filters": filters}
        )
    
    # Get all strings and apply filters
    all_strings = db.get_all()
    filtered_strings = FilterService.apply_filters(all_strings, filters)
    
    return {
        "data": [s.to_dict() for s in filtered_strings],
        "count": len(filtered_strings),
        "filters_applied": filters
    }

@router.get("/filter-by-natural-language", response_model=NaturalLanguageResponseSchema)
async def filter_by_natural_language(
    request: Request,
    query: str = Query(..., min_length=1)
):
    """
    Filter strings using a natural language query.

    This endpoint allows users to query the string database using human-readable language
    instead of technical filters. The query is parsed and converted to appropriate filters.

    Args:
        request (Request): The incoming HTTP request object.
        query (str): A natural language query describing the desired string properties.

    Returns:
        dict: A dictionary containing the filtered list of strings, count, original query,
              and parsed filters.

    Raises:
        HTTPException: Returns 400 if the query cannot be parsed, or 422 if parsed filters conflict.
    """
    # Parse the natural language query
    if not NaturalLanguageParser.can_parse(query):
        return create_error_response(
            error_type="BAD_REQUEST",
            message="Unable to parse natural language query",
            status_code=400,
            path=str(request.url.path),
            details={"query": query}
        )
    
    parsed_filters = NaturalLanguageParser.parse_query(query)
    
    # Validate filter conflicts
    is_valid, error_msg = FilterService.validate_filter_conflicts(parsed_filters)
    if not is_valid:
        return create_error_response(
            error_type="UNPROCESSABLE_ENTITY",
            message="Query parsed but resulted in conflicting filters",
            status_code=422,
            path=str(request.url.path),
            details={
                "conflict": error_msg,
                "filters": parsed_filters
            }
        )
    
    # Apply filters
    all_strings = db.get_all()
    filtered_strings = FilterService.apply_filters(all_strings, parsed_filters)
    
    return {
        "data": [s.to_dict() for s in filtered_strings],
        "count": len(filtered_strings),
        "interpreted_query": {
            "original": query,
            "parsed_filters": parsed_filters
        }
    }

@router.get("/{string_value}", response_model=StringResponseSchema)
async def get_string(request: Request, string_value: str):
    """
    Retrieve a specific string by its value.

    This endpoint fetches a single string from the database based on its exact value.
    The string value is URL-decoded to handle special characters.

    Args:
        request (Request): The incoming HTTP request object.
        string_value (str): The exact string value to retrieve (URL-encoded if necessary).

    Returns:
        dict: A dictionary representation of the StringModel if found.

    Raises:
        HTTPException: Returns 404 if the string does not exist in the system.
    """
    # Decode URL-encoded string
    decoded_value = unquote(string_value)
    
    string_model = db.get_by_value(decoded_value)
    
    if not string_model:
        return create_error_response(
            error_type="NOT_FOUND",
            message="String does not exist in the system",
            status_code=404,
            path=str(request.url.path),
            details={"requested_value": decoded_value}
        )
    
    return string_model.to_dict()

@router.delete("/{string_value}", status_code=204)
async def delete_string(request: Request, string_value: str):
    """
    Delete a string by its value.

    This endpoint removes a string from the database based on its exact value.
    The string value is URL-decoded to handle special characters.

    Args:
        request (Request): The incoming HTTP request object.
        string_value (str): The exact string value to delete (URL-encoded if necessary).

    Returns:
        JSONResponse: A 204 No Content response on successful deletion.

    Raises:
        HTTPException: Returns 404 if the string does not exist in the system.
    """
    # Decode URL-encoded string
    decoded_value = unquote(string_value)
    
    deleted = db.delete(decoded_value)
    
    if not deleted:
        return create_error_response(
            error_type="NOT_FOUND",
            message="String does not exist in the system",
            status_code=404,
            path=str(request.url.path),
            details={"requested_value": decoded_value}
        )
    
    return JSONResponse(status_code=204, content=None)