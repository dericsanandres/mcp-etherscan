from typing import Optional
from pydantic import BaseModel, Field
import re

def validate_ethereum_address(v: str) -> str:
    """Validate Ethereum address format"""
    if not re.match(r'^0x[a-fA-F0-9]{40}$', v):
        raise ValueError('Invalid Ethereum address format')
    return v

class AddressBalance(BaseModel):
    address: str
    balance_in_wei: int
    balance_in_eth: str
    chain: Optional[str] = "Ethereum"
    native_token: Optional[str] = "ETH"

class Transaction(BaseModel):
    hash: str
    from_address: str
    to_address: str
    value: str
    timestamp: int
    block_number: int
    chain: Optional[str] = "Ethereum"
    native_token: Optional[str] = "ETH"

class TokenTransfer(BaseModel):
    token: str
    token_name: str
    token_symbol: str
    from_address: str
    to_address: str
    value: str
    timestamp: int
    block_number: int
    chain: Optional[str] = "Ethereum"
    token_standard: Optional[str] = "ERC20"

class GasPrice(BaseModel):
    safe_gwei: str
    propose_gwei: str
    fast_gwei: str
    chain: Optional[str] = "Ethereum"

class AddressInput(BaseModel):
    address: str = Field(..., description="EVM address (0x format)")
    chain: Optional[str] = Field(default="ethereum", description="Blockchain chain")
    
    def __init__(self, **data):
        super().__init__(**data)
        self.address = validate_ethereum_address(self.address)

class TransactionHistoryInput(BaseModel):
    address: str = Field(..., description="EVM address (0x format)")
    limit: Optional[int] = Field(default=10, ge=1, le=100, description="Number of transactions to return (max 100)")
    chain: Optional[str] = Field(default="ethereum", description="Blockchain chain")
    
    def __init__(self, **data):
        super().__init__(**data)
        self.address = validate_ethereum_address(self.address)

class TokenTransferInput(BaseModel):
    address: str = Field(..., description="EVM address (0x format)")
    limit: Optional[int] = Field(default=10, ge=1, le=100, description="Number of transfers to return (max 100)")
    chain: Optional[str] = Field(default="ethereum", description="Blockchain chain")
    
    def __init__(self, **data):
        super().__init__(**data)
        self.address = validate_ethereum_address(self.address)

class ContractInput(BaseModel):
    address: str = Field(..., description="Contract address (0x format)")
    chain: Optional[str] = Field(default="ethereum", description="Blockchain chain")
    
    def __init__(self, **data):
        super().__init__(**data)
        self.address = validate_ethereum_address(self.address)
