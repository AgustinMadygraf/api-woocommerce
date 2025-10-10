"""
CLI para consumir la API de WooCommerce con estética tipo AS400 IBM.
"""

import os

from src.infrastructure.cli.cli_app import AS400WooCommerceCLI

API_BASE = os.getenv("API_BASE", "http://localhost:5000/api/wp-json/wc/v3")


# Para ejecutar desde run_cli.py:
def run_cli():
    "Función para ejecutar el CLI"
    cli = AS400WooCommerceCLI(API_BASE)
    cli.run()


if __name__ == "__main__":
    run_cli()
