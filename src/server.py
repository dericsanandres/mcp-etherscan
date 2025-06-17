#!/usr/bin/env python3

import asyncio
import os
import sys
from datetime import datetime
from typing import Any

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

from services.etherscan_service import EtherscanService
from models import (
    AddressInput,
    TransactionHistoryInput,
    TokenTransferInput,
    ContractInput
)

# Load environment variables
load_dotenv()

# Initialize Etherscan service
api_key = os.getenv('ETHERSCAN_API_KEY')
if not api_key:
    raise ValueError('ETHERSCAN_API_KEY environment variable is required')

etherscan_service = EtherscanService(api_key)

# Create MCP server
mcp = FastMCP("Etherscan Server")

@mcp.tool()
def check_balance(address: str) -> str:
    """Check the ETH balance of an Ethereum address"""
    try:
        # Validate input
        input_data = AddressInput(address=address)
        balance = etherscan_service.get_address_balance(input_data.address)
        
        return f"Address: {balance.address}\nBalance: {balance.balance_in_eth} ETH"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_transactions(address: str, limit: int = 10) -> str:
    """Get recent transactions for an Ethereum address"""
    try:
        # Validate input
        input_data = TransactionHistoryInput(address=address, limit=limit)
        transactions = etherscan_service.get_transaction_history(
            input_data.address, 
            input_data.limit or 10
        )
        
        if not transactions:
            return f"No transactions found for {input_data.address}"
        
        formatted_transactions = []
        for tx in transactions:
            date = datetime.fromtimestamp(tx.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            formatted_transactions.append(
                f"Block {tx.block_number} ({date}):\n"
                f"Hash: {tx.hash}\n"
                f"From: {tx.from_address}\n"
                f"To: {tx.to_address}\n"
                f"Value: {tx.value} ETH\n"
                f"---"
            )
        
        return f"Recent transactions for {input_data.address}:\n\n" + "\n".join(formatted_transactions)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_token_transfers(address: str, limit: int = 10) -> str:
    """Get ERC20 token transfers for an Ethereum address"""
    try:
        # Validate input
        input_data = TokenTransferInput(address=address, limit=limit)
        transfers = etherscan_service.get_token_transfers(
            input_data.address, 
            input_data.limit or 10
        )
        
        if not transfers:
            return f"No token transfers found for {input_data.address}"
        
        formatted_transfers = []
        for tx in transfers:
            date = datetime.fromtimestamp(tx.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            formatted_transfers.append(
                f"Block {tx.block_number} ({date}):\n"
                f"Token: {tx.token_name} ({tx.token_symbol})\n"
                f"From: {tx.from_address}\n"
                f"To: {tx.to_address}\n"
                f"Value: {tx.value}\n"
                f"Contract: {tx.token}\n"
                f"---"
            )
        
        return f"Recent token transfers for {input_data.address}:\n\n" + "\n".join(formatted_transfers)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_contract_abi(address: str) -> str:
    """Get the ABI for a smart contract"""
    try:
        # Validate input
        input_data = ContractInput(address=address)
        abi = etherscan_service.get_contract_abi(input_data.address)
        
        return f"Contract ABI for {input_data.address}:\n\n{abi}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_gas_prices() -> str:
    """Get current gas prices in Gwei"""
    try:
        prices = etherscan_service.get_gas_oracle()
        
        return (
            f"Current Gas Prices:\n"
            f"Safe Low: {prices.safe_gwei} Gwei\n"
            f"Standard: {prices.propose_gwei} Gwei\n"
            f"Fast: {prices.fast_gwei} Gwei"
        )
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_ens_name(address: str) -> str:
    """Get the ENS name for an Ethereum address"""
    try:
        # Validate input
        input_data = AddressInput(address=address)
        ens_name = etherscan_service.get_ens_name(input_data.address)
        
        return (
            f"ENS name for {input_data.address}: {ens_name}" 
            if ens_name 
            else f"No ENS name found for {input_data.address}"
        )
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main entry point"""
    print("Etherscan MCP Server running on stdio", file=sys.stderr)
    mcp.run()

if __name__ == "__main__":
    main()
