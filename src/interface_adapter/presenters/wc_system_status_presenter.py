"""
Path: src/interface_adapter/presenters/wc_system_status_presenter.py
"""

from src.entities.wc_system_status import WCSystemStatus

class WCSystemStatusPresenter:
    " Presentador para transformar la entidad WCSystemStatus en un formato adecuado para la respuesta HTTP"
    @staticmethod
    def present(entity: WCSystemStatus) -> dict:
        "Transforma la entidad WCSystemStatus en un diccionario"
        return {
            "home_url": entity.home_url,
            "version": entity.version,
            "environment": entity.environment,
            "raw_data": entity.raw_data,
        }
