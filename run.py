"""
Path: run.py
Arranque del servicio con chequeos y logger
"""

import uvicorn
from src.shared.logger_fastapi import get_logger

log = get_logger("datamaq-run")

if __name__ == "__main__":
    log.info("Iniciando DataMaq Gateway")
    # Levanta la app definida en static_server.py
    uvicorn.run(
        "src.infrastructure.fastapi.static_server:app",
        host="0.0.0.0",
        port=5000,
        reload="false"
    )
