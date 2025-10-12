"""
Path: src/interface_adapter/presenters/local_variable_products_presenter.py
"""

from typing import List, Dict
from src.entities.local_variable_product import LocalVariableProduct

class LocalVariableProductsPresenter:
    "Presentador para productos variables locales"
    @staticmethod
    def present(products: List[LocalVariableProduct]) -> List[Dict]:
        "Procesa productos para su presentación en la UI"
        rows = []
        for p in products:
            data = p.to_dict()
            # Mapeo de campos del backend local a los nombres esperados por la UI
            rows.append({
                "ID": data.get("ID_producto_variable", data.get("id", "")),
                "Nombre": data.get("formato", ""),
                "Estado": data.get("estado", ""),
                "Tipo": "LocalStore",  # Valor fijo para distinguir
                "Variaciones": data.get("variaciones", ""),
                "Stock": data.get("stock", ""),
            })
        return rows
