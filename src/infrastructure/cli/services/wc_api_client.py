"""
Path: src/infrastructure/cli/services/wc_api_client.py
"""

from typing import Dict, List, Optional, Tuple
import requests

class WCApiClient:
    "Cliente para la API de WooCommerce"
    def __init__(self, api_base: str):
        self.api_base = api_base

    def get_variable_products(self) -> Tuple[List[Dict], int]:
        "Obtiene productos variables y devuelve (productos, código_estado)"
        try:
            resp = requests.get(f"{self.api_base}/products?product_type=variable", timeout=10)
            return resp.json(), resp.status_code
        except requests.RequestException as e:
            raise ConnectionError(f"Error de conexión: {str(e)}") from e

    def get_product_variation_count(self, product_id: int) -> Optional[str]:
        "Obtiene el número total de variaciones de un producto"
        try:
            resp = requests.get(
                f"{self.api_base}/products/{product_id}/variations?per_page=1",
                timeout=10
            )
            if resp.status_code == 200:
                return resp.headers.get("X-WP-Total", "?")
            return "?"
        except requests.RequestException:
            return "?"

    def get_product_variations(self, product_id, page=1, per_page=20):
        "Obtiene variaciones de un producto y devuelve (variaciones, código_estado, total_variaciones)"
        url = f"{self.api_base}/products/{product_id}/variations"
        params = {"page": page, "per_page": per_page}
        try:
            response = requests.get(url, params=params, timeout=10)
            status_code = response.status_code
            variations = response.json() if status_code == 200 else []
            total = int(response.headers.get("X-WP-Total", len(variations)))
            return variations, status_code, total
        except requests.RequestException as e:
            raise ConnectionError(f"Error de conexión: {str(e)}") from e
