#!/usr/bin/env python3

"""
Simple validation test for the MCP Etherscan Server setup
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        # Test basic Python imports
        import json
        import requests
        from decimal import Decimal
        from datetime import datetime
        print("   Standard library imports work")
        
        # Test third-party imports
        from dotenv import load_dotenv
        print("   python-dotenv import works")
        
        from pydantic import BaseModel, Field
        print("   pydantic import works")
        
        # Test MCP import
        from mcp.server.fastmcp import FastMCP
        print("   MCP FastMCP import works")
        
        return True
    except ImportError as e:
        print(f"   Import error: {e}")
        return False

def test_models():
    """Test that models work correctly"""
    print("\nTesting models...")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from models import AddressInput, validate_ethereum_address
        
        # Test valid address
        valid_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
        addr_input = AddressInput(address=valid_address)
        print(f"   Valid address validation works: {addr_input.address}")
        
        # Test invalid address
        try:
            invalid_address = "0xinvalid"
            AddressInput(address=invalid_address)
            print("   Invalid address should have failed")
            return False
        except ValueError:
            print("   Invalid address validation works")
        
        return True
    except Exception as e:
        print(f"   Model test error: {e}")
        return False

def test_service():
    """Test that service can be created (without API calls)"""
    print("\nTesting service creation...")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from services.etherscan_service import EtherscanService
        
        # Create service instance
        service = EtherscanService("test_api_key")
        print("   EtherscanService creation works")
        
        # Test helper methods
        wei_value = "1000000000000000000"  # 1 ETH in Wei
        eth_value = service._wei_to_eth(wei_value)
        if eth_value == "1":
            print("   Wei to ETH conversion works")
        else:
            print(f"   Wei to ETH conversion failed: {eth_value}")
            return False
        
        return True
    except Exception as e:
        print(f"   Service test error: {e}")
        return False

def test_server_creation():
    """Test that server can be created"""
    print("\nTesting server creation...")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        
        # Set dummy environment variable
        os.environ['ETHERSCAN_API_KEY'] = 'test_key'
        
        from mcp.server.fastmcp import FastMCP
        
        # Create server
        mcp = FastMCP("Test Server")
        print("   MCP server creation works")
        
        # Test tool decorator
        @mcp.tool()
        def test_tool(message: str) -> str:
            """A test tool"""
            return f"Echo: {message}"
        
        print("   Tool decorator works")
        
        return True
    except Exception as e:
        print(f"   Server creation error: {e}")
        return False

def check_environment():
    """Check environment setup"""
    print("\nChecking environment...")
    
    # Check .env file
    if os.path.exists('.env'):
        print("   .env file exists")
    else:
        print("   Warning: .env file not found - you'll need to create one")
    
    # Check Python version
    version = sys.version_info
    if version >= (3, 9):
        print(f"   Python {version.major}.{version.minor} is compatible")
    else:
        print(f"   Python {version.major}.{version.minor} is too old (need 3.9+)")
        return False
    
    return True

def main():
    """Run all validation tests"""
    print("MCP Etherscan Server Validation Test")
    print("=" * 45)
    
    tests = [
        ("Environment Check", check_environment),
        ("Import Test", test_imports),
        ("Models Test", test_models),
        ("Service Test", test_service),
        ("Server Creation Test", test_server_creation),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"\n{name} failed")
        except Exception as e:
            print(f"\n{name} failed with exception: {e}")
    
    print("\n" + "=" * 45)
    if passed == total:
        print(f"All {total} tests passed!")
        print("\nYour setup is ready! Next steps:")
        print("1. Add your Etherscan API key to .env file")
        print("2. Run: python run.py test")
        print("3. Run: python run.py run")
        return True
    else:
        print(f"{passed}/{total} tests passed")
        print("\nPlease fix the failing tests before proceeding.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
