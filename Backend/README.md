# User Management API

A FastAPI backend with user and user details management connected to MySQL database.

## Features

- User authentication with secure password hashing
- User profile management 
- RESTful API endpoints
- MySQL database integration

## API Endpoints

- `GET /` - API root
- `POST /users/` - Create new user
- `GET /users/` - List all users
- `GET /users/{user_id}` - Get user by ID with details
- `POST /users/{user_id}/details/` - Add details to a user
- `GET /user-details/` - List all user details
- `GET /user-details/{detail_id}` - Get user detail by ID

## Running with Docker Compose

The easiest way to run the project is using Docker Compose:

```bash
# From the Backend directory
docker-compose up -d
```

This will:
1. Start the MySQL database
2. Start the FastAPI backend
3. Connect them on the same network

The API will be available at http://localhost:8000

## Running Locally

To run the project locally:

1. Start the MySQL database:
```bash
cd ../Database
docker build -t kub-database .
docker run -d -p 3306:3306 --name kub-db kub-database
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the FastAPI application:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

FastAPI automatically generates documentation for your API:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 