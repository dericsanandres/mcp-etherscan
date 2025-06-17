@echo off

REM Setup script for MCP Etherscan Server (Windows)

echo Setting up MCP Etherscan Server...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please edit .env file and add your Etherscan API key
) else (
    echo .env file already exists
)

echo Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your Etherscan API key
echo 2. Activate the virtual environment: venv\Scripts\activate.bat
echo 3. Run the server: python src\server.py

pause
