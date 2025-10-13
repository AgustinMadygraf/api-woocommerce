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

        "MODE": os.getenv("MODE"),  # CLI o FASTAPI

        # --- MySQL (si aplica) ---
        "MYSQL_HOST": os.getenv("MYSQL_HOST"),
        "MYSQL_PORT": os.getenv("MYSQL_PORT"),
        "MYSQL_USER": os.getenv("MYSQL_USER"),
        "MYSQL_PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "MYSQL_DATABASE": os.getenv("MYSQL_DATABASE"),

        # --- API Base URL ---
        "API_BASE": os.getenv("API_BASE"),
    }
    return config
