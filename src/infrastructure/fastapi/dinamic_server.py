"""
Path: src/infrastructure/fastapi/dinamic_server.py
"""

from fastapi import APIRouter, HTTPException, Query

from src.shared.config import get_config
from src.shared.logger_fastapi import get_logger

from src.infrastructure.httpx.httpx_service import get_wc_system_status, WCSystemStatusGatewayError
from src.interface_adapter.gateways.wc_system_status_httpx_gateway import WCSystemStatusHttpxGateway
from src.interface_adapter.controllers.wc_system_status_controller import WCSystemStatusController
from src.interface_adapter.presenters.wc_system_status_presenter import WCSystemStatusPresenter
from src.use_cases.get_wc_system_status_use_case import GetWCSystemStatusUseCase
from src.entities.wc_system_status import WCSystemStatus

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


class HttpxWCSystemStatusGateway:
    "Implementación del gateway usando httpx"
    async def get_system_status(self, wc_url: str, ck: str, cs: str, auth: str = "basic"):
        "Obtiene el estado del sistema WooCommerce usando httpx"
        resp = await get_wc_system_status(wc_url, ck, cs, auth)
        if resp.status_code >= 400:
            return resp  # Se maneja en el endpoint
        data = resp.json()
        return WCSystemStatus.from_api_response(data)


@router.get("/api/wp-json/wc/v3/system_status")
@router.post("/api/wp-json/wc/v3/system_status")
async def wc_system_status(
    auth: str = Query(
        default="basic",
        pattern="^(basic|query)$",
        description="Método de auth a WooCommerce: 'basic' (user=CK, pass=CS) o 'query' (params).",
    )
):
    "Endpoint para obtener el estado del sistema WooCommerce"
    try:
        cfg = get_config()
        wc_url = _build_wc_status_url(cfg["URL"])
        gateway = WCSystemStatusHttpxGateway(get_wc_system_status)
        use_case = GetWCSystemStatusUseCase(gateway, wc_url, cfg["CK"], cfg["CS"])
        controller = WCSystemStatusController(use_case)
        result = await controller.get_status(auth)

        # Usar el presenter para la respuesta
        return WCSystemStatusPresenter.present(result)

    except WCSystemStatusGatewayError as e:
        logger.error("WooCommerce respondió error %s: %s", e.status_code, str(e.body)[:400])
        raise HTTPException(
            status_code=e.status_code,
            detail={
                "message": e.message,
                "status_code": e.status_code,
                "target": wc_url,
                "body": e.body,
            },
        ) from e
    except Exception as e:  # pylint: disable=broad-except
        logger.exception("Error inesperado en wc_system_status")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error inesperado", "error": str(e)},
        ) from e
