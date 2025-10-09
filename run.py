"""
Path: run.py
Arranque del servicio con chequeos y logger
"""

import os
import sys
import uvicorn
from src.shared.config import get_config
from src.shared.logger import get_logger

log = get_logger("datamaq-run")

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
        reload="true"
    )

if __name__ == "__main__":
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
