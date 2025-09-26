# Todo Management API

A FastAPI-based RESTful API for managing todos with JWT authentication.

## Features

- User registration and authentication with JWT
- CRUD operations for todos
- Filtering and pagination for todo lists
- Secure password hashing
- MySQL database integration
- Alembic database migrations
- Pydantic request/response validation
- Environment-based configuration

## Prerequisites

- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd fast_api
   ```

2. Create a virtual environment and activate it:
   ```bash
   # On Windows
   python -m venv venv
   .\\venv\\Scripts\\activate
   
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the environment:
   - Copy `.env.example` to `.env`
   - Update the database credentials and other settings in `.env`

## Database Setup

1. Make sure MySQL is running
2. Create a new database (default name is `todo_db` or as specified in `.env`)
3. Run database migrations:
   ```bash
   alembic upgrade head
   ```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /api/v1/auth/signup` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token

### Todos (Requires Authentication)

- `GET /api/v1/todos/` - List all todos (with pagination)
- `POST /api/v1/todos/` - Create a new todo
- `GET /api/v1/todos/{todo_id}` - Get a specific todo
- `PUT /api/v1/todos/{todo_id}` - Update a todo
- `DELETE /api/v1/todos/{todo_id}` - Delete a todo

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MYSQL_SERVER` | MySQL server address | `localhost` |
| `MYSQL_USER` | MySQL username | `root` |
| `MYSQL_PASSWORD` | MySQL password | `` |
| `MYSQL_DB` | MySQL database name | `todo_db` |
| `SECRET_KEY` | JWT secret key | Random string |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time in minutes | `10080` (7 days) |
| `API_V1_STR` | API version prefix | `/api/v1` |

## Running Tests

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run tests
pytest
```

## Project Structure

```
app/
├── main.py                 # Application entry point
├── core/                   # Core functionality
│   ├── config.py           # Configuration settings
│   └── security.py         # Security utilities
├── database/               # Database related code
│   ├── connection.py       # Database connection
│   └── models.py           # SQLAlchemy models
├── schemas/                # Pydantic schemas
│   ├── user_schema.py      # User schemas
│   └── todo_schema.py      # Todo schemas
├── api/                    # API routes
│   ├── deps.py             # Dependencies
│   ├── auth_routes.py      # Authentication routes
│   └── todo_routes.py      # Todo routes
└── services/               # Business logic
    ├── user_service.py     # User related services
    └── todo_service.py     # Todo related services
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
