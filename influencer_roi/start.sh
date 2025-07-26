#!/bin/bash

# Influencer ROI Dashboard Startup Script

echo "🚀 Starting Influencer ROI Dashboard..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Setup Django backend
echo "⚙️ Setting up Django backend..."
cd backend

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Start Django server in background
echo "🌐 Starting Django server on http://localhost:8000..."
python manage.py runserver 8000 &
DJANGO_PID=$!

# Wait a moment for Django to start
sleep 3

# Setup Streamlit frontend
echo "📊 Setting up Streamlit frontend..."
cd ../frontend

# Start Streamlit app
echo "🎨 Starting Streamlit app on http://localhost:8501..."
streamlit run app.py --server.port 8501 &
STREAMLIT_PID=$!

echo ""
echo "✅ Dashboard is starting up!"
echo "📊 Frontend: http://localhost:8501"
echo "🔌 Backend API: http://localhost:8000"
echo "📚 Admin: http://localhost:8000/admin"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $DJANGO_PID 2>/dev/null
    kill $STREAMLIT_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait 