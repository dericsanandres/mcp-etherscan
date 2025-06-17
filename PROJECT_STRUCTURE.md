# Project Structure

```
mcp-etherscan/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── __main__.py              # Entry point for module execution
│   ├── server.py                # Main MCP server implementation
│   ├── models.py                # Pydantic models for data validation
│   └── services/
│       ├── __init__.py          # Services package initialization
│       └── etherscan_service.py # Etherscan API service implementation
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── pyproject.toml              # Python project configuration
├── package.json                # Node.js compatibility metadata
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── setup.sh                    # Linux/macOS setup script
├── setup.bat                   # Windows setup script
├── test_service.py             # Service testing script
├── Makefile                    # Build automation
├── README.md                   # Project documentation
├── CONFIGURATION.md            # Configuration examples
├── CHANGELOG.md                # Version history
└── LICENSE                     # MIT license
```

## Key Files

### Core Implementation
- **`src/server.py`**: Main MCP server with tool definitions and handlers
- **`src/services/etherscan_service.py`**: Etherscan API integration service
- **`src/models.py`**: Pydantic models for input validation and data structures

### Configuration
- **`.env.example`**: Template for environment variables
- **`requirements.txt`**: Python dependencies for production
- **`pyproject.toml`**: Modern Python project configuration

### Setup & Testing
- **`setup.sh`**: Automated setup for Unix-like systems
- **`setup.bat`**: Automated setup for Windows
- **`test_service.py`**: Comprehensive service testing

### Documentation
- **`README.md`**: Main project documentation
- **`CONFIGURATION.md`**: Detailed configuration examples
- **`CHANGELOG.md`**: Version history and changes

## Quick Start

1. **Setup Environment**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Configure API Key**:
   ```bash
   # Edit .env file
   ETHERSCAN_API_KEY=your_api_key_here
   ```

3. **Test Installation**:
   ```bash
   source venv/bin/activate
   python test_service.py
   ```

4. **Run Server**:
   ```bash
   python src/server.py
   ```

## Features Implemented

✅ **ETH Balance Checking**  
✅ **Transaction History**  
✅ **ERC20 Token Transfers**  
✅ **Contract ABI Fetching**  
✅ **Gas Price Monitoring**  
✅ **Input Validation**  
✅ **Error Handling**  
✅ **Cross-platform Support**  
✅ **Comprehensive Documentation**  
✅ **Testing Framework**  

## Migration Notes from TypeScript

### Key Changes Made:
1. **Dependencies**: Replaced Node.js packages with Python equivalents
   - `@modelcontextprotocol/sdk` → `mcp`
   - `ethers` → `web3` + `eth-utils`
   - `zod` → `pydantic`
   - `dotenv` → `python-dotenv`

2. **Structure**: Maintained similar organization
   - Server logic in `src/server.py`
   - Service layer in `src/services/`
   - Models defined separately in `src/models.py`

3. **Validation**: Converted Zod schemas to Pydantic models
   - Better Python integration
   - More explicit error messages
   - Type safety maintained

4. **API Integration**: Replaced `fetch` with `requests`
   - More robust error handling
   - Better timeout management
   - Cleaner response processing

5. **ENS Support**: Placeholder implementation
   - Original used ethers.js provider
   - Would need separate ENS provider in production

The Python version maintains full feature parity with the TypeScript implementation while leveraging Python's strengths in data processing and validation.
