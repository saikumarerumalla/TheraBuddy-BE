# AI Therapy Platform - Backend API

Production-grade backend for AI-powered therapy platform.

## Features

- ✅ FastAPI async framework
- ✅ PostgreSQL with SQLAlchemy ORM
- ✅ Redis caching
- ✅ OpenAI GPT-4 / Anthropic Claude integration
- ✅ JWT authentication
- ✅ End-to-end encryption for sensitive data
- ✅ Crisis detection and intervention
- ✅ Mood tracking and analytics
- ✅ Rate limiting
- ✅ Structured logging
- ✅ Docker support

## Setup

### 1. Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker (optional)

### 2. Installation

```bash
# Clone repository
git clone <repo-url>
cd ai-therapy-backend

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### 3. Database Setup

```bash
# Create database
createdb ai_therapy

# Run migrations
alembic upgrade head
```

### 4. Running the Application

```bash
# Development
uvicorn app.main:app --reload --port 8000

# Production
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 5. Using Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login

### Chat
- `POST /api/v1/chat/message` - Send message to AI
- `POST /api/v1/chat/conversation` - Create conversation
- `POST /api/v1/chat/conversation/{id}/end` - End conversation

### Mood
- `POST /api/v1/mood/entry` - Create mood entry
- `GET /api/v1/mood/history` - Get mood history
- `GET /api/v1/mood/analytics` - Get mood analytics
- `POST /api/v1/mood/assessment` - Complete assessment

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update user profile
- `DELETE /api/v1/users/me` - Delete account

### Exercises
- `GET /api/v1/exercises/library` - Get exercise library
- `POST /api/v1/exercises/complete` - Mark exercise complete

### Resources
- `GET /api/v1/resources/crisis` - Get crisis resources
- `GET /api/v1/resources/articles` - Get educational articles

### Analytics
- `GET /api/v1/analytics/dashboard` - Get dashboard analytics

## Environment Variables

See `.env.example` for required configuration.

## Security

- All passwords are hashed with bcrypt
- Sensitive data encrypted at rest
- JWT tokens for authentication
- HTTPS required in production
- Rate limiting enabled
- CORS configured

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

## Deployment

See `docs/deployment.md` for production deployment instructions.

## License

Proprietary - All Rights Reserved
