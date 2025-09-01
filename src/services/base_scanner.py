from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from decimal import Decimal
import requests
import re

from models import AddressBalance, Transaction, TokenTransfer, GasPrice


class BaseScannerService(ABC):
    """Abstract base class for blockchain scanner services"""
    
    def __init__(self, api_key: str, base_url: str, chain_name: str, native_token: str):
        self.api_key = api_key
        self.base_url = base_url
        self.chain_name = chain_name
        self.native_token = native_token
    
    def _make_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to scanner API"""
        params['apikey'] = self.api_key
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') != '1':
                raise Exception(f"{self.chain_name} API error: {data.get('message', 'Request failed')}")
            
            return data
        except requests.RequestException as e:
            raise Exception(f"{self.chain_name} request failed: {str(e)}")
    
    def _wei_to_native(self, wei_value: str) -> str:
        """Convert Wei to native token (18 decimals for all EVM chains)"""
        if not wei_value or wei_value == '0':
            return '0'
        wei = Decimal(wei_value)
        native = wei / Decimal('1000000000000000000')  # 10^18
        return str(native)
    
    def _format_token_value(self, value: str, decimals: str) -> str:
        """Format token value based on decimals"""
        if not value or value == '0':
            return '0'
        
        try:
            decimals_int = int(decimals) if decimals else 18
            value_decimal = Decimal(value)
            formatted = value_decimal / (Decimal('10') ** decimals_int)
            return str(formatted)
        except (ValueError, TypeError):
            return value
    
    def _validate_address(self, address: str) -> str:
        """Validate EVM address format"""
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            raise ValueError(f"Invalid {self.chain_name} address format")
        return address.lower()
    
    def get_address_balance(self, address: str) -> AddressBalance:
        """Get native token balance for an address"""
        try:
            valid_address = self._validate_address(address)
            
            params = {
                'module': 'account',
                'action': 'balance',
                'address': valid_address,
                'tag': 'latest'
            }
            
            data = self._make_request(params)
            balance_wei = data['result']
            balance_native = self._wei_to_native(balance_wei)
            
            return AddressBalance(
                address=valid_address,
                balance_in_wei=int(balance_wei) if balance_wei else 0,
                balance_in_eth=balance_native,
                chain=self.chain_name,
                native_token=self.native_token
            )
        except Exception as e:
            raise Exception(f"Failed to get {self.chain_name} balance: {str(e)}")
    
    def get_transaction_history(self, address: str, limit: int = 10) -> List[Transaction]:
        """Get transaction history for an address"""
        try:
            valid_address = self._validate_address(address)
            
            params = {
                'module': 'account',
                'action': 'txlist',
                'address': valid_address,
                'startblock': '0',
                'endblock': '99999999',
                'page': '1',
                'offset': str(limit),
                'sort': 'desc'
            }
            
            data = self._make_request(params)
            transactions = []
            
            for tx in data.get('result', [])[:limit]:
                value_native = self._wei_to_native(tx.get('value', '0'))
                
                transactions.append(Transaction(
                    hash=tx.get('hash', ''),
                    from_address=tx.get('from', ''),
                    to_address=tx.get('to', '') or 'Contract Creation',
                    value=value_native,
                    timestamp=int(tx.get('timeStamp', '0')),
                    block_number=int(tx.get('blockNumber', '0')),
                    chain=self.chain_name,
                    native_token=self.native_token
                ))
            
            return transactions
        except Exception as e:
            raise Exception(f"Failed to get {self.chain_name} transaction history: {str(e)}")
    
    def get_token_transfers(self, address: str, limit: int = 10) -> List[TokenTransfer]:
        """Get token transfers for an address"""
        try:
            valid_address = self._validate_address(address)
            
            params = {
                'module': 'account',
                'action': 'tokentx',
                'address': valid_address,
                'page': '1',
                'offset': str(limit),
                'sort': 'desc'
            }
            
            data = self._make_request(params)
            transfers = []
            
            for tx in data.get('result', [])[:limit]:
                value_formatted = self._format_token_value(
                    tx.get('value', '0'), 
                    tx.get('tokenDecimal', '18')
                )
                
                transfers.append(TokenTransfer(
                    token=tx.get('contractAddress', ''),
                    token_name=tx.get('tokenName', ''),
                    token_symbol=tx.get('tokenSymbol', ''),
                    from_address=tx.get('from', ''),
                    to_address=tx.get('to', ''),
                    value=value_formatted,
                    timestamp=int(tx.get('timeStamp', '0')),
                    block_number=int(tx.get('blockNumber', '0')),
                    chain=self.chain_name,
                    token_standard=self.get_token_standard()
                ))
            
            return transfers
        except Exception as e:
            raise Exception(f"Failed to get {self.chain_name} token transfers: {str(e)}")
    
    def get_contract_abi(self, address: str) -> str:
        """Get contract ABI"""
        try:
            valid_address = self._validate_address(address)
            
            params = {
                'module': 'contract',
                'action': 'getabi',
                'address': valid_address
            }
            
            data = self._make_request(params)
            return data['result']
        except Exception as e:
            raise Exception(f"Failed to get {self.chain_name} contract ABI: {str(e)}")
    
    def get_gas_oracle(self) -> GasPrice:
        """Get current gas prices"""
        try:
            params = {
                'module': 'gastracker',
                'action': 'gasoracle'
            }
            
            data = self._make_request(params)
            result = data['result']
            
            return GasPrice(
                safe_gwei=result.get('SafeGasPrice', '0'),
                propose_gwei=result.get('ProposeGasPrice', '0'),
                fast_gwei=result.get('FastGasPrice', '0'),
                chain=self.chain_name
            )
        except Exception as e:
            raise Exception(f"Failed to get {self.chain_name} gas prices: {str(e)}")
    
    @abstractmethod
    def get_token_standard(self) -> str:
        """Return the token standard for this chain (ERC20, BEP20, etc.)"""
        pass