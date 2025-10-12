"""
Entidad para el estado del sistema local
"""
from typing import Dict

class LocalSystemStatus:
    def __init__(self, data: Dict):
        self.data = data

    def __getitem__(self, key):
        return self.data.get(key)

    def to_dict(self):
        return self.data
