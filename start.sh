#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  String Analysis API - Quick Start${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 found${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt --quiet

echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}\n"
fi

# Start the server
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Starting FastAPI Server...${NC}"
echo -e "${GREEN}========================================${NC}\n"
echo -e "${BLUE}API will be available at:${NC}"
echo -e "${GREEN}  🌐 http://localhost:8000${NC}"
echo -e "${GREEN}  📚 http://localhost:8000/docs${NC}"
echo -e "${GREEN}  📖 http://localhost:8000/redoc${NC}\n"

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000