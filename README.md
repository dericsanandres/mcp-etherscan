# MCP Etherscan Server (Python)

A **Python implementation** of an MCP (Model Context Protocol) server that provides comprehensive Ethereum blockchain data through Etherscan's API. Built with modern Python tools and designed for seamless integration with Claude Desktop.

🚀 **Ready for Production** | 🐍 **Pure Python** | 🔗 **MCP Compatible** | ⚡ **Fast & Reliable**

## Features

- 💰 **ETH Balance Checking**: Get real-time ETH balance for any Ethereum address
- 📈 **Transaction History**: View recent transactions with detailed information
- 🪙 **Token Transfers**: Track ERC20 token transfers with comprehensive token details
- 📜 **Smart Contract ABI**: Fetch verified smart contract ABIs for development
- ⛽ **Live Gas Prices**: Monitor current gas prices (Safe, Standard, Fast) in real-time
- 🏷️ **ENS Resolution**: Resolve Ethereum addresses to ENS names
- 🔍 **Input Validation**: Robust address validation with clear error messages
- 🚀 **Modern Architecture**: Built with FastMCP and Pydantic for reliability

## Prerequisites

- Python >= 3.9
- An Etherscan API key (get one at https://etherscan.io/apis)

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd mcp-etherscan
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```bash
ETHERSCAN_API_KEY=your_api_key_here
```

## Quick Start

### Option 1: Use the setup script (recommended)
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

## Testing the Installation

Before running the server, test that everything works:
```bash
# Activate virtual environment
source venv/bin/activate

# Run tests
python run.py test
```

**Expected Output:**
```
🧪 Testing Etherscan Service...
==================================================
1. Testing balance check for 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
   Balance: 1,247.832156789012345678 ETH
   ✓ Balance check successful

2. Testing transaction history for 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
   Found 3 transactions
   Latest transaction: 0xa1b2c3d4e5...
   ✓ Transaction history successful

3. Testing token transfers for 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
   Found 3 token transfers
   Latest transfer: USDC
   ✓ Token transfers successful

4. Testing gas prices
   Safe: 12.5 Gwei
   Standard: 15.2 Gwei
   Fast: 18.7 Gwei
   ✓ Gas prices successful

5. Testing contract ABI fetch
   Contract ABI test completed
   ✓ All core functions working
==================================================
✅ All tests completed successfully!
The Etherscan service is working correctly.
```

## Running the Server

Start the server:
```bash
# Using the run script (recommended)
python run.py run

# Or directly
python src/server.py
```

The server will run on stdio, making it compatible with MCP clients like Claude Desktop.

## How It Works

This server implements the Model Context Protocol (MCP) to provide tools for interacting with Ethereum blockchain data through Etherscan's API. Each tool is exposed as an MCP endpoint that can be called by compatible clients.

### Available Tools

1. `check-balance`
   - Input: Ethereum address
   - Output: ETH balance in both Wei and ETH

2. `get-transactions`
   - Input: Ethereum address, optional limit
   - Output: Recent transactions with timestamps, values, and addresses

3. `get-token-transfers`
   - Input: Ethereum address, optional limit
   - Output: Recent ERC20 token transfers with token details

4. `get-contract-abi`
   - Input: Contract address
   - Output: Contract ABI in JSON format

5. `get-gas-prices`
   - Input: None
   - Output: Current gas prices in Gwei

6. `get-ens-name`
   - Input: Ethereum address
   - Output: Associated ENS name if available

## Using with Claude Desktop

To add this server to Claude Desktop:

1. Start the server using `python src/server.py`

2. In Claude Desktop:
   - Go to Settings
   - Navigate to the MCP Servers section
   - Click "Add Server"
   - Enter the following configuration:
     ```json
     {
       "name": "Etherscan Tools (Python)",
       "transport": "stdio",
       "command": "python /path/to/mcp-etherscan/src/server.py"
     }
     ```
   - Save the configuration

3. The Etherscan tools will now be available in your Claude conversations

### Example Usage in Claude

Once connected, you can interact with Ethereum data naturally:

**Balance Queries:**
```
Check the balance of 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

**Transaction Analysis:**
```
Show me the last 5 transactions for vitalik.eth
```

**Gas Price Monitoring:**
```
What are the current Ethereum gas prices?
```

**Token Transfer Tracking:**
```
Find recent USDC transfers for 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
```

## Network Focus

This server is **specifically designed for Ethereum Mainnet** analysis. For other networks:

- **BSC (Binance Smart Chain)**: Planned as separate `mcp-bsc-server` repository
- **Polygon**: Planned as separate `mcp-polygon-server` repository  
- **Arbitrum**: Planned as separate `mcp-arbitrum-server` repository
- **Other chains**: Each will have dedicated MCP servers for optimal performance

> **Why separate servers?** This modular approach ensures better maintainability, independent deployments, and network-specific optimizations.

## Development

To add new features or modify existing ones:

1. The main server logic is in `src/server.py`
2. Etherscan API interactions are handled in `src/services/etherscan_service.py`
3. Models are defined in `src/models.py`

## License

MIT License - See LICENSE file for details
