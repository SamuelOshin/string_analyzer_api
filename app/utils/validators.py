from typing import Any, Dict, Optional, Tuple

class RequestValidator:
    """Utility class for validating request data."""
    
    @staticmethod
    def validate_string_value(value: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate that the value is a string.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(value, str):
            return False, f"value must be a string, received {type(value).__name__}"
        return True, None
    
    @staticmethod
    def validate_non_empty_string(value: str) -> Tuple[bool, Optional[str]]:
        """
        Validate that the string is not empty.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not value or len(value) == 0:
            return False, "value cannot be empty"
        return True, None
    
    @staticmethod
    def validate_query_params(params: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate query parameters for filtering.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate is_palindrome
        if 'is_palindrome' in params and params['is_palindrome'] is not None:
            if not isinstance(params['is_palindrome'], bool):
                return False, "is_palindrome must be a boolean"
        
        # Validate min_length
        if 'min_length' in params and params['min_length'] is not None:
            if not isinstance(params['min_length'], int) or params['min_length'] < 0:
                return False, "min_length must be a non-negative integer"
        
        # Validate max_length
        if 'max_length' in params and params['max_length'] is not None:
            if not isinstance(params['max_length'], int) or params['max_length'] < 0:
                return False, "max_length must be a non-negative integer"
        
        # Validate word_count
        if 'word_count' in params and params['word_count'] is not None:
            if not isinstance(params['word_count'], int) or params['word_count'] < 0:
                return False, "word_count must be a non-negative integer"
        
        # Validate contains_character
        if 'contains_character' in params and params['contains_character'] is not None:
            char = params['contains_character']
            if not isinstance(char, str):
                return False, "contains_character must be a string"
            if len(char) != 1:
                return False, "contains_character must be exactly one character"
        
        return True, None
    
    @staticmethod
    def validate_natural_language_query(query: str) -> Tuple[bool, Optional[str]]:
        """
        Validate natural language query.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not query or not query.strip():
            return False, "query cannot be empty"
        
        if len(query) > 500:
            return False, "query is too long (max 500 characters)"
        
        return True, None
    
    @staticmethod
    def sanitize_string_for_url(value: str) -> str:
        """
        Sanitize string for use in URL path.
        
        Args:
            value: String to sanitize
            
        Returns:
            URL-safe string
        """
        from urllib.parse import quote
        return quote(value, safe='')


class FilterValidator:
    """Utility class for validating filter combinations."""
    
    @staticmethod
    def check_length_conflict(min_length: Optional[int], max_length: Optional[int]) -> Tuple[bool, Optional[str]]:
        """
        Check if min_length and max_length create a conflict.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if min_length is not None and max_length is not None:
            if min_length > max_length:
                return False, f"min_length ({min_length}) is greater than max_length ({max_length})"
        return True, None
    
    @staticmethod
    def validate_filter_combination(filters: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate that filter combination is valid.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check length conflict
        min_len = filters.get('min_length')
        max_len = filters.get('max_length')
        
        is_valid, error = FilterValidator.check_length_conflict(min_len, max_len)
        if not is_valid:
            return False, error
        
        # Add more validation rules here as needed
        
        return True, None


class StringValidator:
    """Utility class for validating string properties."""
    
    @staticmethod
    def is_valid_length(value: str, min_length: Optional[int] = None, max_length: Optional[int] = None) -> bool:
        """Check if string length is within specified bounds."""
        length = len(value)
        
        if min_length is not None and length < min_length:
            return False
        
        if max_length is not None and length > max_length:
            return False
        
        return True
    
    @staticmethod
    def contains_character(value: str, character: str) -> bool:
        """Check if string contains a specific character."""
        return character in value
    
    @staticmethod
    def matches_word_count(value: str, word_count: int) -> bool:
        """Check if string has exact word count."""
        return len(value.split()) == word_count
    
    @staticmethod
    def is_palindrome(value: str) -> bool:
        """Check if string is a palindrome (case-insensitive)."""
        cleaned = value.lower()
        return cleaned == cleaned[::-1]


class ErrorMessageBuilder:
    """Utility class for building consistent error messages."""
    
    @staticmethod
    def build_validation_error(field: str, expected_type: str, received_type: str, received_value: Any = None) -> Dict[str, Any]:
        """Build validation error details."""
        details = {
            "field": field,
            "expected_type": expected_type,
            "received_type": received_type
        }
        
        if received_value is not None:
            details["received_value"] = received_value
        
        return details
    
    @staticmethod
    def build_conflict_error(existing_id: str, value: str, created_at: str) -> Dict[str, Any]:
        """Build conflict error details."""
        return {
            "existing_id": existing_id,
            "value": value,
            "created_at": created_at
        }
    
    @staticmethod
    def build_not_found_error(requested_value: str) -> Dict[str, Any]:
        """Build not found error details."""
        return {
            "requested_value": requested_value
        }
    
    @staticmethod
    def build_filter_conflict_error(conflict: str, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Build filter conflict error details."""
        return {
            "conflict": conflict,
            "filters": filters
        }