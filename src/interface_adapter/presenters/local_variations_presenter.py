"""
Presentador para variaciones de producto local
"""
from src.entities.local_variation import LocalVariation
from typing import List, Dict

class LocalVariationsPresenter:
    @staticmethod
    def present(variations: List[LocalVariation]) -> List[Dict]:
        return [v.to_dict() for v in variations]
