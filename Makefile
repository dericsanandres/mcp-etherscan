# Makefile for MCP Etherscan Server

.PHONY: help install install-dev test clean lint format run setup

# Default target
help:
	@echo "Available commands:"
	@echo "  setup       - Run initial setup (create venv, install deps)"
	@echo "  install     - Install production dependencies"
	@echo "  install-dev - Install development dependencies"
	@echo "  test        - Run tests"
	@echo "  lint        - Run linting (flake8, mypy)"
	@echo "  format      - Format code (black, isort)"
	@echo "  run         - Run the MCP server"
	@echo "  clean       - Clean up generated files"

# Setup everything
setup:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file - please edit it"; fi

# Install production dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Run tests
test:
	python test_service.py

# Run linting
lint:
	flake8 src/
	mypy src/

# Format code
format:
	black src/
	isort src/

# Run the server
run:
	python src/server.py

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
