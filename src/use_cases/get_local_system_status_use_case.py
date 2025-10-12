"""
Caso de uso para obtener el estado del sistema local
"""
from src.entities.local_system_status import LocalSystemStatus
from src.interface_adapter.gateways.localstore_gateway import LocalStoreGateway
from typing import Optional

class GetLocalSystemStatusUseCase:
    def __init__(self, gateway: LocalStoreGateway):
        self.gateway = gateway

    def execute(self) -> Optional[LocalSystemStatus]:
        data, status = self.gateway.get_system_status()
        if status == 200 and data:
            return LocalSystemStatus(data)
        return None
