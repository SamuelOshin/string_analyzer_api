from datetime import datetime
from typing import Dict

class StringModel:
    def __init__(self, value: str, properties: Dict, created_at: str = None):
        self.value = value
        self.properties = properties
        self.id = properties['sha256_hash']
        self.created_at = created_at or datetime.utcnow().isoformat() + "Z"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "value": self.value,
            "properties": self.properties,
            "created_at": self.created_at
        }