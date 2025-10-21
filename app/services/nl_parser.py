import re
from typing import Dict, Any

class NaturalLanguageParser:
    @staticmethod
    def parse_query(query: str) -> Dict[str, Any]:
        """Parse natural language query into structured filters."""
        query_lower = query.lower()
        filters = {}
        
        # Palindrome detection
        if 'palindrome' in query_lower or 'palindromic' in query_lower:
            filters['is_palindrome'] = True
        
        # Single word detection
        if 'single word' in query_lower or 'one word' in query_lower:
            filters['word_count'] = 1
        
        # Word count detection (exact numbers)
        word_count_match = re.search(r'(\d+)\s+words?', query_lower)
        if word_count_match and 'word_count' not in filters:
            filters['word_count'] = int(word_count_match.group(1))
        
        # Length constraints - "longer than X"
        longer_match = re.search(r'longer than (\d+)', query_lower)
        if longer_match:
            filters['min_length'] = int(longer_match.group(1)) + 1
        
        # Length constraints - "shorter than X"
        shorter_match = re.search(r'shorter than (\d+)', query_lower)
        if shorter_match:
            filters['max_length'] = int(shorter_match.group(1)) - 1
        
        # Length constraints - "at least X characters"
        at_least_match = re.search(r'at least (\d+)', query_lower)
        if at_least_match:
            filters['min_length'] = int(at_least_match.group(1))
        
        # Contains specific letter
        contains_letter_match = re.search(r'contain(?:ing|s)?\s+(?:the\s+)?(?:letter\s+)?([a-z])\b', query_lower)
        if contains_letter_match:
            filters['contains_character'] = contains_letter_match.group(1)
        
        # First vowel heuristic
        if 'first vowel' in query_lower:
            filters['contains_character'] = 'a'
        
        # Specific character patterns
        letter_z_match = re.search(r'letter ([a-z])', query_lower)
        if letter_z_match and 'contains_character' not in filters:
            filters['contains_character'] = letter_z_match.group(1)
        
        return filters
    
    @staticmethod
    def can_parse(query: str) -> bool:
        """Check if query can be parsed into valid filters."""
        try:
            filters = NaturalLanguageParser.parse_query(query)
            return len(filters) > 0
        except Exception:
            return False