# Kub Project

A full-stack application with microservices architecture featuring a React frontend, FastAPI backend, MySQL database, Redis cache, and Kafka message broker.

## Project Overview

Kub Project is a modern web application demonstrating a complete microservices architecture with:

- **Frontend**: React application built with Vite
- **Backend**: FastAPI RESTful API service
- **Database**: MySQL for persistent data storage
- **Cache**: Redis for performance optimization
- **Message Broker**: Kafka for asynchronous processing
- **Kafka UI**: Kafdrop for monitoring Kafka

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────┐
│          Client Browser          │
└───────────────┬─────────────────┘
                │ HTTP/HTTPS
                ▼
┌─────────────────────────────────┐
│       Frontend (React/Vite)      │
│  Port: 8080 Container: kub-frontend │
└───────────────┬─────────────────┘
                │ HTTP/REST API
                ▼
┌─────────────────────────────────┐
│       Backend (FastAPI)         │
│  Port: 8000 Container: kub-backend  │
└───┬───────────────┬─────────────┘
    │               │
    ▼               │
┌────────────┐      │
│   Cache    │      │
│  (Redis)   │◄─────┤
│ Port: 6379 │      │
│ Container: │      │
│ kub-cache  │      │
└────────────┘      │
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
┌────────────┐ ┌────────────┐ ┌────────────┐
│  Database  │ │  Message   │ │  Eventual  │
│  (MySQL)   │ │   Broker   │ │ Consistency│
│ Port: 3306 │ │  (Kafka)   │ │   Events   │
│ Container: │ │ Port: 9092 │ │            │
│kub-database│ │ Container: │ │            │
└────────────┘ │ kub-kafka  │ └────────────┘
               └────────────┘
```

### Detailed Component Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                               FRONTEND                                   │
├─────────────────────────────────────────────────────────────────────────┤
│ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ │
│ │   React UI    │ │  React Router │ │ State Mgmt    │ │  API Service  │ │
│ │  Components   │ │  Navigation   │ │  (Context)    │ │  (HTTP/Fetch) │ │
│ └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘ │
└───────────────────────────────────────────────────────────────────────┬─┘
                                                                        │
                                                                        ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                                BACKEND                                   │
├─────────────────────────────────────────────────────────────────────────┤
│ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ │
│ │   FastAPI     │ │ Authentication│ │  Data Models  │ │  API Routes   │ │
│ │   Framework   │ │    Service    │ │  & Schemas    │ │   & Endpoints │ │
│ └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘ │
└┬────────────────────┬───────────────────────┬────────────────────────┬──┘
 │                    │                       │                        │
 ▼                    ▼                       ▼                        ▼
┌───────────┐ ┌──────────────────┐ ┌───────────────────┐ ┌─────────────────┐
│ Database  │ │ Cache Connection │ │  Message Broker   │ │ Authentication   │
│Connection │ │    & Service     │ │   Connection      │ │     Service      │
│ & Service │ │                  │ │    & Service      │ │                  │
└───────────┘ └──────────────────┘ └───────────────────┘ └─────────────────┘
     │                │                     │                    │
     ▼                ▼                     ▼                    │
┌──────────┐ ┌────────────┐ ┌─────────────────────┐             │
│ Database │ │   Cache    │ │    Message Broker   │<────────────┘
│  MySQL   │ │   Redis    │ │       Kafka         │
└──────────┘ └────────────┘ └─────────────────────┘
```

## Data Flow and Component Interactions

### Step-by-Step Workflow

1. **User Interaction Flow**
   1. User accesses the application through a web browser (http://localhost:8080)
   2. Frontend container (kub-frontend) serves the React application
   3. User interacts with the UI (login, registration, dashboard navigation)
   4. Frontend makes HTTP requests to the backend API

2. **Authentication Flow**
   1. User submits login credentials via the frontend
   2. Frontend sends authentication request to backend API
   3. Backend validates credentials against database
   4. Upon successful authentication:
      - Backend generates authentication token
      - Token is returned to frontend
      - Frontend stores token for subsequent API requests
   5. For protected routes, frontend includes token with requests

3. **Data Retrieval Flow**
   1. Frontend requests data from backend API
   2. Backend first checks Redis cache for requested data
      - If data exists in cache:
         * Data is served directly from cache (fast response)
         * Response header "X-Data-Source: redis_cache" is added
      - If data is not in cache:
         * Backend retrieves data from MySQL database
         * Data is stored in Redis cache for future requests
         * Response header "X-Data-Source: database" is added
   3. Data is returned to frontend for display

4. **Data Modification Flow**
   1. User submits form or triggers action to modify data
   2. Frontend sends request to backend API
   3. Backend updates the MySQL database
   4. Backend invalidates related Redis cache entries
   5. Backend publishes event to Kafka for:
      - Notification to other services
      - Audit logging
      - Eventual consistency operations
   6. Confirmation is sent back to frontend

5. **Asynchronous Processing Flow**
   1. Backend publishes messages to Kafka topics
   2. These messages might include:
      - User activity logs
      - System events
      - Data change notifications
   3. Other services/background processes consume these messages
   4. Enables eventual consistency and event-driven architecture

## Key Architecture Components

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
- Transactional operations
- Data integrity enforcement

### Cache (Redis)

Redis cache for performance optimization with:
- API response caching
- Session management
- High-performance key-value storage
- Configurable data expiration

### Message Broker (Kafka)

Kafka for asynchronous message processing with:
- Event-driven architecture
- Message queuing
- Reliable message delivery
- Topic-based communication
- Web UI monitoring via Kafdrop

### Monitoring and Management UIs

#### Kafdrop - Kafka Web UI
Kafdrop provides a web UI for monitoring Kafka clusters:
- View broker information
- Browse topics and topic messages
- View consumer groups
- Create topics
- View topic configuration
- Simple message publishing for testing

Access Kafdrop at: http://localhost:9000

## Technical Implementation Details

### Docker Container Network

All services are connected via the `kub-network` Docker bridge network, enabling:
- Service discovery using container names as hostnames
- Isolated network environment
- Secure inter-service communication

### Health Checks and Resilience

Each service implements health checks:
- Database: checks connection and query execution
- Redis: ping command to verify availability
- Kafka: topic listing to verify broker health
- Backend: comprehensive check of all dependent services
- Services automatically restart on failure (restart: on-failure)

### Data Persistence

- MySQL data is persisted using Docker volumes: `./Database/mysql_data:/var/lib/mysql`
- Redis data is persisted using Docker volumes: `./Cache/redis_data:/data`
- Kafka data is persisted using Docker volumes: `./Broker/kafka_data:/bitnami/kafka`

### Containerization

Each service is containerized with Docker:
- Standardized environment
- Isolated dependencies
- Simple deployment
- Scalability

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
   - Kafka UI (Kafdrop): http://localhost:9000

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