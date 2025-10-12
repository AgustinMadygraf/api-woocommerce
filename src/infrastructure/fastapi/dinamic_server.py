"""
Path: src/infrastructure/fastapi/dinamic_server.py
"""

from fastapi import APIRouter, HTTPException, Query, Response

from src.shared.config import get_config
from src.shared.logger_fastapi import get_logger

from src.infrastructure.woocommerce.woocommerce_service import (
    get_system_status, WCServiceError, get_variable_products, get_product_variations
)
from src.interface_adapter.presenters.wc_system_status_presenter import WCSystemStatusPresenter
from src.entities.wc_system_status import WCSystemStatus
from src.use_cases.get_wc_variable_products import GetWCVariableProductsUseCase

router = APIRouter(prefix="", tags=["woocommerce"])
logger = get_logger("woocommerce-adapter")

logger.info("Inicializando el router de WooCommerce Adapter")


@router.get("/api/LocalStore/wc/v3/products")
def local_products(per_page: int = Query(10, ge=1, le=100), page: int = Query(1, ge=1)):
    "Endpoint local para obtener productos variables (mock)"
    productos = [
        {
            "ID_producto_variable": 1228,
            "formato": "12x08x19",
            "es_marron": True,
            "gramaje": 100,
            "stock": 54819,
            "estado": "publish",
            "ultima_actualizacion": "2025-10-12T10:00:00"
        },
        {
            "ID_producto_variable": 773,
            "formato": "16x10x24",
            "es_marron": True,
            "gramaje": 100,
            "stock": 80328,
            "estado": "publish",
            "ultima_actualizacion": "2025-10-12T10:00:00"
        }
    ]
    # Paginación simple
    start = (page - 1) * per_page
    end = start + per_page
    return productos[start:end]

@router.get("/api/LocalStore/wc/v3/products/{product_variable_id}/variations")
def local_product_variations(product_variable_id: int, per_page: int = Query(10, ge=1, le=100), page: int = Query(1, ge=1)):
    "Endpoint local para obtener variaciones de producto (mock)"
    variaciones = [
        {
            "id_produto_variaciones": 773,
            "id_producto_variable": product_variable_id,
            "es_manijas": True,
            "cantidad": 100,
            "id_impresion": 0,
            "precio_final": 123.45,
            "ultima_actualizacion": "2025-10-12T10:00:00"
        },
        {
            "id_produto_variaciones": 773,
            "id_producto_variable": product_variable_id,
            "es_manijas": True,
            "cantidad": 200,
            "id_impresion": 0,
            "precio_final": 99.99,
            "ultima_actualizacion": "2025-10-12T10:00:00"
        }
    ]
    start = (page - 1) * per_page
    end = start + per_page
    return variaciones[start:end]

@router.get("/api/LocalStore/wc/v3/system_status")
def local_system_status():
    "Endpoint local para obtener estado del sistema (mock)"
    return {"db_status": "ok", "ultima_actualizacion": "2025-10-12T10:00:00"}

@router.get("/api/wp-json/wc/v3/system_status")
def wc_system_status():
    "Endpoint para obtener el estado del sistema WooCommerce"
    try:
        cfg = get_config()
        base_url = cfg["URL"]
        ck = cfg["CK"]
        cs = cfg["CS"]
        data = get_system_status(base_url, ck, cs)
        result = WCSystemStatus.from_api_response(data)
        return WCSystemStatusPresenter.present(result)
    except WCServiceError as e:
        logger.error("WooCommerce respondió error %s: %s", e.status_code, str(e.body)[:400])
        raise HTTPException(status_code=e.status_code, detail=e.message) from e
    except Exception as e:
        logger.exception("Error inesperado en wc_system_status")
        raise HTTPException(status_code=500, detail="Error inesperado") from e


@router.get("/api/wp-json/wc/v3/products")
def wc_variable_products(product_type: str = "variable"):
    "Endpoint para obtener productos variables desde WooCommerce"
    if product_type != "variable":
        raise HTTPException(status_code=400, detail="Solo se soporta type=variable en este endpoint")
    try:
        cfg = get_config()
        base_url = cfg["URL"]
        ck = cfg["CK"]
        cs = cfg["CS"]
        # Inyección de dependencia: pasamos la función de infraestructura al caso de uso
        use_case = GetWCVariableProductsUseCase(
            lambda *a, **kw: get_variable_products(base_url, ck, cs, *a, **kw)
        )
        products = use_case.execute()
        return [prod.to_dict() for prod in products]
    except WCServiceError as e:
        logger.error("WooCommerce respondió error %s: %s", e.status_code, str(e.body)[:400])
        raise HTTPException(status_code=e.status_code, detail=e.message) from e
    except Exception as e:
        logger.exception("Error inesperado en wc_variable_products")
        raise HTTPException(status_code=500, detail="Error inesperado") from e


@router.get("/api/wp-json/wc/v3/products/{product_id}/variations")
def wc_product_variations(
    product_id: int,
    per_page: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    response: Response = None
):
    "Endpoint para obtener variaciones de un producto variable desde WooCommerce"
    try:
        cfg = get_config()
        base_url = cfg["URL"]
        ck = cfg["CK"]
        cs = cfg["CS"]
        params = {"per_page": per_page, "page": page}
        # Modifica get_product_variations para que retorne también los headers
        variations_data, headers = get_product_variations(base_url, ck, cs, product_id, params, return_headers=True)
        # Reenviar el header X-WP-Total si existe
        if response is not None and "X-WP-Total" in headers:
            response.headers["X-WP-Total"] = headers["X-WP-Total"]
        return [var for var in variations_data]
    except WCServiceError as e:
        logger.error("WooCommerce respondió error %s: %s", e.status_code, str(e.body)[:400])
        raise HTTPException(status_code=e.status_code, detail=e.message) from e
    except Exception as e:
        logger.exception("Error inesperado en wc_product_variations")
        raise HTTPException(status_code=500, detail="Error inesperado") from e
