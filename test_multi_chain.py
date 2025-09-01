#!/usr/bin/env python3
"""
Test script for multi-chain blockchain scanner MCP server
Tests both single-chain and cross-chain functionality
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.chain_manager import ChainManager

# Load environment variables
load_dotenv()

def test_chain_initialization():
    """Test chain manager initialization"""
    print("=== Testing Chain Initialization ===")
    
    chain_manager = ChainManager()
    available_chains = chain_manager.get_available_chains()
    
    print(f"Available chains: {available_chains}")
    
    if not available_chains:
        print("❌ No chains available. Check your API keys in .env file:")
        print("  ETHERSCAN_API_KEY=your_ethereum_api_key")
        print("  BSCSCAN_API_KEY=your_bsc_api_key")
        return False
    
    print("✅ Chain manager initialized successfully")
    return True

def test_single_chain_operations():
    """Test single-chain operations"""
    print("\n=== Testing Single Chain Operations ===")
    
    chain_manager = ChainManager()
    
    # Test address with some activity  
    test_address = "0x8ba1f109551bD432803012645Hac136c27043bd4"  # Example address
    
    try:
        # Test balance check
        balance = chain_manager.check_balance(test_address, "ethereum")
        print(f"✅ Balance check: {balance.balance_in_eth} {balance.native_token} on {balance.chain}")
        
        # Test transaction history
        transactions = chain_manager.get_transactions(test_address, "ethereum", limit=3)
        print(f"✅ Transaction history: Found {len(transactions)} transactions")
        
        # Test gas prices
        gas_prices = chain_manager.get_gas_prices("ethereum")
        print(f"✅ Gas prices: {gas_prices.safe_gwei}/{gas_prices.propose_gwei}/{gas_prices.fast_gwei} gwei")
        
    except Exception as e:
        print(f"❌ Single chain test failed: {str(e)}")
        return False
    
    return True

def test_multi_chain_operations():
    """Test cross-chain operations"""
    print("\n=== Testing Multi-Chain Operations ===")
    
    chain_manager = ChainManager()
    
    # Test address that might have activity on multiple chains
    test_address = "0x8ba1f109551bD432803012645Hac136c27043bd4"
    
    try:
        # Test multi-chain balance check
        results = chain_manager.check_balance_multi_chain(test_address)
        print(f"✅ Multi-chain balance check: Tested {len(results)} chains")
        
        for chain, result in results.items():
            if result['success']:
                balance = result['balance']
                print(f"  {chain}: {balance['balance_in_eth']} {result['native_token']}")
            else:
                print(f"  {chain}: ERROR - {result['error']}")
        
        # Test address activity search
        activity_results = chain_manager.search_address_activity(test_address)
        print(f"✅ Activity search: {activity_results['chains_with_activity']}/{activity_results['chains_searched']} chains with activity")
        
        if activity_results['has_multi_chain_activity']:
            print("  📍 Multi-chain activity detected!")
        
    except Exception as e:
        print(f"❌ Multi-chain test failed: {str(e)}")
        return False
    
    return True

def test_error_handling():
    """Test error handling for invalid inputs"""
    print("\n=== Testing Error Handling ===")
    
    chain_manager = ChainManager()
    
    try:
        # Test invalid address
        try:
            chain_manager.check_balance("invalid_address")
            print("❌ Should have failed for invalid address")
            return False
        except Exception:
            print("✅ Invalid address rejected correctly")
        
        # Test unavailable chain
        try:
            chain_manager.check_balance("0x8ba1f109551bD432803012645Hac136c27043bd4", "nonexistent_chain")
            print("❌ Should have failed for unavailable chain")
            return False
        except Exception:
            print("✅ Unavailable chain rejected correctly")
        
    except Exception as e:
        print(f"❌ Error handling test failed: {str(e)}")
        return False
    
    return True

def test_backward_compatibility():
    """Test that original single-chain functionality still works"""
    print("\n=== Testing Backward Compatibility ===")
    
    try:
        # Import original service
        from services.etherscan_service import EtherscanService
        
        api_key = os.getenv('ETHERSCAN_API_KEY')
        if not api_key:
            print("⚠️ ETHERSCAN_API_KEY not found, skipping backward compatibility test")
            return True
        
        etherscan_service = EtherscanService(api_key)
        test_address = "0x8ba1f109551bD432803012645Hac136c27043bd4"
        
        # Test original methods still work
        balance = etherscan_service.get_address_balance(test_address)
        print(f"✅ Original service balance check: {balance.balance_in_eth} ETH")
        
        # Verify new chain fields are populated
        if hasattr(balance, 'chain') and hasattr(balance, 'native_token'):
            print(f"✅ New fields populated: {balance.chain}, {balance.native_token}")
        else:
            print("❌ New fields not populated in backward compatibility")
            return False
        
    except Exception as e:
        print(f"❌ Backward compatibility test failed: {str(e)}")
        return False
    
    return True

def main():
    """Main test runner"""
    print("🔗 Multi-Chain Blockchain Scanner Test Suite")
    print("=" * 50)
    
    tests = [
        test_chain_initialization,
        test_single_chain_operations,
        test_multi_chain_operations,
        test_error_handling,
        test_backward_compatibility
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {str(e)}")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Multi-chain implementation ready.")
        return 0
    else:
        print("⚠️ Some tests failed. Check configuration and implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())