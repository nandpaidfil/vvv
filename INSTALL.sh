#!/bin/bash

echo "🚀 Setting up NY Creation..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip -y

# Install virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required Python libraries
pip install -r requirements.txt

# Make files executable
chmod +x *

echo "✅ Setup complete! Run: python3 nand.py"
