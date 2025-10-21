import hashlib
from typing import Dict

class StringAnalyzer:
    @staticmethod
    def calculate_length(value: str) -> int:
        """Calculate the number of characters in the string."""
        return len(value)
    
    @staticmethod
    def check_palindrome(value: str) -> bool:
        """Check if string is a palindrome (case-insensitive)."""
        cleaned = value.lower()
        return cleaned == cleaned[::-1]
    
    @staticmethod
    def count_unique_chars(value: str) -> int:
        """Count the number of distinct characters."""
        return len(set(value))
    
    @staticmethod
    def count_words(value: str) -> int:
        """Count words separated by whitespace."""
        return len(value.split())
    
    @staticmethod
    def generate_sha256(value: str) -> str:
        """Generate SHA-256 hash of the string."""
        return hashlib.sha256(value.encode('utf-8')).hexdigest()
    
    @staticmethod
    def build_char_frequency_map(value: str) -> Dict[str, int]:
        """Build a frequency map of each character."""
        freq_map = {}
        for char in value:
            freq_map[char] = freq_map.get(char, 0) + 1
        return freq_map
    
    @classmethod
    def analyze(cls, value: str) -> Dict:
        """Analyze string and return all computed properties."""
        return {
            "length": cls.calculate_length(value),
            "is_palindrome": cls.check_palindrome(value),
            "unique_characters": cls.count_unique_chars(value),
            "word_count": cls.count_words(value),
            "sha256_hash": cls.generate_sha256(value),
            "character_frequency_map": cls.build_char_frequency_map(value)
        }