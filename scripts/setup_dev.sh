#!/bin/bash

# PsyAI Development Environment Setup Script

set -e

echo "================================"
echo "PsyAI Development Setup"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."

# Detect Python command (python3 on Linux/Mac, python on Windows)
# Test actual execution and check output (Windows python3 alias shows error message)
PYTHON_CMD=""
python_test_output=$(python --version 2>&1)
if [ $? -eq 0 ] && echo "$python_test_output" | grep -q "Python [0-9]"; then
    PYTHON_CMD="python"
else
    python3_test_output=$(python3 --version 2>&1)
    if [ $? -eq 0 ] && echo "$python3_test_output" | grep -q "Python [0-9]"; then
        PYTHON_CMD="python3"
    else
        echo "Error: Python not found. Please install Python 3.11 or higher."
        echo "Tried 'python': $python_test_output"
        echo "Tried 'python3': $python3_test_output"
        exit 1
    fi
fi

# Get version
python_version_output=$($PYTHON_CMD --version 2>&1)
python_version=$(echo "$python_version_output" | awk '{print $2}')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python $required_version or higher is required"
    echo "Current version: $python_version"
    exit 1
fi
echo "✓ Python $python_version found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    $PYTHON_CMD -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
# Windows Git Bash uses Scripts/activate, Linux/Mac uses bin/activate
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "Error: Could not find virtual environment activation script"
    exit 1
fi
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -e ".[dev]"
echo "✓ Dependencies installed"
echo ""

# Copy environment file
echo "Setting up environment variables..."
if [ -f ".env" ]; then
    echo ".env file already exists. Skipping..."
else
    cp .env.example .env
    echo "✓ .env file created from .env.example"
    echo "⚠ Please edit .env and add your API keys"
fi
echo ""

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install
echo "✓ Pre-commit hooks installed"
echo ""

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p logs chroma_db data
echo "✓ Directories created"
echo ""

# Initialize database (if Docker is available)
if command -v docker &> /dev/null; then
    echo "Docker found. Starting database services..."
    echo "Run: docker-compose up -d postgres redis"
    echo ""
else
    echo "⚠ Docker not found. You'll need to set up PostgreSQL and Redis manually."
    echo ""
fi

echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Start database services: docker-compose up -d"
echo "3. Run database migrations: alembic upgrade head"
echo "4. Start the development server: uvicorn psyai.platform.api.app:app --reload"
echo ""
echo "For testing, run: pytest"
echo ""
echo "Happy coding! 🚀"
