#!/usr/bin/env python3

"""
Quick test runner for the MCP Etherscan Server
"""

import subprocess
import sys
import os

def run_test():
    """Run the test script"""
    print("Running Etherscan service tests...\n")
    
    try:
        result = subprocess.run([sys.executable, "test_service.py"], 
                              capture_output=True, text=True, timeout=30)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("Test timed out after 30 seconds")
        return False
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def run_server():
    """Run the MCP server"""
    print("Starting MCP Etherscan Server...\n")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([sys.executable, "src/server.py"])
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error running server: {e}")

def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        success = run_test()
        sys.exit(0 if success else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == "run":
        run_server()
    else:
        print("MCP Etherscan Server")
        print("===================")
        print()
        print("Usage:")
        print("  python run.py test  - Run tests")
        print("  python run.py run   - Start the server")
        print()
        print("Make sure you have:")
        print("1. Installed dependencies: pip install -r requirements.txt")
        print("2. Created .env file with ETHERSCAN_API_KEY")

if __name__ == "__main__":
    main()
