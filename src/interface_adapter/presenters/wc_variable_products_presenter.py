"""
Presentador para productos variables de WooCommerce
Transforma entidades WCVariableProduct en datos listos para la UI
"""

from typing import List, Dict
from src.entities.wc_variable_product import WCVariableProduct

class WCVariableProductsPresenter:
    @staticmethod
    def present(products: List[WCVariableProduct], variation_counts: Dict[int, str]) -> List[Dict]:
        """Procesa productos variables para su presentación en la UI"""
        rows = []
        for prod in products:
            rows.append({
                "ID": prod.id,
                "Nombre": prod.name,
                "Estado": getattr(prod, "status", ""),
                "Tipo": getattr(prod, "type", ""),
                "Variaciones": variation_counts.get(prod.id, "?"),
                "Stock": getattr(prod, "stock_quantity", None) if getattr(prod, "stock_quantity", None) is not None else "Por variación",
            })
        return rows
