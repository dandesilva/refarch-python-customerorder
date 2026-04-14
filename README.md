# Customer Order Services - Python Edition

A modern Python refactoring of the JEE Customer Order Services reference architecture, targeting containerized deployment.

> **✅ STATUS: Full stack is running with TWO web frontends!**
> - **Modern React Frontend:** http://localhost:3000
> - **Classic Dojo Frontend:** http://localhost:3001
> - **API Backend:** http://localhost:8000
> - **API Docs:** http://localhost:8000/api/docs
> 
> **Login:** rbarcia / b0wfish
> 
> See [FRONTENDS.md](FRONTENDS.md) for frontend comparison guide

## Overview

This project is a complete refactoring of the original JavaEE-based Customer Order Services application to a modern Python stack optimized for containerized environments. The application maintains feature parity with the original while leveraging modern technologies and cloud-native patterns.

### Original vs. Refactored Architecture

| Component | Original (JEE) | Refactored (Python) |
|-----------|----------------|---------------------|
| **Framework** | JavaEE / JAX-RS | FastAPI |
| **ORM** | JPA 2.0 / EJB 3.0 | SQLAlchemy 2.0 |
| **Database** | IBM DB2 | PostgreSQL |
| **App Server** | WebSphere Liberty | Uvicorn (ASGI) |
| **Security** | LDAP / Basic Auth | JWT Bearer Tokens |
| **Deployment** | WAR/EAR on Liberty | Podman/Docker Container |
| **Configuration** | XML (server.xml) | Environment Variables |

## Features

- **RESTful API** - Full REST API for customer, product, category, and order management
- **Domain Model** - Complete domain model with:
  - Customer (Business & Residential types with single-table inheritance)
  - Products with hierarchical categories
  - Orders with line items
  - Optimistic locking for concurrent updates
- **Authentication** - JWT-based authentication (vs. original LDAP/BasicAuth)
- **Database Migrations** - Alembic for schema versioning
- **Containerized** - Docker and docker-compose for easy deployment
- **OpenAPI/Swagger** - Interactive API documentation

## Quick Start

### Prerequisites

- **Podman & Podman Compose** (recommended) OR Docker & Docker Compose
- Make (optional, for convenience commands)

### Running with Podman Compose (Recommended)

1. **Navigate to the project**
   ```bash
   cd /Users/ddesilva/Developer/projects/refarch-python-customerorder
   ```

2. **Start the application**
   ```bash
   make up
   # or
   podman-compose up -d
   ```

### Running with Docker Compose (Alternative)

If using Docker instead of Podman, update the Makefile to use `docker-compose`:
```bash
# Edit Makefile and change COMPOSE = podman-compose to COMPOSE = docker-compose
# Or run directly:
docker-compose up -d
```

3. **Access the application**
   - API: http://localhost:8000
   - Interactive API Docs: http://localhost:8000/api/docs
   - ReDoc: http://localhost:8000/api/redoc

4. **View logs**
   ```bash
   make logs
   # or
   docker-compose logs -f
   ```

5. **Stop the application**
   ```bash
   make down
   # or
   docker-compose down
   ```

## API Usage

### Authentication

The application uses JWT Bearer token authentication. First, obtain a token:

```bash
# Login (using default user: rbarcia / password: b0wfish)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -u rbarcia:b0wfish

# Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "username": "rbarcia"
}
```

Use the token in subsequent requests:

```bash
export TOKEN="your-access-token-here"

# Get customer info
curl http://localhost:8000/api/v1/Customer \
  -H "Authorization: Bearer $TOKEN"
```

### Example API Calls

**Get Product Categories**
```bash
curl http://localhost:8000/api/v1/Category
```

**Get Products by Category**
```bash
curl http://localhost:8000/api/v1/Product?categoryId=2
```

**Get Product Details**
```bash
curl http://localhost:8000/api/v1/Product/1
```

**Add Item to Cart (requires authentication)**
```bash
curl -X POST http://localhost:8000/api/v1/Customer/OpenOrder/LineItem \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "productId": 1,
    "quantity": 2
  }'
```

