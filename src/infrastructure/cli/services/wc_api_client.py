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

    def get_product_variations(self, product_id: str, per_page: int = 50) -> Tuple[List[Dict], int, Optional[int]]:
        "Obtiene variaciones de un producto y devuelve (variaciones, código_estado, total_variaciones)"
        try:
            all_variations = []
            page = 1
            total = None

            while True:
                resp = requests.get(
                    f"{self.api_base}/products/{product_id}/variations?per_page={per_page}&page={page}",
                    timeout=20
                )

                if resp.status_code != 200:
                    return [], resp.status_code, None

                variations = resp.json()
                if not variations:
                    break

                all_variations.extend(variations)

                # Leer el total de variaciones del header
                if total is None:
                    total_str = resp.headers.get("X-WP-Total")
                    total = int(total_str) if total_str and total_str.isdigit() else None

                # Si ya tenemos todas las variaciones, salimos
                if total is not None and len(all_variations) >= total:
                    break

                page += 1

            return all_variations, 200, total

        except requests.RequestException as e:
            raise ConnectionError(f"Error de conexión: {str(e)}") from e
