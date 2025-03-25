# Inventory Management API

## Project Title: Building a Backend API for a Simple Inventory Management System using Django Rest Framework

### Objective
Develop a backend API for an Inventory Management System that supports CRUD operations on inventory items, integrated with JWT-based authentication for secure access. The system utilizes Django Rest Framework (DRF), PostgreSQL for the database, Redis for caching, and includes unit tests to ensure functionality. It also implements error handling and logging for debugging and monitoring.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Database Migrations](#database-migrations)
- [Caching](#caching)
- [Testing](#testing)
- [Logging](#logging)
- [Usage Examples](#usage-examples)
- [API Documentation](#api-documentation)

---

## Project Overview
An inventory management system allows businesses to manage their stock efficiently. The API provides endpoints to create, read, update, and delete inventory items. Redis caching improves performance for frequently accessed items, and JWT authentication ensures secure access.

---

## Features
- Secure JWT authentication for API access.
- CRUD operations for inventory items.
- Redis caching for optimized performance.
- PostgreSQL database for structured data storage.
- Django ORM for database interaction.
- Unit tests for all API endpoints.
- Integrated logging system for debugging and monitoring.

---

## Technology Stack
- **Backend Framework**: Django Rest Framework (DRF)
- **Database**: PostgreSQL
- **Caching**: Redis
- **Authentication**: JWT (JSON Web Token)
- **Logging**: Python logging module
- **Testing**: Django Test Framework

---

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- PostgreSQL
- Redis
- Virtualenv

### Setup Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/ronygeorgen/Inventory-management.git
   cd inventory-management-api
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure environment variables in a `.env` file:
   ```ini
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_URL=postgres://user:password@localhost:5432/inventory_db
   REDIS_URL=redis://localhost:6379
   ```
5. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
6. Run the development server:
   ```sh
   python manage.py runserver
   ```

---

## API Endpoints
### Authentication
- **Register**: `POST /api/register/`
- **Login (Obtain JWT Token)**: `POST /api/token/`
- **Refresh Token**: `POST /api/token/refresh/`

### Item Management
- **Create Item**: `POST /api/items/`
- **Retrieve Item**: `GET /api/items/{item_id}/`
- **Update Item**: `PUT /api/items/{item_id}/`
- **Delete Item**: `DELETE /api/items/{item_id}/`

---

## Authentication
This API uses JWT authentication. Users must obtain a token via the `/api/token/` endpoint and include it in the `Authorization` header:
```sh
Authorization: Bearer <your-token>
```

---

## Database Migrations
After making changes to models, apply migrations:
```sh
python manage.py makemigrations
python manage.py migrate
```

---

## Caching
Redis is used to cache frequently accessed inventory items. Ensure Redis is running and configured in settings.

---

## Testing
Run tests to verify functionality:
```sh
python manage.py test
```

---

## Logging
Logging is enabled for tracking API requests, errors, and debugging information. Logs are stored in `logs/django.log`.

---

## Usage Examples
### Creating an Item
```sh
POST /api/items/
Content-Type: application/json
{
  "name": "Laptop",
  "description": "A powerful laptop",
  "quantity": 10,
  "price": 1200.50
}
```

### Retrieving an Item
```sh
GET /api/items/1/
Authorization: Bearer <your-token>
```

### Updating an Item
```sh
PUT /api/items/1/
Content-Type: application/json
Authorization: Bearer <your-token>
{
  "name": "Laptop Pro",
  "description": "An upgraded version",
  "quantity": 5,
  "price": 1500.75
}
```

### Deleting an Item
```sh
DELETE /api/items/1/
Authorization: Bearer <your-token>
```

---

## API Documentation
For detailed API documentation, refer to the Postman collection:
[Inventory Management API Documentation](https://documenter.getpostman.com/view/36618039/2sAYkKGx4p)

---

