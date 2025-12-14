# Production Considerations

This example demonstrates several best practices for running a FastAPI application in a production environment.

## How to Run This Example

### 1. Create a `.env` file

This application uses Pydantic's settings management to load configuration from environment variables. Create a file named `.env` in this directory with the following content:

```
ADMIN_EMAIL=your_admin_email@example.com
DATABASE_URL=postgresql://user:password@db_host:5432/your_db
```

### 2. Run with Uvicorn (for development)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Build and Run with Docker and Gunicorn (for production)

This is the recommended way to run the application in production.

**Build the Docker image:**

```bash
docker build -t fastapi-prod-example .
```

**Run the Docker container:**

```bash
docker run -d -p 80:80 --env-file .env --name my-fastapi-app fastapi-prod-example
```

This command will:
- Run the container in detached mode (`-d`).
- Map port 80 on the host to port 80 in the container (`-p 80:80`).
- Load the environment variables from your `.env` file (`--env-file .env`).
- Give the container a name (`--name my-fastapi-app`).

### 4. Nginx/Reverse Proxy

In a real production setup, you would typically run a reverse proxy like Nginx in front of your Gunicorn server. Nginx can handle things like:

- **SSL/TLS termination:** Handling HTTPS requests and encrypting/decrypting traffic.
- **Load balancing:** Distributing traffic across multiple instances of your application.
- **Serving static files:** Efficiently serving static content.
- **Security:** Implementing rate limiting, IP whitelisting/blacklisting, etc.

A typical setup would have Nginx listen on port 443 (HTTPS), and then proxy the requests to the Gunicorn server running on a non-privileged port (like 8000) inside the private network.
