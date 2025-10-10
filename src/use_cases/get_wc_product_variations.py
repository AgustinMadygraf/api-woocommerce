"""
Caso de uso para obtener variaciones de un producto variable en WooCommerce.
"""

from typing import List, Callable
from src.entities.wc_product_variation import WCProductVariation

class GetWCProductVariationsUseCase:
    "Caso de uso para obtener variaciones de un producto variable de WooCommerce"
    def __init__(self, fetch_variations_func: Callable[..., list]):
        "fetch_variations_func: función que retorna una lista de variaciones desde la infraestructura."
        self._fetch_variations_func = fetch_variations_func

    def execute(self, product_id: int, *args, **kwargs) -> List[WCProductVariation]:
        "Ejecuta el caso de uso y retorna una lista de variaciones para el producto dado"
        variations_data = self._fetch_variations_func(product_id, *args, **kwargs)
        return [WCProductVariation.from_api_response(var) for var in variations_data]
