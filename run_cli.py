"""
Path: run_cli.py
"""

from src.infrastructure.cli.as400_woocommerce_cli import AS400WooCommerceCLI
from src.shared.config import get_config

config = get_config()
API_BASE = config.get("API_BASE")+"/api/wp-json/wc/v3"


if __name__ == "__main__":
    cli = AS400WooCommerceCLI(API_BASE)
    cli.run()
