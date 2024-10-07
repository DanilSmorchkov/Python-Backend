from dataclasses import dataclass, field
from typing import List, Dict
from uuid import uuid4

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect

app = FastAPI()


@dataclass(slots=True)
class ConnectionManager:
    active_connections: Dict[str, List[WebSocket]] = field(init=False, default_factory=dict)

    async def connect(self, websocket: WebSocket, chat_name: str) -> None:
        await websocket.accept()
        if chat_name not in self.active_connections:
            self.active_connections[chat_name] = []
        self.active_connections[chat_name].append(websocket)

    async def disconnect(self, websocket: WebSocket, channel_name: str) -> None:
        self.active_connections[channel_name].remove(websocket)

    async def publish(self, message: str, chat_name: str) -> None:
        for ws in self.active_connections[chat_name]:
            await ws.send_text(message)


connection_manager = ConnectionManager()


@app.websocket("/chat/{chat_name}")
async def chat(websocket: WebSocket, chat_name: str):
    client_id = str(uuid4())
    await connection_manager.connect(websocket=websocket, chat_name=chat_name)
    await connection_manager.publish(message=f"client {client_id} subscribed", chat_name=chat_name)

    try:
        while True:
            text = await websocket.receive_text()
            await connection_manager.publish(message=f"{client_id} :: {text}", chat_name=chat_name)
    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket=websocket, channel_name=chat_name)
        await connection_manager.publish(message=f"client {client_id} unsubscribed", chat_name=chat_name)