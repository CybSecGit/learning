#!/bin/bash

# Web Scraping Course Documentation Startup Script
# This script sets up and starts the Docusaurus development server

set -e

echo "🕷️  Web Scraping Course Documentation"
echo "======================================"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEBSITE_DIR="$SCRIPT_DIR/website"

echo "📁 Course directory: $SCRIPT_DIR"
echo "📁 Website directory: $WEBSITE_DIR"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ from https://nodejs.org"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node --version)"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Navigate to website directory
cd "$WEBSITE_DIR"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
else
    echo "✅ Dependencies already installed"
fi

# Start development server
echo ""
echo "🚀 Starting development server..."
echo "📖 Documentation will open at http://localhost:3000"
echo "🔄 Server will auto-reload when you edit files"
echo ""
echo "💡 Tip: This course is in web-scraping-course/ and can be"
echo "   easily moved to its own repository when ready!"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm run start
