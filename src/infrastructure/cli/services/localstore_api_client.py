"""
Cliente para la API de almacenamiento local (LocalStore)
"""
import requests
from typing import Dict, List, Optional, Tuple

class LocalStoreApiClient:
    "Cliente para la API LocalStore"
    def __init__(self, api_base: str):
        self.api_base = api_base

    def get_system_status(self) -> Tuple[Optional[Dict], int]:
        "Obtiene el estado del sistema local"
        try:
            resp = requests.get(f"{self.api_base.replace('/wp-json/wc/v3', '/LocalStore/wc/v3')}/system_status", timeout=10)
            return resp.json(), resp.status_code
        except requests.RequestException:
            return None, 0

    def get_variable_products(self) -> Tuple[List[Dict], int]:
        "Obtiene productos variables del almacenamiento local"
        try:
            resp = requests.get(f"{self.api_base.replace('/wp-json/wc/v3', '/LocalStore/wc/v3')}/products", timeout=10)
            return resp.json(), resp.status_code
        except requests.RequestException:
            return [], 0

    def get_product_variations(self, product_id: int, page: int = 1, per_page: int = 20) -> Tuple[List[Dict], int]:
        "Obtiene variaciones de un producto variable del almacenamiento local"
        url = f"{self.api_base.replace('/wp-json/wc/v3', '/LocalStore/wc/v3')}/products/{product_id}/variations"
        params = {"page": page, "per_page": per_page}
        try:
            resp = requests.get(url, params=params, timeout=10)
            return resp.json(), resp.status_code
        except requests.RequestException:
            return [], 0
