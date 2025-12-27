# Enterprise Task System

This is a high-demand, enterprise-level FastAPI application that demonstrates best practices for building scalable and maintainable systems.

## Features

- **Structured Project Layout:** A clean and organized project structure that separates concerns.
- **Database Migrations:** Using Alembic to manage database schema changes.
- **Dockerized Environment:** A `docker-compose.yml` file for easy local development and deployment.
- **Asynchronous Database Calls:** Using `async` and `await` for non-blocking database operations.
- **Dependency Injection:** Leveraging FastAPI's dependency injection system for clean and testable code.
- **Authentication and Authorization:** Secure endpoints with JWT-based authentication.
- **Configuration Management:** Using Pydantic's `BaseSettings` to manage configuration from environment variables.
- **Work ID Generation:** A system for generating and assigning unique work IDs to tasks.
- **Mail-like Message Formatting:** A service for formatting messages in a mail-like structure.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    ```

2.  **Create a `.env` file:**
    Copy the `.env.example` file to a new file named `.env` and update the values as needed.
    ```bash
    cp .env.example .env
    ```

3.  **Run with Docker Compose:**
    ```bash
    docker-compose up -d --build
    ```

4.  **Access the API:**
    The API will be available at [http://localhost:8000](http://localhost:8000). You can access the interactive API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

## Running Migrations

To create a new migration:
```bash
docker-compose exec api alembic revision --autogenerate -m "Your migration message"
```

To apply migrations:
```bash
docker-compose exec api alembic upgrade head
```

## Documentation

This project includes detailed, tutorial-style documentation for each module. You can find the documentation in the [`docs`](./docs) directory. It's recommended to read the documentation in conjunction with the source code to get a full understanding of the project.
