# MCP Etherscan Server (Python)

A Python implementation of an MCP (Model Context Protocol) server that provides Ethereum blockchain data tools via Etherscan's API. Features include checking ETH balances, viewing transaction history, tracking ERC20 transfers, fetching contract ABIs, monitoring gas prices, and resolving ENS names.

## Features

- **Balance Checking**: Get ETH balance for any Ethereum address
- **Transaction History**: View recent transactions with detailed information
- **Token Transfers**: Track ERC20 token transfers with token details
- **Contract ABI**: Fetch smart contract ABIs for development
- **Gas Prices**: Monitor current gas prices (Safe Low, Standard, Fast)
- **ENS Resolution**: Resolve Ethereum addresses to ENS names

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

You can use commands like:
```
Check the balance of 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
```
or
```
Show me recent transactions for vitalik.eth
```

## Development

To add new features or modify existing ones:

1. The main server logic is in `src/server.py`
2. Etherscan API interactions are handled in `src/services/etherscan_service.py`
3. Models are defined in `src/models.py`

## License

MIT License - See LICENSE file for details
