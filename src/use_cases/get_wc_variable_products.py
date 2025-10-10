"""
Path: src/use_cases/get_wc_variable_products.py
"""

from typing import List, Callable
from src.entities.wc_variable_product import WCVariableProduct

class GetWCVariableProductsUseCase:
    "Caso de uso para obtener productos variables de WooCommerce"
    def __init__(self, fetch_products_func: Callable[..., list]):
        "Inyecta la función que obtiene los productos variables"
        self._fetch_products_func = fetch_products_func

    def execute(self, *args, **kwargs) -> List[WCVariableProduct]:
        "Ejecuta el caso de uso y retorna una lista de productos variables"
        products_data = self._fetch_products_func(*args, **kwargs)
        return [WCVariableProduct.from_api_response(prod) for prod in products_data]
