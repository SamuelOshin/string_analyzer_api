from pydantic import BaseModel, Field, field_validator
from typing import Optional

class CreateStringRequest(BaseModel):
    value: str = Field(..., description="String to analyze")
    
    @field_validator('value')
    @classmethod
    def validate_value(cls, v):
        if not isinstance(v, str):
            raise ValueError('value must be a string')
        return v

class QueryFiltersRequest(BaseModel):
    is_palindrome: Optional[bool] = None
    min_length: Optional[int] = Field(None, ge=0)
    max_length: Optional[int] = Field(None, ge=0)
    word_count: Optional[int] = Field(None, ge=0)
    contains_character: Optional[str] = Field(None, min_length=1, max_length=1)
    
    @field_validator('min_length', 'max_length')
    @classmethod
    def validate_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('must be a non-negative integer')
        return v