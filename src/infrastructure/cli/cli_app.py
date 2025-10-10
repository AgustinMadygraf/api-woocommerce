"""
Path: src/infrastructure/cli/cli_app.py
"""

import argparse
import asyncio
import sys
from httpx import Response

from src.shared.logger import get_logger
from src.shared.config import get_config

from src.interface_adapter.controllers.wc_system_status_controller import WCSystemStatusController
from src.infrastructure.httpx.httpx_service import get_wc_system_status
from src.interface_adapter.gateways.wc_system_status_httpx_gateway import WCSystemStatusHttpxGateway
from src.use_cases.get_wc_system_status_use_case import GetWCSystemStatusUseCase

logger = get_logger("woocommerce-cli")

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

async def system_status_command(auth="basic"):
    """Ejecuta el comando system_status en modo CLI"""
    cfg = get_config()
    wc_url = _build_wc_status_url(cfg["URL"])
    gateway = WCSystemStatusHttpxGateway(get_wc_system_status)
    use_case = GetWCSystemStatusUseCase(gateway, wc_url, cfg["CK"], cfg["CS"])
    controller = WCSystemStatusController(use_case)

    logger.info("Consultando estado del sistema WooCommerce en %s", wc_url)
    try:
        result = await controller.get_status(auth)
        if isinstance(result, Response) and result.status_code >= 400:
            logger.error("WooCommerce respondió error %s: %s", result.status_code, result.text[:400])
            sys.exit(1)

        logger.info("Estado del sistema recuperado correctamente")
        print(f"Environment: {result.home_url}")
        print(f"WooCommerce version: {result.version}")
        return result.raw_data
    except (KeyError, ValueError) as e:
        logger.error("Error de configuración o URL: %s", e)
        sys.exit(1)
    except Exception as e:
        logger.exception("Error inesperado en system_status_command: %s", e)
        raise

def run_cli():
    """Main entry point for CLI application"""
    parser = argparse.ArgumentParser(description='Cliente CLI para WooCommerce API')
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')

    # Comando system_status
    status_parser = subparsers.add_parser('status', help='Verificar estado del sistema WooCommerce')
    status_parser.add_argument('--auth', choices=['basic', 'query'], default='basic',
                              help='Método de autenticación: basic o query')

    # Agregar más comandos aquí según sea necesario

    args = parser.parse_args()

    if args.command == 'status':
        asyncio.run(system_status_command(args.auth))
    elif not args.command:
        parser.print_help()
        sys.exit(1)
    else:
        logger.error("Comando desconocido: %s", args.command)
        sys.exit(1)

if __name__ == "__main__":
    run_cli()
