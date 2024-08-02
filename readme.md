# Hotel Booking System

This project is a comprehensive hotel booking system composed of multiple microservices, each handling a specific part of the system. The microservices communicate with each other using RabbitMQ, and the whole system is orchestrated using Docker Compose.

## Microservices

- **Authentication Service**: Handles user authentication and authorization.
- **Room Service**: Manages room availability and information.
- **Booking Service**: Handles booking operations.
- **Review Service**: Manages reviews and ratings for the hotel.
- **Notification Service**: Sends notifications to users.
- **RabbitMQ**: Message broker for inter-service communication.
- **PostgreSQL**: Database for each service.
- **PgAdmin**: Database administration tool.
- **Nginx**: Reverse proxy for routing requests to appropriate services.

## Prerequisites

- Docker
- Docker Compose

## Setup

### Clone the repository

```bash
git clone https://github.com/yourusername/hotel-booking-system.git
cd hotel-booking-system
```

## Environment Variables
Each service has its own .env_db file for database configuration. Make sure to create these files in the respective service directories (authentication_service, room_service, booking_service, review_service) with the necessary environment variables.

### Example .env_db file for authentication_service:

```
POSTGRES_DB=auth_db
POSTGRES_USER=auth_user
POSTGRES_PASSWORD=auth_password
```

## Build and Run
Build and run the services using Docker Compose:

```bash
docker-compose up --build
```
This command will start all the services defined in the docker-compose.yml file.

### Accessing Services
```
RabbitMQ Management: http://localhost:15672
Authentication Service: http://localhost/auth
Room Service: http://localhost/room
Booking Service: http://localhost/booking
Review Service: http://localhost/review
PgAdmin: http://localhost:5050
Nginx: http://localhost
```

### API Endpoints
#### Authentication Service
```
POST /auth/login: User login
POST /auth/register: User registration
GET /auth/jwt/users/me/: Get current user info
```

#### Room Service
```
GET /room/: List all rooms
POST /room/: Create a new room
```

#### Booking Service

```
GET /booking/: List all bookings
POST /booking/: Create a new booking
```

#### Review Service
```
GET /review/: List all reviews
POST /review/: Create a new review
```

#### Database Management
To manage the PostgreSQL databases, you can use PgAdmin:

1. Open http://localhost:5050
2. Login with:
    - Email: `admin@admin.com`
    - Password: `admin`


Add new servers for each service database using the credentials provided in their respective .env_db files.