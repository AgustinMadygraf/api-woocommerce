"""
Presentador para estado del sistema local
"""
from src.entities.local_system_status import LocalSystemStatus
from typing import Dict

class LocalSystemStatusPresenter:
    @staticmethod
    def present(status: LocalSystemStatus) -> Dict:
        return status.to_dict()
