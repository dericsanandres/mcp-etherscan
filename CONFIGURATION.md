# MCP Etherscan Server Configuration Examples

## Claude Desktop Configuration

Add this to your Claude Desktop MCP settings:

```json
{
  "mcpServers": {
    "etherscan": {
      "command": "python",
      "args": ["/path/to/mcp-etherscan/src/server.py"],
      "env": {
        "ETHERSCAN_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Alternative: Using absolute path

```json
{
  "mcpServers": {
    "etherscan": {
      "command": "/path/to/mcp-etherscan/venv/bin/python",
      "args": ["/path/to/mcp-etherscan/src/server.py"]
    }
  }
}
```

## Environment Variables

Create a `.env` file in the project root:

```bash
# Etherscan API Key (required)
ETHERSCAN_API_KEY=your_etherscan_api_key_here

# Optional: Custom API endpoints (if using a different network)
# ETHERSCAN_BASE_URL=https://api.etherscan.io/api
```

## Systemd Service (Linux)

Create `/etc/systemd/system/mcp-etherscan.service`:

```ini
[Unit]
Description=MCP Etherscan Server
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/mcp-etherscan
Environment=ETHERSCAN_API_KEY=your_api_key_here
ExecStart=/path/to/mcp-etherscan/venv/bin/python src/server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable mcp-etherscan
sudo systemctl start mcp-etherscan
```

## Docker Configuration

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY .env .

CMD ["python", "src/server.py"]
```

Build and run:
```bash
docker build -t mcp-etherscan .
docker run -e ETHERSCAN_API_KEY=your_key mcp-etherscan
```

## Development Setup

For development with hot reload:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run with auto-reload (using watchdog)
pip install watchdog
watchmedo auto-restart --patterns="*.py" --recursive python src/server.py
```

## Testing Configuration

For testing without Claude Desktop:

```bash
# Test the service directly
python test_service.py

# Manual testing with MCP client
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | python src/server.py
```
