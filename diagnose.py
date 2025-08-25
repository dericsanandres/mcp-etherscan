#!/usr/bin/env python3

"""
Diagnostic script to help debug Etherscan API issues
"""

import os
import sys
import requests
from dotenv import load_dotenv

def test_api_key():
    """Test the Etherscan API key with detailed error reporting"""
    
    load_dotenv()
    
    api_key = os.getenv('ETHERSCAN_API_KEY')
    if not api_key:
        print("No ETHERSCAN_API_KEY found in environment variables")
        print("   Please check your .env file")
        return False
    
    print(f"API Key found: {api_key[:8]}...{api_key[-4:]} (masked)")
    print()
    
    # Test with a simple API call
    test_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    url = "https://api.etherscan.io/api"
    
    params = {
        'module': 'account',
        'action': 'balance',
        'address': test_address,
        'tag': 'latest',
        'apikey': api_key
    }
    
    print("Testing API call...")
    print(f"   URL: {url}")
    print(f"   Address: {test_address}")
    print()
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"HTTP Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        data = response.json()
        print(f"API Response:")
        print(f"   Status: {data.get('status', 'unknown')}")
        print(f"   Message: {data.get('message', 'none')}")
        
        if 'result' in data:
            print(f"   Result: {data['result']}")
        
        print()
        
        # Analyze the response
        status = data.get('status')
        message = data.get('message', '').lower()
        
        if status == '1':
            print("API call successful!")
            balance_wei = data.get('result', '0')
            balance_eth = int(balance_wei) / 10**18 if balance_wei.isdigit() else 0
            print(f"   Balance: {balance_eth:.6f} ETH")
            return True
        elif status == '0':
            print("API call failed!")
            if 'invalid api key' in message:
                print("   Issue: Invalid API Key")
                print("   Solutions:")
                print("   1. Check if your API key is correct")
                print("   2. Make sure you copied it correctly (no spaces/newlines)")
                print("   3. Verify the API key is activated on Etherscan")
            elif 'rate limit' in message or 'exceeded' in message:
                print("   Issue: Rate Limiting")
                print("   Solutions:")
                print("   1. Wait a few seconds and try again")
                print("   2. Consider upgrading your API plan if needed")
            elif 'max rate limit reached' in message:
                print("   Issue: Rate Limit Exceeded")
                print("   Solutions:")
                print("   1. Wait for rate limit reset (usually 1 second)")
                print("   2. Check your API plan limits")
            else:
                print(f"   Unknown issue: {message}")
                print("   Solutions:")
                print("   1. Check Etherscan API documentation")
                print("   2. Verify your API key status on etherscan.io")
        else:
            print(f"Unexpected status: {status}")
            print(f"   Message: {message}")
        
        return False
        
    except requests.exceptions.Timeout:
        print("Request timed out")
        print("   Check your internet connection")
        return False
    except requests.exceptions.ConnectionError:
        print("Connection error")
        print("   Check your internet connection")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def check_env_file():
    """Check the .env file setup"""
    print("Checking .env file...")
    
    if not os.path.exists('.env'):
        print(".env file not found")
        print("   Solutions:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your API key to the .env file")
        return False
    
    print(".env file exists")
    
    # Read the file and check format
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        if 'ETHERSCAN_API_KEY=' in content:
            print("ETHERSCAN_API_KEY variable found")
            
            # Extract the key
            for line in content.split('\n'):
                if line.startswith('ETHERSCAN_API_KEY='):
                    key_value = line.split('=', 1)[1].strip()
                    if not key_value or key_value == 'your_etherscan_api_key_here':
                        print("API key not set (still has placeholder)")
                        print("   Replace 'your_etherscan_api_key_here' with your actual API key")
                        return False
                    elif len(key_value) != 34:
                        print(f"Warning: API key length unusual: {len(key_value)} chars (expected 34)")
                        print("   Double-check your API key")
                    else:
                        print("API key appears to be set correctly")
                    break
        else:
            print("ETHERSCAN_API_KEY variable not found in .env")
            print("   Add: ETHERSCAN_API_KEY=your_actual_api_key")
            return False
            
    except Exception as e:
        print(f"Error reading .env file: {e}")
        return False
    
    return True

def main():
    """Main diagnostic function"""
    print("Etherscan API Diagnostic Tool")
    print("=" * 40)
    print()
    
    # Check .env file first
    if not check_env_file():
        print("\nFix the .env file issues above and try again")
        return False
    
    print()
    
    # Test API key
    if test_api_key():
        print("\nAll tests passed! Your API setup is working correctly.")
        return True
    else:
        print("\nPlease fix the API issues above and try again")
        print("\nGetting an API Key:")
        print("   1. Go to https://etherscan.io/apis")
        print("   2. Create a free account")
        print("   3. Generate an API key")
        print("   4. Add it to your .env file")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
