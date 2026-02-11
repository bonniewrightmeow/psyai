# Getting Started with PsyAI

## Repository Structure

```
PsyAI/
├── README.md                # Project overview
├── GETTING_STARTED.md       # This file
│
├── src/psyai/
│   ├── core/                # Platform Layer 1 (Core Infrastructure)
│   ├── platform/            # Platform Layers 2-6
│   │   ├── vertexai_integration/
│   │   ├── vertexai_evaluation/
│   │   ├── centaur_integration/
│   │   ├── storage/
│   │   └── api/
│   └── features/            # Feature Layer (Parallel)
│       ├── chat/
│       ├── evals/
│       ├── hitl/
│       └── confidence/
│
├── tests/
├── scripts/
└── docker/
```

## Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

### Quick Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/PsyAILabs/PsyAI.git
cd PsyAI

# Run automated setup
bash scripts/setup_dev.sh

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Required keys:
# - ANTHROPIC_API_KEY
# - LANGSMITH_API_KEY
# - CENTAUR_API_KEY (when available)
```

3. **Start services:**
```bash
cd docker
docker-compose up -d postgres redis
```

# Initialize database
alembic upgrade head

# Run the API server
uvicorn psyai.platform.api_framework:app --host 0.0.0.0 --port 8000 --reload
```

### Manual Setup

#### 1. System Dependencies (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv python3-pip
sudo apt-get install -y build-essential libpq-dev
sudo apt-get install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

#### 2. Python Environment

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
```

#### 3. Environment Configuration

```bash
cp .env.example .env
```

Required environment variables:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_HOST` - Redis hostname (default: localhost)
- `SECRET_KEY` - JWT secret key (generate a secure random string)
- `GOOGLE_CLOUD_PROJECT` - GCP project ID
- `VERTEX_AI_LOCATION` - Vertex AI region (e.g., us-central1)

#### 4. Database & Cache Services

```bash
docker-compose up -d

# Verify services
docker-compose ps
docker exec psyai-postgres psql -U psyai -d psyai -c "SELECT version();"
docker exec psyai-redis redis-cli ping

# Run migrations
alembic upgrade head
```

## Development Workflow

### Running the Application

```bash
source venv/bin/activate

# Development mode with auto-reload
uvicorn psyai.platform.api_framework:app --host 0.0.0.0 --port 8000 --reload

# Production mode
uvicorn psyai.platform.api_framework:app --host 0.0.0.0 --port 8000 --workers 4
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=psyai --cov-report=html

# Run specific component tests
pytest tests/unit/core/
pytest tests/unit/platform/
pytest tests/unit/features/chat/
```

### Linting & Formatting

```bash
black src/
ruff src/
mypy src/
```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Restart service
docker-compose restart api

# Stop all
docker-compose down

# Reset database (WARNING: deletes all data)
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

## API Documentation

Once the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Quick API Test

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "username": "testuser", "password": "SecurePass123!", "full_name": "Test User"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=SecurePass123!"
```

## Coding Standards

- **Python 3.11+** required
- **Type hints** everywhere (`mypy` enforced)
- **Tests** required (80%+ coverage)
- **Code style:** Black, Ruff, isort (pre-commit hooks)

## Troubleshooting

### Database Connection Issues

```bash
docker-compose ps postgres
docker-compose logs postgres
docker-compose restart postgres
```

### Redis Connection Issues

```bash
docker-compose ps redis
docker-compose logs redis
docker exec psyai-redis redis-cli ping
```

### Port Already in Use

```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

### View Application Logs

```bash
tail -f logs/psyai.log
grep ERROR logs/psyai.log
```

## FAQ

**Q: Which feature should I work on?**
A: Choose based on interest. Chat and Confidence can start immediately. HITL requires Evals to be functional first.

**Q: How do features communicate?**
A: Through platform services only. No direct feature-to-feature imports.

**Q: Can features share code?**
A: Only through platform. Put shared logic in platform, not in features.

**Q: What about the Q1 2026 research study?**
A: All features must be complete and tested for study preparation.

## Getting Help

- Open a GitHub issue
- Consult the API documentation at `/docs`
- Contact project maintainers