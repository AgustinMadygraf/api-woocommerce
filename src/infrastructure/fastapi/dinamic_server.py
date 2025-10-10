"""
Path: src/infrastructure/fastapi/dinamic_server.py
"""

from fastapi import APIRouter, HTTPException

from src.shared.config import get_config
from src.shared.logger_fastapi import get_logger

from src.infrastructure.woocommerce.woocommerce_service import (
    get_system_status, WCServiceError, get_variable_products
)
from src.interface_adapter.presenters.wc_system_status_presenter import WCSystemStatusPresenter
from src.entities.wc_system_status import WCSystemStatus
from src.use_cases.get_wc_variable_products import GetWCVariableProductsUseCase

router = APIRouter(prefix="", tags=["woocommerce"])
logger = get_logger("woocommerce-adapter")

logger.info("Inicializando el router de WooCommerce Adapter")


def _build_wc_status_url(base_url: str) -> str:
    "Construye la URL completa para el endpoint de estado del sistema WooCommerce"
    base = (base_url or "").strip()
    if not base:
        raise ValueError("URL base vacía")

    # Limpiar espacios y barras
    base = base.strip().rstrip("/")

    # Si el usuario metió 'wp-json' por error en la base, lo recortamos
    for frag in ("/wp-json", "/wp-json/"):
        if base.endswith(frag.rstrip("/")):
            base = base[: -len(frag.rstrip("/"))]
            base = base.rstrip("/")

    return f"{base}/wp-json/wc/v3/system_status"


@router.get("/api/wp-json/wc/v3/system_status")
@router.post("/api/wp-json/wc/v3/system_status")
def wc_system_status():
    "Endpoint para obtener el estado del sistema WooCommerce usando la librería oficial"
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
    "Endpoint para obtener productos variables desde WooCommerce usando la arquitectura limpia"
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
