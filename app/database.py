from typing import Dict, List, Optional
from app.models.string_model import StringModel

class InMemoryDatabase:
    def __init__(self):
        # Store by value for easy lookup
        self._store: Dict[str, StringModel] = {}
    
    def create(self, string_model: StringModel) -> StringModel:
        """Create a new string entry."""
        self._store[string_model.value] = string_model
        return string_model
    
    def get_by_value(self, value: str) -> Optional[StringModel]:
        """Get string by its value."""
        return self._store.get(value)
    
    def get_by_hash(self, hash_value: str) -> Optional[StringModel]:
        """Get string by its SHA-256 hash."""
        for string_model in self._store.values():
            if string_model.id == hash_value:
                return string_model
        return None
    
    def exists(self, value: str) -> bool:
        """Check if string exists in database."""
        return value in self._store
    
    def get_all(self) -> List[StringModel]:
        """Get all strings."""
        return list(self._store.values())
    
    def delete(self, value: str) -> bool:
        """Delete string by value. Returns True if deleted, False if not found."""
        if value in self._store:
            del self._store[value]
            return True
        return False
    
    def count(self) -> int:
        """Get total count of strings."""
        return len(self._store)

# Global database instance
db = InMemoryDatabase()