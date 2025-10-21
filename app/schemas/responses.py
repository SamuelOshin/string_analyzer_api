from pydantic import BaseModel
from typing import Dict, List, Any
from datetime import datetime

class StringPropertiesSchema(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: Dict[str, int]

class StringResponseSchema(BaseModel):
    id: str
    value: str
    properties: StringPropertiesSchema
    created_at: str

class StringListResponseSchema(BaseModel):
    data: List[StringResponseSchema]
    count: int
    filters_applied: Dict[str, Any]

class InterpretedQuerySchema(BaseModel):
    original: str
    parsed_filters: Dict[str, Any]

class NaturalLanguageResponseSchema(BaseModel):
    data: List[StringResponseSchema]
    count: int
    interpreted_query: InterpretedQuerySchema