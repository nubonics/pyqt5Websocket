from typing import List

import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.requests import Request


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
app = FastAPI()


@app.post('/change_page')
async def change_page(request: Request):
    data = await request.json()

    # Here is where I need to send pageNum via the websocket, so that it reaches the client


@app.get("/")
async def get():
    return 'Welcome to Overseer, from our fastapi server.'


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            try:
                data = await websocket.receive()
            except RuntimeError:
                continue

            data = data.get('text')

            if data is None:
                # manager.disconnect(websocket)
                # await manager.broadcast(f"{client_id} left the chat")
                break
            elif 'page_number_' in data:
                await manager.send_personal_message(f"Hello, {client_id} from Overseer's fastapi websocket server.", websocket=websocket)
                # await manager.broadcast(f"Hello, from Overseer's fastapi websocket server.")
                await manager.broadcast(f"{client_id} left the chat")
                manager.disconnect(websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{client_id} left the chat")


if __name__ == "__main__":
    uvicorn.run("fastapi_server:app", host="127.0.0.1", port=8000, log_level="info")
