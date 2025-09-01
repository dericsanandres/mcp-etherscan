import os
from typing import Dict, List, Optional, Any, Type
from services.base_scanner import BaseScannerService
from services.etherscan_service import EtherscanService
from services.bscscan_service import BscscanService
from models import AddressBalance, Transaction, TokenTransfer, GasPrice


class ChainManager:
    """Orchestrates multiple blockchain scanner services"""
    
    def __init__(self, api_keys: Optional[Dict[str, str]] = None):
        """
        Initialize ChainManager with API keys
        
        Args:
            api_keys: Dict mapping chain names to API keys
                     If None, will load from environment variables
        """
        if api_keys is None:
            api_keys = {}
        
        # Chain configuration
        self.chain_info: Dict[str, Dict[str, Any]] = {
            'ethereum': {
                'service_class': EtherscanService,
                'env_var': 'ETHERSCAN_API_KEY',
                'native_token': 'ETH',
                'token_standard': 'ERC20',
                'explorer_url': 'https://etherscan.io'
            },
            'bsc': {
                'service_class': BscscanService,
                'env_var': 'BSCSCAN_API_KEY',
                'native_token': 'BNB',
                'token_standard': 'BEP20',
                'explorer_url': 'https://bscscan.com'
            }
        }
        
        # Initialize services for available chains
        self.services: Dict[str, BaseScannerService] = {}
        self._initialize_services(api_keys)
    
    def _initialize_services(self, api_keys: Dict[str, str]):
        """Initialize scanner services for chains with API keys"""
        for chain_name, chain_config in self.chain_info.items():
            # Get API key from parameter or environment
            api_key = api_keys.get(chain_name) or os.getenv(chain_config['env_var'])
            
            if api_key:
                service_class = chain_config['service_class']
                self.services[chain_name] = service_class(api_key)
    
    def get_available_chains(self) -> List[str]:
        """Get list of available chains"""
        return list(self.services.keys())
    
    def is_chain_available(self, chain: str) -> bool:
        """Check if a chain is available"""
        return chain.lower() in self.services
    
    def get_chain_info(self, chain: str) -> Dict[str, Any]:
        """Get information about a specific chain"""
        return self.chain_info.get(chain.lower(), {})
    
    def _get_service(self, chain: str) -> BaseScannerService:
        """Get service for a specific chain"""
        chain_lower = chain.lower()
        if chain_lower not in self.services:
            raise ValueError(f"Chain '{chain}' not available. Available chains: {list(self.services.keys())}")
        return self.services[chain_lower]
    
    # Single-chain operations
    def check_balance(self, address: str, chain: str = "ethereum") -> AddressBalance:
        """Check balance for an address on a specific chain"""
        service = self._get_service(chain)
        return service.get_address_balance(address)
    
    def get_transactions(self, address: str, chain: str = "ethereum", limit: int = 10) -> List[Transaction]:
        """Get transactions for an address on a specific chain"""
        service = self._get_service(chain)
        return service.get_transaction_history(address, limit)
    
    def get_token_transfers(self, address: str, chain: str = "ethereum", limit: int = 10) -> List[TokenTransfer]:
        """Get token transfers for an address on a specific chain"""
        service = self._get_service(chain)
        return service.get_token_transfers(address, limit)
    
    def get_contract_abi(self, address: str, chain: str = "ethereum") -> str:
        """Get contract ABI on a specific chain"""
        service = self._get_service(chain)
        return service.get_contract_abi(address)
    
    def get_gas_prices(self, chain: str = "ethereum") -> GasPrice:
        """Get gas prices for a specific chain"""
        service = self._get_service(chain)
        return service.get_gas_oracle()
    
    # Cross-chain operations
    def check_balance_multi_chain(self, address: str, chains: Optional[List[str]] = None) -> Dict[str, Any]:
        """Check balance across multiple chains"""
        if chains is None:
            chains = self.get_available_chains()
        
        results = {}
        for chain in chains:
            try:
                if self.is_chain_available(chain):
                    balance = self.check_balance(address, chain)
                    results[chain] = {
                        'success': True,
                        'balance': balance.dict(),
                        'native_token': self.get_chain_info(chain).get('native_token', 'Unknown')
                    }
                else:
                    results[chain] = {
                        'success': False,
                        'error': f"Chain '{chain}' not available"
                    }
            except Exception as e:
                results[chain] = {
                    'success': False,
                    'error': str(e)
                }
        
        return results
    
    def search_address_activity(self, address: str, chains: Optional[List[str]] = None) -> Dict[str, Any]:
        """Search for address activity across multiple chains"""
        if chains is None:
            chains = self.get_available_chains()
        
        results = {
            'address': address,
            'chains_searched': len(chains),
            'chains': {}
        }
        
        total_chains_with_activity = 0
        
        for chain in chains:
            chain_result = {
                'has_activity': False,
                'balance': None,
                'transaction_count': 0,
                'latest_transaction': None,
                'error': None
            }
            
            try:
                if not self.is_chain_available(chain):
                    chain_result['error'] = f"Chain '{chain}' not available"
                    results['chains'][chain] = chain_result
                    continue
                
                # Check balance
                balance = self.check_balance(address, chain)
                chain_result['balance'] = balance.dict()
                
                # Check if address has any activity (balance > 0 or transactions)
                if float(balance.balance_in_eth) > 0:
                    chain_result['has_activity'] = True
                
                # Get recent transactions to check activity
                try:
                    transactions = self.get_transactions(address, chain, limit=1)
                    if transactions:
                        chain_result['has_activity'] = True
                        chain_result['transaction_count'] = 1  # We only fetched 1
                        chain_result['latest_transaction'] = transactions[0].dict()
                except Exception:
                    # If we can't get transactions, still count as activity if balance > 0
                    pass
                
                if chain_result['has_activity']:
                    total_chains_with_activity += 1
                    
            except Exception as e:
                chain_result['error'] = str(e)
            
            results['chains'][chain] = chain_result
        
        results['chains_with_activity'] = total_chains_with_activity
        results['has_multi_chain_activity'] = total_chains_with_activity > 1
        
        return results