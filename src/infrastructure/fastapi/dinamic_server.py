"""
Path: src/infrastructure/fastapi/dinamic_server.py
"""

from fastapi import APIRouter, HTTPException, Query

from src.shared.config import require_config
from src.shared.logger import get_logger

from src.infrastructure.httpx.httpx_service import get_wc_system_status

router = APIRouter(prefix="", tags=["woocommerce"])
logger = get_logger("woocommerce-adapter")

logger.info("Inicializando el router de WooCommerce Adapter")


def _build_wc_status_url(base_url: str) -> str:
    """
    Normaliza la base (con/sin slash final) y construye el endpoint completo.
    Evita duplicar 'wp-json' si el usuario pegó algo raro en URL.
    """
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
async def wc_system_status(
    auth: str = Query(
        default="basic",
        pattern="^(basic|query)$",
        description="Método de auth a WooCommerce: 'basic' (user=CK, pass=CS) o 'query' (params).",
    )
):
    " Consulta el estado del sistema WooCommerce y lo devuelve como JSON"
    try:
        cfg = require_config(["URL", "CK", "CS"])
        wc_url = _build_wc_status_url(cfg["URL"])

        resp = await get_wc_system_status(wc_url, cfg["CK"], cfg["CS"], auth)

        if resp.status_code >= 400:
            logger.error("WooCommerce respondió error %s: %s", resp.status_code, resp.text[:400])
            raise HTTPException(
                status_code=resp.status_code,
                detail={
                    "message": "WooCommerce devolvió un error",
                    "status_code": resp.status_code,
                    "target": wc_url,
                    "body": resp.text,
                },
            )

        data = resp.json()
        return data

    except Exception as e:  # pylint: disable=broad-except
        logger.exception("Error inesperado en wc_system_status")
        raise HTTPException(
            status_code=500,
            detail={"message": "Error inesperado", "error": str(e)},
        ) from e
