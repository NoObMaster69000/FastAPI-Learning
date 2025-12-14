# FastAPI Learning Path: From Beginner to Advanced

Welcome to the FastAPI Learning Path! This repository is a structured collection of code examples designed to guide you through learning FastAPI, from the absolute basics to advanced production-level concepts.

The examples are organized by skill level, with heavily commented code to explain the "why" behind the "how."

## Project Structure

The learning path is divided into three main directories, each representing a skill level:

-   `beginner/`: Core fundamentals for getting started with FastAPI.
-   `intermediate/`: More complex topics for building robust applications.
-   `advanced/`: High-level concepts for performance, architecture, and deployment.

Each skill-level directory contains subdirectories for specific topics (e.g., `01_core_fundamentals`, `04_database_integration`). Every topic folder is a self-contained, runnable FastAPI application.

## How to Use This Repository

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    ```

2.  **Navigate to an example:**
    Choose a topic you want to learn and change into its directory.
    ```bash
    # Example for the first lesson
    cd beginner/01_core_fundamentals
    ```

3.  **Install dependencies and run the server:**
    Most examples have their own `main.py` file. The general way to run them is with `uvicorn`. First, you'll need to install the dependencies. The root `requirements.txt` contains the base packages.
    ```bash
    # Install base dependencies from the root directory
    pip install -r requirements.txt

    # Navigate to an example and run it
    cd beginner/01_core_fundamentals
    uvicorn main:app --reload
    ```
    Some examples may have their own `requirements.txt` file for additional dependencies. Be sure to check the example's directory.

4.  **Explore the API:**
    Once the server is running, open your browser to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to see the interactive API documentation (Swagger UI).

## Topics Covered

### `beginner` - Core Fundamentals

-   **01_core_fundamentals:** Your first app, path operations (`GET`, `POST`), path and query parameters, request bodies, and automatic API docs.
-   **02_working_with_data:** Using Pydantic for data validation, defining response models, and using `Field` for extra validation.
-   **03_basic_features:** Handling form data, file uploads, headers, cookies, and serving static files.

### `intermediate` - Building Robust Applications

-   **01_advanced_data_handling:** Complex Pydantic models (nested models, custom validators).
-   **02_dependencies_and_architecture:** Dependency Injection, using classes as dependencies, and global dependencies.
-   **03_security_basics:** Authentication and authorization with OAuth2, JWT tokens, API keys, and HTTP Basic Auth.
-   **04_database_integration:** Connecting to a SQL database with SQLAlchemy, structuring your code with CRUD functions, and managing database sessions.
-   **05_error_handling:** Raising HTTP exceptions and creating custom exception handlers.
-   **06_testing:** Writing tests for your application with `pytest` and `TestClient`, and overriding dependencies.

### `advanced` - Performance, Architecture, and Deployment

-   **01_performance_and_scalability:** True `async` endpoints, background tasks, and streaming responses.
-   **02_advanced_architecture:** Organizing large applications with `APIRouter` and lifespan events.
-   **03_advanced_security:** Implementing CORS middleware and adding custom security headers.
-   **04_websockets:** Building real-time features with WebSockets.
-   **05_deployment_and_production:** Production considerations like configuration management (environment variables), structured logging, and containerizing your app with Docker and Gunicorn.

Enjoy your learning journey!
