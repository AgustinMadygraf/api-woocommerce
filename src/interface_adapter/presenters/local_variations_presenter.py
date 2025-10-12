"""
Path: src/interface_adapter/presenters/local_variations_presenter.py
"""

from typing import List, Dict
from src.entities.local_variation import LocalVariation

class LocalVariationsPresenter:
    "Presentador para variaciones de producto local"
    @staticmethod
    def present(variations: List[LocalVariation]) -> List[Dict]:
        "Procesa variaciones para su presentación en la UI"
        rows = []
        for v in variations:
            data = v.to_dict()
            rows.append({
                "ID": data.get("id_produto_variaciones", ""),
                "Cantidad": data.get("cantidad", ""),
                "Estado": data.get("estado", ""),
                "Manijas": "Sí" if data.get("es_manijas", False) else "No",
                "Precio Final": data.get("precio_final", ""),
                "Impresion": data.get("id_impresion", ""),
            })
        return rows
