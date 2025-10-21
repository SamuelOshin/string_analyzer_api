from typing import List, Dict, Any
from app.models.string_model import StringModel

class FilterService:
    @staticmethod
    def apply_filters(strings: List[StringModel], filters: Dict[str, Any]) -> List[StringModel]:
        """Apply filters to list of strings."""
        result = strings
        
        # Filter by palindrome
        if filters.get('is_palindrome') is not None:
            result = [s for s in result if s.properties['is_palindrome'] == filters['is_palindrome']]
        
        # Filter by min_length
        if filters.get('min_length') is not None:
            result = [s for s in result if s.properties['length'] >= filters['min_length']]
        
        # Filter by max_length
        if filters.get('max_length') is not None:
            result = [s for s in result if s.properties['length'] <= filters['max_length']]
        
        # Filter by word_count
        if filters.get('word_count') is not None:
            result = [s for s in result if s.properties['word_count'] == filters['word_count']]
        
        # Filter by contains_character
        if filters.get('contains_character') is not None:
            char = filters['contains_character']
            result = [s for s in result if char in s.value]
        
        return result
    
    @staticmethod
    def validate_filter_conflicts(filters: Dict[str, Any]) -> tuple[bool, str]:
        """Check for conflicting filters. Returns (is_valid, error_message)."""
        min_len = filters.get('min_length')
        max_len = filters.get('max_length')
        
        if min_len is not None and max_len is not None:
            if min_len > max_len:
                return False, f"min_length ({min_len}) is greater than max_length ({max_len})"
        
        return True, ""