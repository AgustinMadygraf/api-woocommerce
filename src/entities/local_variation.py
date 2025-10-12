"""
Entidad para variación de producto local
"""
from typing import Dict

class LocalVariation:
    def __init__(self, data: Dict):
        self.data = data
        self.id = data.get("id")
        self.sku = data.get("sku")
        self.price = data.get("price")
        self.attributes = data.get("attributes", {})

    def to_dict(self):
        return self.data
