"""
Entidad para producto variable local
"""
from typing import Dict

class LocalVariableProduct:
    def __init__(self, data: Dict):
        self.data = data
        self.id = data.get("id")
        self.name = data.get("name")
        self.sku = data.get("sku")
        self.price = data.get("price")
        self.variations = data.get("variations", [])

    def to_dict(self):
        return self.data
