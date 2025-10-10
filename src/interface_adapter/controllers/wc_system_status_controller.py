"""
Path: src/interface_adapter/controllers/wc_system_status_controller.py
"""

from src.use_cases.get_wc_system_status_use_case import GetWCSystemStatusUseCase

class WCSystemStatusController:
    "Controlador para orquestar la obtención del estado del sistema WooCommerce"
    def __init__(self, use_case: GetWCSystemStatusUseCase):
        self.use_case = use_case

    async def get_status(self, auth: str = "basic"):
        "Obtiene el estado del sistema WooCommerce"
        return await self.use_case.execute(auth)
