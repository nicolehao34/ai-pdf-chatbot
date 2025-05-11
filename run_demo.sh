#!/bin/bash

# Function to cleanup processes on exit
cleanup() {
    echo "Cleaning up..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if a port is in use
port_in_use() {
    lsof -i ":$1" >/dev/null 2>&1
}

# Set up cleanup on script exit
trap cleanup EXIT

# Check for required commands
echo "Checking dependencies..."
for cmd in python3 node npm; do
    if ! command_exists $cmd; then
        echo "Error: $cmd is not installed. Please install it first."
        exit 1
    fi
done

# Check if ports are available
if port_in_use 5173; then
    echo "Error: Port 5173 is already in use. Please free up this port."
    exit 1
fi

if port_in_use 8000; then
    echo "Error: Port 8000 is already in use. Please free up this port."
    exit 1
fi

# Backend setup
echo "Setting up backend..."
cd backend || exit 1

# Create and activate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
    # Update dependencies
    pip install --upgrade -r requirements.txt
fi

# Check if .env file exists, if not create it
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
    echo "Please update the OPENAI_API_KEY in backend/.env with your actual API key"
fi

# Start backend server
echo "Starting backend server..."
uvicorn main:app --reload &
BACKEND_PID=$!

cd ..

# Frontend setup
echo "Setting up frontend..."
cd frontend || exit 1

# Clean install of frontend dependencies
echo "Installing frontend dependencies..."
rm -rf node_modules package-lock.json
npm install
npm install -g vite

# Start frontend server
echo "Starting frontend server..."
npm run dev &
FRONTEND_PID=$!

cd ..

# Wait for both servers to start
echo "Waiting for servers to start..."
sleep 5

# Check if servers are running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "Error: Backend server failed to start"
    exit 1
fi

if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "Error: Frontend server failed to start"
    exit 1
fi

echo "Servers are running!"
echo "Frontend: http://localhost:5173"
echo "Backend: http://localhost:8000"
echo "Press Ctrl+C to stop both servers"

# Wait for user interrupt
wait 