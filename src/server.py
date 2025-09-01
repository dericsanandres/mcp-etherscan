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

from services.chain_manager import ChainManager
from models import (
    AddressInput,
    TransactionHistoryInput,
    TokenTransferInput,
    ContractInput
)

# Load environment variables
load_dotenv()

# Initialize Chain Manager (handles all chains)
chain_manager = ChainManager()

# Create MCP server
mcp = FastMCP("Etherscan Server")

@mcp.tool()
def check_balance(address: str, chain: str = "ethereum") -> str:
    """Check the native token balance of an address on any supported chain"""
    try:
        # Validate input
        input_data = AddressInput(address=address, chain=chain)
        balance = chain_manager.check_balance(input_data.address, input_data.chain)
        
        return f"Address: {balance.address}\nChain: {balance.chain}\nBalance: {balance.balance_in_eth} {balance.native_token}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_transactions(address: str, limit: int = 10, chain: str = "ethereum") -> str:
    """Get recent transactions for an address on any supported chain"""
    try:
        # Validate input
        input_data = TransactionHistoryInput(address=address, limit=limit, chain=chain)
        transactions = chain_manager.get_transactions(
            input_data.address, 
            input_data.chain,
            input_data.limit or 10
        )
        
        if not transactions:
            return f"No transactions found for {input_data.address} on {input_data.chain}"
        
        formatted_transactions = []
        for tx in transactions:
            date = datetime.fromtimestamp(tx.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            formatted_transactions.append(
                f"Block {tx.block_number} ({date}):\n"
                f"Hash: {tx.hash}\n"
                f"From: {tx.from_address}\n"
                f"To: {tx.to_address}\n"
                f"Value: {tx.value} {tx.native_token}\n"
                f"---"
            )
        
        return f"Recent transactions for {input_data.address} on {input_data.chain}:\n\n" + "\n".join(formatted_transactions)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_token_transfers(address: str, limit: int = 10, chain: str = "ethereum") -> str:
    """Get token transfers for an address on any supported chain"""
    try:
        # Validate input
        input_data = TokenTransferInput(address=address, limit=limit, chain=chain)
        transfers = chain_manager.get_token_transfers(
            input_data.address, 
            input_data.chain,
            input_data.limit or 10
        )
        
        if not transfers:
            return f"No token transfers found for {input_data.address} on {input_data.chain}"
        
        formatted_transfers = []
        for tx in transfers:
            date = datetime.fromtimestamp(tx.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            formatted_transfers.append(
                f"Block {tx.block_number} ({date}):\n"
                f"Token: {tx.token_name} ({tx.token_symbol})\n"
                f"Standard: {tx.token_standard}\n"
                f"From: {tx.from_address}\n"
                f"To: {tx.to_address}\n"
                f"Value: {tx.value}\n"
                f"Contract: {tx.token}\n"
                f"---"
            )
        
        return f"Recent token transfers for {input_data.address} on {input_data.chain}:\n\n" + "\n".join(formatted_transfers)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_contract_abi(address: str, chain: str = "ethereum") -> str:
    """Get the ABI for a smart contract on any supported chain"""
    try:
        # Validate input
        input_data = ContractInput(address=address, chain=chain)
        abi = chain_manager.get_contract_abi(input_data.address, input_data.chain)
        
        return f"Contract ABI for {input_data.address} on {input_data.chain}:\n\n{abi}"
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_gas_prices(chain: str = "ethereum") -> str:
    """Get current gas prices in Gwei for any supported chain"""
    try:
        prices = chain_manager.get_gas_prices(chain)
        
        return (
            f"Current Gas Prices on {prices.chain}:\n"
            f"Safe Low: {prices.safe_gwei} Gwei\n"
            f"Standard: {prices.propose_gwei} Gwei\n"
            f"Fast: {prices.fast_gwei} Gwei"
        )
    except Exception as e:
        return f"Error: {str(e)}"

# Multi-chain tools
@mcp.tool()
def check_balance_all_chains(address: str) -> str:
    """Check balance for an address across all available chains"""
    try:
        input_data = AddressInput(address=address)
        results = chain_manager.check_balance_multi_chain(input_data.address)
        
        formatted_results = []
        for chain, result in results.items():
            if result['success']:
                balance_info = result['balance']
                formatted_results.append(
                    f"{chain.upper()}: {balance_info['balance_in_eth']} {result['native_token']}"
                )
            else:
                formatted_results.append(f"{chain.upper()}: ERROR - {result['error']}")
        
        return f"Balance for {input_data.address} across all chains:\n\n" + "\n".join(formatted_results)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def search_address_activity(address: str) -> str:
    """Search for address activity across all available chains"""
    try:
        input_data = AddressInput(address=address)
        results = chain_manager.search_address_activity(input_data.address)
        
        summary = f"Activity Search for {results['address']}:\n"
        summary += f"Chains searched: {results['chains_searched']}\n"
        summary += f"Chains with activity: {results['chains_with_activity']}\n"
        summary += f"Multi-chain activity: {'Yes' if results['has_multi_chain_activity'] else 'No'}\n\n"
        
        chain_details = []
        for chain, info in results['chains'].items():
            if info['has_activity']:
                balance_info = info['balance']
                activity_info = f"{chain.upper()}: ACTIVE\n"
                activity_info += f"  Balance: {balance_info['balance_in_eth']} {balance_info['native_token']}\n"
                
                if info['latest_transaction']:
                    tx = info['latest_transaction']
                    date = datetime.fromtimestamp(tx['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                    activity_info += f"  Latest TX: {tx['hash'][:20]}... ({date})\n"
                
                chain_details.append(activity_info)
            elif info['error']:
                chain_details.append(f"{chain.upper()}: ERROR - {info['error']}\n")
            else:
                chain_details.append(f"{chain.upper()}: No activity detected\n")
        
        return summary + "\n".join(chain_details)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_available_chains() -> str:
    """Get list of available blockchain networks"""
    try:
        chains = chain_manager.get_available_chains()
        if not chains:
            return "No chains are currently available. Please check your API key configuration."
        
        chain_info = []
        for chain in chains:
            info = chain_manager.get_chain_info(chain)
            chain_info.append(
                f"{chain.upper()}: {info.get('native_token', 'Unknown')} "
                f"({info.get('token_standard', 'Unknown')} tokens)"
            )
        
        return f"Available chains ({len(chains)}):\n\n" + "\n".join(chain_info)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def get_ens_name(address: str) -> str:
    """Get the ENS name for an Ethereum address (Ethereum only)"""
    try:
        # Validate input
        input_data = AddressInput(address=address)
        # ENS is only available on Ethereum
        service = chain_manager._get_service("ethereum")
        ens_name = service.get_ens_name(input_data.address)
        
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
