"""
Path: src/shared/config.py
"""

import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    "Load configuration from environment variables"
    config = {
        # --- Logging ---
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),

        # --- WooCommerce API ---
        "URL": os.getenv("URL"),  # p.ej. https://midominio.com/
        "CK": os.getenv("CK"),    # consumer key
        "CS": os.getenv("CS"),    # consumer secret

        # --- MySQL (si aplica) ---
        "MYSQL_HOST": os.getenv("MYSQL_HOST"),
        "MYSQL_PORT": os.getenv("MYSQL_PORT"),
        "MYSQL_USER": os.getenv("MYSQL_USER"),
        "MYSQL_PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "MYSQL_DATABASE": os.getenv("MYSQL_DATABASE"),
    }
    return config


def require_config(keys: list[str]):
    "Lanza excepción si faltan claves críticas"
    cfg = get_config()
    missing = [k for k in keys if not cfg.get(k)]
    if missing:
        raise RuntimeError(f"Faltan variables de entorno requeridas: {', '.join(missing)}")
    return cfg
