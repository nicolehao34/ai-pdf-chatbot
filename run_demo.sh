#!/bin/bash

# Function to cleanup processes on exit
cleanup() {
    echo "Cleaning up..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set up cleanup on script exit
trap cleanup EXIT

# Create and activate virtual environment if it doesn't exist
if [ ! -d "backend/venv" ]; then
    echo "Setting up Python virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    cd ..
else
    cd backend
    source venv/bin/activate
    cd ..
fi

# Check if .env file exists, if not create it
if [ ! -f "backend/.env" ]; then
    echo "Creating .env file..."
    echo "OPENAI_API_KEY=your_openai_api_key_here" > backend/.env
    echo "Please update the OPENAI_API_KEY in backend/.env with your actual API key"
fi

# Start backend
echo "Starting backend server..."
cd backend
source venv/bin/activate
uvicorn main:app --reload &
cd ..

# Start frontend
echo "Starting frontend server..."
cd frontend
npm install
npm run dev &

# Wait for both processes
wait 