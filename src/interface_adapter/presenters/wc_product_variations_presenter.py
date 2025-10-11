"""
Presentador para variaciones de productos de WooCommerce
Transforma variaciones en datos listos para la UI
"""

from typing import List, Dict

class WCProductVariationsPresenter:
    @staticmethod
    def present(variations: List[Dict]) -> List[Dict]:
        """Procesa variaciones de producto para su presentación en la UI"""
        rows = []
        for var in variations:
            cantidad = ""
            manijas = ""
            impresion = ""
            con_sin_manijas = ""

            for attr in var.get("attributes", []):
                if attr.get("name", "").lower() == "cantidad":
                    cantidad = attr.get("option", "")
                elif attr.get("name", "").lower() == "impresión":
                    impresion = attr.get("option", "")
                elif attr.get("name", "").lower() == "con o sin manijas":
                    manijas = attr.get("option", "")
                    if manijas.strip().lower() == "con manijas":
                        con_sin_manijas = "Con manijas"
                    elif manijas.strip().lower() == "sin manijas":
                        con_sin_manijas = "Sin manijas"
                    else:
                        con_sin_manijas = manijas

            precio_final_raw = var.get("price")
            try:
                precio_final = "{:,.2f}".format(float(precio_final_raw)) if precio_final_raw else ""
            except (ValueError, TypeError):
                precio_final = precio_final_raw or ""

            rows.append({
                "ID": var.get("id"),
                "Precio": precio_final,
                "Cantidad": cantidad,
                "Estado": var.get("status"),
                "Manijas": manijas,
                "Impresion": impresion,
                "Precio Final": precio_final,
                "Con/Sin Manijas": con_sin_manijas,
            })

        # Ordenaciones
        rows.sort(key=lambda x: int(x["Cantidad"]) if str(x["Cantidad"]).isdigit() else 0)
        rows.sort(key=lambda x: str(x["Impresion"]).lower(), reverse=True)

        return rows
