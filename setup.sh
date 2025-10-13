#!/bin/bash

echo "Setting up AI Therapy Platform Backend..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create .env from example
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file - please configure it"
fi

# Create database
createdb ai_therapy 2>/dev/null || echo "Database already exists"

# Run migrations
alembic upgrade head

echo ""
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure .env file with your API keys"
echo "2. Run: uvicorn app.main:app --reload"
echo "3. Visit: http://localhost:8000/docs"
