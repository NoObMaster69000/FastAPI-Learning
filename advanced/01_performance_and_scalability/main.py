# To run this example:
# 1. cd into the `advanced/01_performance_and_scalability` directory.
# 2. Run `uvicorn main:app --reload` in your terminal.
# 3. For rate limiting, you would typically use a library like `slowapi`.
#    pip install slowapi

import asyncio
from fastapi import FastAPI, BackgroundTasks, Depends, Request
from fastapi.responses import StreamingResponse
import time

app = FastAPI()

# --- Async/Await: True Async Endpoints ---

# By using `async def` for your path operations, you allow FastAPI to handle
# requests concurrently. When one request is waiting for an I/O operation
# (like reading from a database or calling another API), FastAPI can work
# on another request.

@app.get("/async-endpoint")
async def async_endpoint():
    """
    This is a true async endpoint.
    - `asyncio.sleep(1)` simulates a non-blocking I/O operation.
    - While this endpoint is "sleeping", the server can process other requests.
    """
    await asyncio.sleep(1)
    return {"message": "Async operation completed."}

@app.get("/sync-endpoint")
def sync_endpoint():
    """
    This is a synchronous endpoint.
    - `time.sleep(1)` is a blocking operation.
    - While this endpoint is "sleeping", the server cannot process other requests
      (unless you have multiple worker processes).
    """
    time.sleep(1)
    return {"message": "Sync operation completed."}

# --- Background Tasks ---

# Background tasks allow you to run operations after returning a response.
# This is useful for tasks that don't need to be completed before the client
# receives the response, such as sending an email or processing data.

def write_notification(email: str, message=""):
    """ A simple function that simulates sending an email. """
    with open("log.txt", mode="a") as email_file:
        content = f"Notification for {email}: {message}\n"
        email_file.write(content)
        # In a real app, this would be an actual email sending logic.
        time.sleep(5) # Simulate the time it takes to send an email.
        email_file.write(" - Email sent.")

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    """
    Sends a notification as a background task.
    - The response is sent immediately, and the `write_notification` function
      runs in the background.
    """
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}

# --- Streaming Responses ---

# `StreamingResponse` allows you to send a stream of data to the client
# without having to load it all into memory first. This is ideal for
pre large files.

async def fake_csv_generator():
    """ An async generator that yields CSV rows. """
    for i in range(10):
        yield f"{i},some_data,more_data\\n"
        await asyncio.sleep(0.5) # Simulate I/O delay

@app.get("/stream-csv")
async def stream_csv():
    """
    Streams a CSV file to the client.
    - The `fake_csv_generator` function is used to generate the data row by row.
    - The response is sent chunk by chunk, which is memory-efficient.
    """
    return StreamingResponse(fake_csv_generator(), media_type="text/csv")

# --- Caching and Rate Limiting (Conceptual) ---

# Caching and rate limiting are often implemented using dependencies and middleware.
# Libraries like `fastapi-cache` and `slowapi` are popular for this.

# Example of a conceptual rate limiter dependency:
# This is a simplified example. A real implementation would use a
# library like `slowapi` and a datastore like Redis to track requests.

async def rate_limiter(request: Request):
    """
    A conceptual dependency for rate limiting.
    - In a real app, this would check the request's IP address and
      the time of the last request to enforce a rate limit.
    """
    # Pseudo-code:
    # client_ip = request.client.host
    # if await is_rate_limited(client_ip):
    #     raise HTTPException(status_code=429, detail="Too Many Requests")
    return True

@app.get("/limited-route", dependencies=[Depends(rate_limiter)])
async def limited_route():
    """
    This endpoint is conceptually rate-limited.
    """
    return {"message": "You are within the rate limit."}
