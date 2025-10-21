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
    """Helper to create error responses."""
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
    """Analyze and store a new string."""
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
    """Get all strings with optional filtering."""
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
    """Filter strings using natural language query."""
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
    """Get a specific string by its value."""
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
    """Delete a string by its value."""
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