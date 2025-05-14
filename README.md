# Kub Project

A full-stack application with microservices architecture featuring a React frontend, FastAPI backend, MySQL database, Redis cache, and Kafka message broker.

## Project Overview

Kub Project is a modern web application demonstrating a complete microservices architecture with:

- **Frontend**: React application built with Vite
- **Backend**: FastAPI RESTful API service
- **Database**: MySQL for persistent data storage
- **Cache**: Redis for performance optimization
- **Message Broker**: Kafka for asynchronous processing

## Architecture

```
┌─────────────┐    ┌─────────────┐
│   Frontend  │───>│   Backend   │
│   (React)   │<───│  (FastAPI)  │
└─────────────┘    └──────┬──────┘
                          │
                ┌─────────┼────────────┐
                │         │            │
        ┌───────▼──┐ ┌────▼────┐ ┌─────▼─────┐
        │ Database │ │  Cache  │ │   Broker  │
        │  (MySQL) │ │ (Redis) │ │  (Kafka)  │
        └──────────┘ └─────────┘ └───────────┘
```

## Features

- User authentication and authorization
- User profile management
- RESTful API endpoints
- Caching layer with Redis
- Message processing with Kafka
- Containerized with Docker

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/kub-project.git
   cd kub-project
   ```

2. Start the application:
   ```bash
   docker-compose up -d
   ```

3. Access the application:
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Service Details

### Frontend (React + Vite)

A modern React application with:
- React Router for navigation
- User authentication and dashboard
- Communication with the backend API

### Backend (FastAPI)

A Python FastAPI application with:
- RESTful API endpoints
- User authentication with secure password hashing
- Integration with MySQL database
- Redis caching
- Kafka message processing

### Database (MySQL)

MySQL database for persistent storage with:
- User data storage
- User details management

### Cache (Redis)

Redis cache for performance optimization with:
- API response caching
- Session management

### Message Broker (Kafka)

Kafka for asynchronous message processing with:
- Event-driven architecture
- Message queuing

## Development

### Directory Structure

- `/Frontend`: React frontend application
- `/Backend`: FastAPI backend service
- `/Database`: MySQL database configuration
- `/Cache`: Redis cache configuration
- `/Broker`: Kafka broker configuration

### Running Individual Services

Each service can be built and run separately:

```bash
# Build and run the database
cd Database
docker build -t kub-database .
docker run -d -p 3306:3306 --name kub-database kub-database

# Build and run the cache
cd ../Cache
docker build -t kub-cache .
docker run -d -p 6379:6379 --name kub-cache kub-cache

# Build and run the Kafka broker
cd ../Broker
docker build -t kub-kafka .
docker run -d -p 9092:9092 --name kub-kafka kub-kafka

# Build and run the backend
cd ../Backend
docker build -t kub-backend .
docker run -d -p 8000:8000 --name kub-backend kub-backend

# Build and run the frontend
cd ../Frontend
docker build -t kub-frontend .
docker run -d -p 8080:80 --name kub-frontend kub-frontend
```

## API Documentation

The backend API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## License

[MIT License](LICENSE) 