**Submit Order (requires authentication and ETag)**
```bash
# First get current order with ETag
curl http://localhost:8000/api/v1/Customer \
  -H "Authorization: Bearer $TOKEN" \
  -v | grep -i etag

# Then submit with If-Match header
curl -X POST http://localhost:8000/api/v1/Customer/OpenOrder \
  -H "Authorization: Bearer $TOKEN" \
  -H "If-Match: 1"
```

**View Order History**
```bash
curl http://localhost:8000/api/v1/Customer/Orders \
  -H "Authorization: Bearer $TOKEN"
```

## Local Development

### Setup Python Environment

1. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start PostgreSQL**
   ```bash
   docker-compose up -d db
   ```

5. **Run migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the application**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

## Project Structure

```
refarch-python-customerorder/
├── app/
│   ├── models/          # SQLAlchemy domain models
│   ├── schemas/         # Pydantic request/response schemas
│   ├── services/        # Business logic layer
│   ├── api/
│   │   └── routes/      # REST API endpoints
│   ├── config.py        # Application configuration
│   ├── database.py      # Database connection
│   ├── auth.py          # Authentication & JWT
│   └── main.py          # FastAPI application
├── alembic/             # Database migrations
├── tests/               # Test suite
├── Dockerfile           # Container image definition
├── docker-compose.yml   # Multi-container setup
├── requirements.txt     # Python dependencies
└── README.md
```

## Key Architectural Patterns

### Single Table Inheritance
Customer types (Business/Residential) use SQLAlchemy's single-table inheritance, matching the original JPA `SINGLE_TABLE` strategy.

### Optimistic Locking
Orders use version numbers for optimistic concurrency control, preventing lost updates in concurrent scenarios.

### Service Layer Pattern
Business logic is encapsulated in service classes, separated from HTTP/API concerns.

### Dependency Injection
FastAPI's dependency injection system manages service lifecycle and database sessions.

## Configuration

The application is configured via environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |
| `SECRET_KEY` | JWT signing key | (required for production) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | `30` |
| `DEBUG` | Enable debug mode | `False` |
| `API_PREFIX` | API URL prefix | `/api/v1` |

See [.env.example](.env.example) for complete configuration options.

## Default Users

The seed data includes these test users:

| Username | Password | Type | Description |
|----------|----------|------|-------------|
| `rbarcia` | `b0wfish` | Residential | Default test user from original app |
| `bcorporate` | `bcorporate` | Business | Business customer example |

## Deployment

### Podman (Recommended)

Build and push to a container registry:

```bash
podman build -t customerorder-api:latest .
podman tag customerorder-api:latest your-registry/customerorder-api:latest
podman push your-registry/customerorder-api:latest
```

### Docker (Alternative)

```bash
docker build -t customerorder-api:latest .
docker tag customerorder-api:latest your-registry/customerorder-api:latest
docker push your-registry/customerorder-api:latest
```

### Kubernetes

Example deployment (create as needed):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: customerorder-api
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: your-registry/customerorder-api:latest
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        ports:
        - containerPort: 8000
```

## Testing

```bash
# Run all tests
make test

# Run with coverage
docker-compose exec app pytest --cov=app --cov-report=html
```

## Migration Notes from JEE Version

### What Changed?

1. **Database**: Migrated from DB2 to PostgreSQL
2. **Authentication**: JWT tokens replace LDAP/basic auth
3. **Deployment**: Container-first instead of app server deployment
4. **Configuration**: Environment variables instead of XML config
5. **API**: Async-capable FastAPI instead of JAX-RS

### What Stayed the Same?

1. **Domain Model**: Same entities and relationships
2. **Business Logic**: Order management, customer operations
3. **API Endpoints**: Similar REST API structure
4. **Optimistic Locking**: Version-based concurrency control
5. **Data Model**: Compatible schema structure

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project maintains the same license as the original JEE reference architecture.

## Related Projects

- Original JEE Version: https://github.com/ibm-cloud-architecture/refarch-jee-customerorder

## Support

For issues and questions:
- Check the [API documentation](http://localhost:8000/api/docs) when running
- Review the original project documentation for business logic questions
- Open an issue in the repository
