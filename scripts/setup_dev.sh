#!/bin/bash

# PsyAI Development Environment Setup Script

set -e

echo "================================"
echo "PsyAI Development Setup"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."

# Detect Python command, prioritizing Python 3.11 or 3.12 (required: >=3.11,<3.13)
PYTHON_CMD=""
python_version=""

# Try Windows Python launcher with 3.11 first
if command -v py &> /dev/null; then
    py311_output=$(py -3.11 --version 2>&1)
    if [ $? -eq 0 ] && echo "$py311_output" | grep -q "Python [0-9]"; then
        PYTHON_CMD="py -3.11"
        python_version=$(echo "$py311_output" | awk '{print $2}')
    else
        # Try 3.12 as fallback
        py312_output=$(py -3.12 --version 2>&1)
        if [ $? -eq 0 ] && echo "$py312_output" | grep -q "Python [0-9]"; then
            PYTHON_CMD="py -3.12"
            python_version=$(echo "$py312_output" | awk '{print $2}')
        fi
    fi
fi

# If Windows launcher didn't work, try python3.11 (Linux/Mac style)
if [ -z "$PYTHON_CMD" ]; then
    python311_output=$(python3.11 --version 2>&1)
    if [ $? -eq 0 ] && echo "$python311_output" | grep -q "Python [0-9]"; then
        PYTHON_CMD="python3.11"
        python_version=$(echo "$python311_output" | awk '{print $2}')
    else
        # Try python3.12
        python312_output=$(python3.12 --version 2>&1)
        if [ $? -eq 0 ] && echo "$python312_output" | grep -q "Python [0-9]"; then
            PYTHON_CMD="python3.12"
            python_version=$(echo "$python312_output" | awk '{print $2}')
        fi
    fi
fi

# If still not found, try generic python/python3 but verify version
if [ -z "$PYTHON_CMD" ]; then
    python_test_output=$(python --version 2>&1)
    if [ $? -eq 0 ] && echo "$python_test_output" | grep -q "Python [0-9]"; then
        test_version=$(echo "$python_test_output" | awk '{print $2}')
        # Check if version is >= 3.11 and < 3.13
        if [ "$(printf '%s\n' "3.11" "$test_version" | sort -V | head -n1)" = "3.11" ] && \
           [ "$(printf '%s\n' "$test_version" "3.13" | sort -V | head -n1)" != "3.13" ]; then
            PYTHON_CMD="python"
            python_version="$test_version"
        fi
    fi
    
    if [ -z "$PYTHON_CMD" ]; then
        python3_test_output=$(python3 --version 2>&1)
        if [ $? -eq 0 ] && echo "$python3_test_output" | grep -q "Python [0-9]"; then
            test_version=$(echo "$python3_test_output" | awk '{print $2}')
            # Check if version is >= 3.11 and < 3.13
            if [ "$(printf '%s\n' "3.11" "$test_version" | sort -V | head -n1)" = "3.11" ] && \
               [ "$(printf '%s\n' "$test_version" "3.13" | sort -V | head -n1)" != "3.13" ]; then
                PYTHON_CMD="python3"
                python_version="$test_version"
            fi
        fi
    fi
fi

# Verify we found a compatible Python version
if [ -z "$PYTHON_CMD" ]; then
    echo "Error: Python 3.11 or 3.12 not found. Please install Python 3.11 or 3.12."
    echo "The project requires Python >=3.11,<3.13"
    exit 1
fi

required_version="3.11"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python $required_version or higher (but < 3.13) is required"
    echo "Current version: $python_version"
    exit 1
fi

# Check upper bound (must be < 3.13)
if [ "$(printf '%s\n' "$python_version" "3.13" | sort -V | head -n1)" = "3.13" ]; then
    echo "Error: Python 3.13 is not supported. Please use Python 3.11 or 3.12."
    echo "Current version: $python_version"
    exit 1
fi

echo "✓ Python $python_version found (using: $PYTHON_CMD)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    # Check if existing venv uses the correct Python version
    if [ -f "venv/pyvenv.cfg" ]; then
        venv_python=$(grep "^version" venv/pyvenv.cfg 2>/dev/null | awk '{print $3}' || echo "")
        if [ -n "$venv_python" ]; then
            # Check if venv Python version is compatible (>=3.11,<3.13)
            if [ "$(printf '%s\n' "3.11" "$venv_python" | sort -V | head -n1)" = "3.11" ] && \
               [ "$(printf '%s\n' "$venv_python" "3.13" | sort -V | head -n1)" != "3.13" ]; then
                echo "Virtual environment already exists with Python $venv_python. Skipping..."
            else
                echo "Existing virtual environment uses Python $venv_python (incompatible)."
                echo "Removing old virtual environment..."
                rm -rf venv
                $PYTHON_CMD -m venv venv
                echo "✓ Virtual environment recreated with Python $python_version"
            fi
        else
            echo "Virtual environment already exists. Skipping..."
        fi
    else
        echo "Virtual environment already exists. Skipping..."
    fi
else
    $PYTHON_CMD -m venv venv
    echo "✓ Virtual environment created with Python $python_version"
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
