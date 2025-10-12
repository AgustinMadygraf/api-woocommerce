"""
Path: run_cli.py
"""

import os

from src.infrastructure.cli.as400_woocommerce_cli import AS400WooCommerceCLI

API_BASE = os.getenv("API_BASE", "http://localhost:5000/api/wp-json/wc/v3")


if __name__ == "__main__":
    cli = AS400WooCommerceCLI(API_BASE)
    cli.run()
