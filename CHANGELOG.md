# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-17

### Added
- Initial Python implementation of MCP Etherscan Server
- Support for checking ETH balances
- Transaction history retrieval
- ERC20 token transfer tracking
- Contract ABI fetching
- Gas price monitoring
- ENS name resolution (placeholder)
- Comprehensive error handling and validation
- Pydantic models for input validation
- Environment variable configuration
- Setup scripts for Linux/Windows
- Test suite for service validation
- Docker configuration examples
- Documentation and configuration guides

### Features
- **Balance Checking**: Get ETH balance for any Ethereum address
- **Transaction History**: View recent transactions with detailed information
- **Token Transfers**: Track ERC20 token transfers with token details
- **Contract ABI**: Fetch smart contract ABIs for development
- **Gas Prices**: Monitor current gas prices (Safe Low, Standard, Fast)
- **ENS Resolution**: Resolve Ethereum addresses to ENS names

### Technical Details
- Python 3.9+ support
- Uses MCP (Model Context Protocol) for client communication
- Integrates with Etherscan API
- Web3.py for Ethereum utilities
- Async/await support for better performance
- Comprehensive input validation with Pydantic
- Environment-based configuration
- Cross-platform compatibility (Linux, macOS, Windows)

### Documentation
- README with installation and usage instructions
- Configuration examples for various setups
- Development setup guide
- API documentation through MCP schema definitions
