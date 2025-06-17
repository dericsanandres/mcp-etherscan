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

class Transaction(BaseModel):
    hash: str
    from_address: str
    to_address: str
    value: str
    timestamp: int
    block_number: int

class TokenTransfer(BaseModel):
    token: str
    token_name: str
    token_symbol: str
    from_address: str
    to_address: str
    value: str
    timestamp: int
    block_number: int

class GasPrice(BaseModel):
    safe_gwei: str
    propose_gwei: str
    fast_gwei: str

class AddressInput(BaseModel):
    address: str = Field(..., description="Ethereum address (0x format)")
    
    def __init__(self, **data):
        super().__init__(**data)
        self.address = validate_ethereum_address(self.address)

class TransactionHistoryInput(BaseModel):
    address: str = Field(..., description="Ethereum address (0x format)")
    limit: Optional[int] = Field(default=10, ge=1, le=100, description="Number of transactions to return (max 100)")
    
    def __init__(self, **data):
        super().__init__(**data)
        self.address = validate_ethereum_address(self.address)

class TokenTransferInput(BaseModel):
    address: str = Field(..., description="Ethereum address (0x format)")
    limit: Optional[int] = Field(default=10, ge=1, le=100, description="Number of transfers to return (max 100)")
    
    def __init__(self, **data):
        super().__init__(**data)
        self.address = validate_ethereum_address(self.address)

class ContractInput(BaseModel):
    address: str = Field(..., description="Contract address (0x format)")
    
    def __init__(self, **data):
        super().__init__(**data)
        self.address = validate_ethereum_address(self.address)
