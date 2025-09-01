from typing import Optional
from services.base_scanner import BaseScannerService


class EtherscanService(BaseScannerService):
    """Ethereum scanner service using Etherscan API"""
    
    def __init__(self, api_key: str):
        super().__init__(
            api_key=api_key,
            base_url="https://api.etherscan.io/api",
            chain_name="Ethereum",
            native_token="ETH"
        )
    
    def get_token_standard(self) -> str:
        """Return the token standard for Ethereum"""
        return "ERC20"
    
    def get_ens_name(self, address: str) -> Optional[str]:
        """Get ENS name for an address (placeholder implementation)"""
        try:
            # Note: Etherscan API doesn't directly support ENS reverse lookup
            # This would typically require a separate ENS provider or web3 connection
            # For now, returning None as a placeholder
            return None
        except Exception as e:
            raise Exception(f"Failed to get ENS name: {str(e)}")
