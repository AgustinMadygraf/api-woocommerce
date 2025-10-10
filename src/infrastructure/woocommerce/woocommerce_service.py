"""
Path: src/infrastructure/woocommerce/woocommerce_service.py
"""

from woocommerce import API

from src.shared.logger_fastapi import get_logger

logger = get_logger("woocommerce-service")

class WCServiceError(Exception):
    "Excepción para errores en el servicio WooCommerce"
    def __init__(self, status_code, message, body=None):
        self.status_code = status_code
        self.message = message
        self.body = body
        super().__init__(f"{status_code}: {message}")

def get_wc_api(base_url: str, ck: str, cs: str, version: str = "wc/v3"):
    "Inicializa y retorna la instancia de WooCommerce API"
    return API(
        url=base_url,
        consumer_key=ck,
        consumer_secret=cs,
        wp_api=True,
        version=version,
        timeout=30
    )

def get_system_status(base_url: str, ck: str, cs: str) -> dict:
    "Obtiene el estado del sistema WooCommerce usando la librería oficial"
    wcapi = get_wc_api(base_url, ck, cs)
    try:
        resp = wcapi.get("system_status")
        if resp.status_code >= 400:
            logger.error("WooCommerce respondió error %s: %s", resp.status_code, resp.text)
            raise WCServiceError(resp.status_code, "WooCommerce devolvió un error", resp.text)
        return resp.json()
    except Exception as e:
        logger.exception("Error inesperado en get_system_status")
        raise WCServiceError(500, "Error inesperado", str(e)) from e
