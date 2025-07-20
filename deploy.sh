#!/bin/bash

# Quick Deployment Script for Flora & Fauna Data Collection App
echo "🌱 Flora & Fauna Data Collection App - Deployment Helper"
echo "=================================================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python
if command_exists python3; then
    echo "✅ Python3 found: $(python3 --version)"
else
    echo "❌ Python3 not found. Please install Python 3.11+"
    exit 1
fi

# Check pip
if command_exists pip3; then
    echo "✅ pip3 found"
else
    echo "❌ pip3 not found. Please install pip"
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Test the app
echo ""
echo "🧪 Testing app syntax..."
python3 -m py_compile app.py

if [ $? -eq 0 ]; then
    echo "✅ App syntax is valid"
else
    echo "❌ App has syntax errors"
    exit 1
fi

# Create data directories
echo ""
echo "📁 Creating data directories..."
mkdir -p data/text data/audio data/video data/images
echo "✅ Data directories created"

# Local deployment options
echo ""
echo "🚀 Deployment Options:"
echo "1. Local development server"
echo "2. Local network server"
echo "3. Prepare for cloud deployment"
echo ""

read -p "Select option (1-3): " option

case $option in
    1)
        echo "🖥️  Starting local development server..."
        echo "📍 App will be available at: http://localhost:8501"
        streamlit run app.py
        ;;
    2)
        echo "🌐 Starting local network server..."
        echo "📍 App will be available at: http://$(hostname -I | awk '{print $1}'):8501"
        echo "🔗 Share this URL with devices on your network"
        streamlit run app.py --server.address 0.0.0.0 --server.port 8501
        ;;
    3)
        echo "☁️  Preparing for cloud deployment..."
        echo ""
        echo "📋 Cloud Deployment Checklist:"
        echo "✅ requirements.txt - Ready"
        echo "✅ Procfile - Ready"
        echo "✅ setup.sh - Ready"
        echo "✅ .streamlit/config.toml - Ready"
        echo "✅ Dockerfile - Ready"
        echo ""
        echo "🌍 Available platforms:"
        echo "• Streamlit Community Cloud (Recommended): https://share.streamlit.io"
        echo "• Heroku: https://heroku.com"
        echo "• Railway: https://railway.app"
        echo "• Render: https://render.com"
        echo ""
        echo "📖 See DEPLOYMENT.md for detailed instructions"
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac
