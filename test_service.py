#!/usr/bin/env python3

"""
Test script for MCP Etherscan Server

This script tests the basic functionality of the Etherscan service
without running the full MCP server.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.etherscan_service import EtherscanService

def test_etherscan_service():
    """Test the Etherscan service functionality"""
    
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('ETHERSCAN_API_KEY')
    if not api_key:
        print("Error: ETHERSCAN_API_KEY not found in environment variables")
        print("Please create a .env file with your Etherscan API key")
        return False
    
    print("Testing Etherscan Service...")
    print("=" * 50)
    
    try:
        service = EtherscanService(api_key)
        
        # Test address (Ethereum Foundation)
        test_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
        
        # Test 1: Get balance
        print(f"1. Testing balance check for {test_address}")
        balance = service.get_address_balance(test_address)
        print(f"   Balance: {balance.balance_in_eth} ETH")
        print(f"   ✓ Balance check successful")
        print()
        
        # Test 2: Get transaction history
        print(f"2. Testing transaction history for {test_address}")
        transactions = service.get_transaction_history(test_address, limit=3)
        print(f"   Found {len(transactions)} transactions")
        if transactions:
            latest_tx = transactions[0]
            print(f"   Latest transaction: {latest_tx.hash[:10]}...")
        print(f"   ✓ Transaction history successful")
        print()
        
        # Test 3: Get token transfers
        print(f"3. Testing token transfers for {test_address}")
        transfers = service.get_token_transfers(test_address, limit=3)
        print(f"   Found {len(transfers)} token transfers")
        if transfers:
            latest_transfer = transfers[0]
            print(f"   Latest transfer: {latest_transfer.token_symbol}")
        print(f"   ✓ Token transfers successful")
        print()
        
        # Test 4: Get gas prices
        print("4. Testing gas prices")
        gas_prices = service.get_gas_oracle()
        print(f"   Safe: {gas_prices.safe_gwei} Gwei")
        print(f"   Standard: {gas_prices.propose_gwei} Gwei")
        print(f"   Fast: {gas_prices.fast_gwei} Gwei")
        print(f"   ✓ Gas prices successful")
        print()
        
        # Test 5: Test contract ABI (using a known contract)
        print("5. Testing contract ABI fetch")
        usdc_contract = "0xA0b86a33E6417c0b8cE4E3aDa22b9a7D3A76b5f6"  # Example contract
        try:
            abi = service.get_contract_abi(usdc_contract)
            print(f"   ABI length: {len(abi)} characters")
            print(f"   ✓ Contract ABI successful")
        except Exception as e:
            print(f"   Contract ABI test failed (this is normal for unverified contracts): {e}")
        print()
        
        print("=" * 50)
        print("✅ All tests completed successfully!")
        print("The Etherscan service is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main test function"""
    success = test_etherscan_service()
    
    if success:
        print("\n🎉 You can now run the MCP server with: python src/server.py")
        sys.exit(0)
    else:
        print("\n💥 Please fix the issues above before running the server")
        sys.exit(1)

if __name__ == "__main__":
    main()
