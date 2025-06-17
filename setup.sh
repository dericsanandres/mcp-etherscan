#!/bin/bash

# Setup script for MCP Etherscan Server

echo "Setting up MCP Etherscan Server..."

# Check if Python 3.9+ is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed"
    exit 1
fi

python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.9"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo "Error: Python 3.9 or higher is required (found $python_version)"
    exit 1
fi

echo "✓ Python $python_version found"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run validation test
echo "Running validation tests..."
python validate.py

if [ $? -ne 0 ]; then
    echo "❌ Validation failed. Please check the errors above."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your Etherscan API key"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Etherscan API key:"
echo "   ETHERSCAN_API_KEY=your_api_key_here"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Test the installation:"
echo "   python run.py test"
echo ""
echo "4. Run the server:"
echo "   python run.py run"
