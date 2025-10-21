import pytest
from app.services.analyzer import StringAnalyzer

class TestStringAnalyzer:
    
    def test_calculate_length(self):
        assert StringAnalyzer.calculate_length("hello") == 5
        assert StringAnalyzer.calculate_length("") == 0
        assert StringAnalyzer.calculate_length("hello world") == 11
    
    def test_check_palindrome(self):
        assert StringAnalyzer.check_palindrome("racecar") == True
        assert StringAnalyzer.check_palindrome("RaceCar") == True
        assert StringAnalyzer.check_palindrome("hello") == False
        assert StringAnalyzer.check_palindrome("A") == True
        assert StringAnalyzer.check_palindrome("") == True
    
    def test_count_unique_chars(self):
        assert StringAnalyzer.count_unique_chars("hello") == 4  # h, e, l, o
        assert StringAnalyzer.count_unique_chars("aaa") == 1
        assert StringAnalyzer.count_unique_chars("") == 0
        assert StringAnalyzer.count_unique_chars("abc") == 3
    
    def test_count_words(self):
        assert StringAnalyzer.count_words("hello world") == 2
        assert StringAnalyzer.count_words("hello") == 1
        assert StringAnalyzer.count_words("") == 0
        assert StringAnalyzer.count_words("one two three") == 3
        assert StringAnalyzer.count_words("  multiple   spaces  ") == 2
    
    def test_generate_sha256(self):
        hash1 = StringAnalyzer.generate_sha256("hello")
        hash2 = StringAnalyzer.generate_sha256("hello")
        hash3 = StringAnalyzer.generate_sha256("world")
        
        assert hash1 == hash2  # Same input = same hash
        assert hash1 != hash3  # Different input = different hash
        assert len(hash1) == 64  # SHA-256 produces 64 hex characters
    
    def test_build_char_frequency_map(self):
        freq_map = StringAnalyzer.build_char_frequency_map("hello")
        assert freq_map == {'h': 1, 'e': 1, 'l': 2, 'o': 1}
        
        freq_map2 = StringAnalyzer.build_char_frequency_map("aaa")
        assert freq_map2 == {'a': 3}
        
        freq_map3 = StringAnalyzer.build_char_frequency_map("")
        assert freq_map3 == {}
    
    def test_analyze_complete(self):
        result = StringAnalyzer.analyze("racecar")
        
        assert result['length'] == 7
        assert result['is_palindrome'] == True
        assert result['unique_characters'] == 4
        assert result['word_count'] == 1
        assert 'sha256_hash' in result
        assert result['character_frequency_map'] == {
            'r': 2, 'a': 2, 'c': 2, 'e': 1
        }