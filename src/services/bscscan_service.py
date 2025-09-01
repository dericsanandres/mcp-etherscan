from services.base_scanner import BaseScannerService


class BscscanService(BaseScannerService):
    """BSC scanner service using BSCScan API"""
    
    def __init__(self, api_key: str):
        super().__init__(
            api_key=api_key,
            base_url="https://api.bscscan.com/api",
            chain_name="BSC",
            native_token="BNB"
        )
    
    def get_token_standard(self) -> str:
        """Return the token standard for BSC"""
        return "BEP20"