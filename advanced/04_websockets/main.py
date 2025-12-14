# To run this example:
# 1. cd into the `advanced/04_websockets` directory.
# 2. Run `uvicorn main:app --reload` in your terminal.
# 3. Open the `index.html` file in your browser to interact with the WebSocket.

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

# A simple class to manage active WebSocket connections.
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# --- HTML for the WebSocket Client ---
# This is a simple HTML page that will be served by the root endpoint.
# It contains JavaScript to connect to the WebSocket and interact with it.
with open("index.html", "r") as f:
    html = f.read()

@app.get("/")
async def get():
    return HTMLResponse(html)

# --- WebSocket Endpoint ---

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    """
    This is the WebSocket endpoint.
    - It uses the `ConnectionManager` to handle connections.
    - It listens for incoming messages and broadcasts them to all clients.
    """
    await manager.connect(websocket)
    try:
        while True:
            # Wait for a message from the client.
            data = await websocket.receive_text()

            # Send a message back to the client that sent the message.
            await manager.send_personal_message(f"You wrote: {data}", websocket)

            # Broadcast the message to all other clients.
            await manager.broadcast(f"Client #{client_id} says: {data}")

    except WebSocketDisconnect:
        # When a client disconnects, remove them from the connection manager.
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")
