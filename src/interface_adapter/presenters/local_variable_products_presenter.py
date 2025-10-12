"""
Presentador para productos variables locales
"""
from src.entities.local_variable_product import LocalVariableProduct
from typing import List, Dict

class LocalVariableProductsPresenter:
    @staticmethod
    def present(products: List[LocalVariableProduct]) -> List[Dict]:
        return [p.to_dict() for p in products]
