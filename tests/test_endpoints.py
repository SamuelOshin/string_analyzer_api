import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_database():
    """Clear database before each test"""
    db._store.clear()
    yield
    db._store.clear()

class TestCreateString:
    
    def test_create_string_success(self):
        response = client.post(
            "/strings",
            json={"value": "hello world"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data['value'] == "hello world"
        assert data['properties']['length'] == 11
        assert data['properties']['word_count'] == 2
        assert 'sha256_hash' in data['properties']
    
    def test_create_duplicate_string(self):
        # Create first time
        client.post("/strings", json={"value": "test"})
        
        # Try to create again
        response = client.post("/strings", json={"value": "test"})
        
        assert response.status_code == 409
        data = response.json()
        assert data['error'] == "CONFLICT"
    
    def test_create_palindrome(self):
        response = client.post("/strings", json={"value": "racecar"})
        
        assert response.status_code == 201
        data = response.json()
        assert data['properties']['is_palindrome'] == True

class TestGetString:
    
    def test_get_existing_string(self):
        # Create string first
        client.post("/strings", json={"value": "test string"})
        
        # Get it
        response = client.get("/strings/test%20string")
        
        assert response.status_code == 200
        data = response.json()
        assert data['value'] == "test string"
    
    def test_get_nonexistent_string(self):
        response = client.get("/strings/nonexistent")
        
        assert response.status_code == 404
        data = response.json()
        assert data['error'] == "NOT_FOUND"

class TestGetAllStrings:
    
    def test_get_all_no_filters(self):
        # Create some strings
        client.post("/strings", json={"value": "hello"})
        client.post("/strings", json={"value": "world"})
        
        response = client.get("/strings")
        
        assert response.status_code == 200
        data = response.json()
        assert data['count'] == 2
        assert len(data['data']) == 2
    
    def test_filter_by_palindrome(self):
        client.post("/strings", json={"value": "racecar"})
        client.post("/strings", json={"value": "hello"})
        client.post("/strings", json={"value": "level"})
        
        response = client.get("/strings?is_palindrome=true")
        
        assert response.status_code == 200
        data = response.json()
        assert data['count'] == 2
        assert data['filters_applied']['is_palindrome'] == True
    
    def test_filter_by_length(self):
        client.post("/strings", json={"value": "hi"})
        client.post("/strings", json={"value": "hello"})
        client.post("/strings", json={"value": "world"})
        
        response = client.get("/strings?min_length=5")
        
        assert response.status_code == 200
        data = response.json()
        assert data['count'] == 2

class TestNaturalLanguage:
    
    def test_nl_single_word_palindrome(self):
        client.post("/strings", json={"value": "racecar"})
        client.post("/strings", json={"value": "hello world"})
        
        response = client.get(
            "/strings/filter-by-natural-language?query=single%20word%20palindromic%20strings"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data['count'] == 1
        assert data['interpreted_query']['parsed_filters']['word_count'] == 1
        assert data['interpreted_query']['parsed_filters']['is_palindrome'] == True

class TestDeleteString:
    
    def test_delete_existing_string(self):
        client.post("/strings", json={"value": "delete me"})
        
        response = client.delete("/strings/delete%20me")
        
        assert response.status_code == 204
    
    def test_delete_nonexistent_string(self):
        response = client.delete("/strings/nonexistent")
        
        assert response.status_code == 404
        data = response.json()
        assert data['error'] == "NOT_FOUND"