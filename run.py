"""
Path: run.py
Arranque del servicio con chequeos y logger
"""

import os
import sys
import uvicorn
from src.shared.config import get_config, require_config
from src.shared.logger import get_logger

log = get_logger("datamaq-run")

def _preflight():
    config = get_config()

    try:
        require_config(["URL", "CK", "CS"])
    except RuntimeError as e:
        log.error(str(e))
        sys.exit(1)

    # Chequeo de assets front (mismo comportamiento que antes, opcional)
    static_path = os.getenv("STATIC_PATH") or config.get("STATIC_PATH")
    if static_path and not os.path.isdir(static_path):
        log.warning("STATIC_PATH no existe: %s (solo aviso)", static_path)

def run_fastapi():
    """Inicia el servidor FastAPI"""
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "5000"))
    log.info("Iniciando DataMaq Gateway en http://%s:%s", host, port)
    # Levanta la app definida en static_server.py
    uvicorn.run(
        "src.infrastructure.fastapi.static_server:app",
        host=host,
        port=port,
        reload=os.getenv("UVICORN_RELOAD", "true").lower() == "true"
    )

if __name__ == "__main__":
    _preflight()
    cfg = get_config()
    mode = cfg.get("MODE", "FASTAPI").upper()

    if mode == "FASTAPI":
        run_fastapi()
    elif mode == "CLI":
        from src.infrastructure.cli.cli_app import run_cli
        run_cli()
    else:
        log.error("Modo no reconocido: %s. Use FASTAPI o CLI", mode)
        sys.exit(1)
