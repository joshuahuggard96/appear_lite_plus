#!/bin/bash
# Setup script for Appear Lite Plus on Raspberry Pi

echo "Setting up Appear Lite Plus..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it first."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env file with your configuration"
fi

# Initialize database
echo "Initializing database..."
python -c "from src.database.db import Database; db = Database()"

echo ""
echo "Setup complete!"
echo ""
echo "To start the server:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: python run.py"
echo ""
echo "Web interface will be available at http://localhost:5000"
echo "Default login: admin/admin"
