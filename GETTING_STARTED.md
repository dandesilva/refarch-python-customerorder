# Getting Started with Customer Order Services (Python Edition)

This guide will help you quickly get the refactored Python application running.

## 🚀 5-Minute Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Navigate to project directory
cd /Users/ddesilva/Developer/projects/refarch-python-customerorder

# Start everything with one command
make up

# Wait about 30 seconds for database initialization, then access:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/api/docs
```

That's it! The application is running with PostgreSQL.

### Option 2: Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL (via Docker)
docker-compose up -d db

# Copy environment file
cp .env.example .env

# Run migrations
alembic upgrade head

# Start application
uvicorn app.main:app --reload
```

## 🧪 Testing the API

### 1. Get Authentication Token

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -u rbarcia:b0wfish
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "username": "rbarcia"
}
```

Save this token for subsequent requests:
```bash
export TOKEN="<your-token-here>"
```

### 2. Browse Products

**Get all categories:**
```bash
curl http://localhost:8000/api/v1/Category
```

**Get products in a category:**
```bash
curl http://localhost:8000/api/v1/Product?categoryId=2
```

**Get product details:**
```bash
curl http://localhost:8000/api/v1/Product/1
```

### 3. Manage Shopping Cart

**View your customer info:**
```bash
curl http://localhost:8000/api/v1/Customer \
  -H "Authorization: Bearer $TOKEN"
```

**Add item to cart:**
```bash
curl -X POST http://localhost:8000/api/v1/Customer/OpenOrder/LineItem \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"productId": 1, "quantity": 2}'
```

**Add another item:**
```bash
curl -X POST http://localhost:8000/api/v1/Customer/OpenOrder/LineItem \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"productId": 3, "quantity": 1}'
```

**View cart (get ETag for next step):**
```bash
curl -v http://localhost:8000/api/v1/Customer \
  -H "Authorization: Bearer $TOKEN" 2>&1 | grep -i etag
```

Save the ETag value (e.g., `2`):
```bash
export ETAG="2"
```

**Submit order:**
```bash
curl -X POST http://localhost:8000/api/v1/Customer/OpenOrder \
  -H "Authorization: Bearer $TOKEN" \
  -H "If-Match: $ETAG"
```

**View order history:**
```bash
curl http://localhost:8000/api/v1/Customer/Orders \
  -H "Authorization: Bearer $TOKEN"
```

## 📚 Interactive Documentation

The easiest way to explore the API is via the built-in Swagger UI:

1. Open http://localhost:8000/api/docs in your browser
2. Click "Authorize" button
3. Click "Login" to get token (username: `rbarcia`, password: `b0wfish`)
4. Copy the `access_token` from response
5. Enter in format: `Bearer <token>`
6. Click "Authorize"
7. Now you can test all endpoints interactively!

## 🔧 Common Operations

### View Logs
```bash
make logs
# or
docker-compose logs -f app
```

### Access Database
```bash
docker-compose exec db psql -U customerorder -d customerorderdb
```

### Run Migrations
```bash
make migrate
# or
docker-compose exec app alembic upgrade head
```

### Access App Shell
```bash
make shell
# or
docker-compose exec app /bin/bash
```

### Stop Everything
```bash
make down
# or
docker-compose down
```

### Clean Up (removes data!)
```bash
make clean
# or
docker-compose down -v
```

## 🐛 Troubleshooting

### "Connection refused" to database
Wait 10-15 seconds after `docker-compose up` for PostgreSQL to initialize.

### "Token expired"
Get a new token via `/api/v1/auth/login`

### "Order has been modified" (412 error)
Another request changed the order. Get fresh ETag from `/api/v1/Customer`

### Port 8000 already in use
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9

# Or change port in docker-compose.yml
```

### Cannot connect to Docker
```bash
# Make sure Docker Desktop is running
docker ps
```

## 📊 Default Test Data

### Users
- **Username:** `rbarcia` / **Password:** `b0wfish` (Residential Customer)
- **Username:** `bcorporate` / **Password:** `bcorporate` (Business Customer)

### Products
- Product 1: Laptop Pro 15 ($1,299.99)
- Product 2: Desktop Workstation ($899.99)
- Product 3: Office Chair ($249.99)
- Product 4: Coffee Maker ($79.99)
- Product 5: Laptop Air 13 ($999.99)

### Categories
- 1: Electronics (top-level)
  - 2: Computers
    - 3: Laptops
    - 4: Desktops
- 5: Home & Garden (top-level)
  - 6: Furniture
  - 7: Appliances

## 🎯 Next Steps

1. **Explore the API** - Use Swagger UI at http://localhost:8000/api/docs
2. **Review the Code** - Check out the clean architecture in `/app`
3. **Add Features** - Models, services, and routes are easy to extend
4. **Deploy** - Use the Dockerfile for any container platform
5. **Integrate** - Connect your frontend or other services

## 📖 Additional Resources

- [README.md](README.md) - Complete project documentation
- [CHANGELOG.md](CHANGELOG.md) - What changed from JEE version
- [API Docs](http://localhost:8000/api/docs) - Interactive API documentation

## 💡 Key Differences from JEE Version

| Aspect | JEE Version | Python Version |
|--------|-------------|----------------|
| **Auth** | HTTP Basic / LDAP | JWT Bearer Token |
| **Start** | First login | POST to `/auth/login` |
| **Format** | Headers: `Authorization: Basic <base64>` | Headers: `Authorization: Bearer <token>` |
| **Server** | WebSphere Liberty | Uvicorn (ASGI) |
| **Deploy** | WAR to Liberty | Docker container |

## ✅ Verification Checklist

After starting the application, verify:

- [ ] `curl http://localhost:8000/health` returns `{"status": "healthy"}`
- [ ] `docker-compose ps` shows both containers running
- [ ] http://localhost:8000/api/docs loads in browser
- [ ] Can login via `/auth/login` endpoint
- [ ] Can view categories and products
- [ ] Can add items to cart with authentication
- [ ] Can submit order with ETag

---

**Need Help?** Check the troubleshooting section or review the API documentation at `/api/docs`
