#!/usr/bin/env python3

"""
MCP Etherscan Server

A Python implementation of an MCP (Model Context Protocol) server 
that provides Ethereum blockchain data tools via Etherscan's API.
"""

__version__ = "1.0.0"
__author__ = "Deric C San Andres"
__email__ = "dercsanandres@gmail.com"

from .server import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
