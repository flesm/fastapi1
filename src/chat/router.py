from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter, Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.chat.models import Messages
from src.database import async_session_maker, get_async_session

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):  # падлключэнне карыстальніка
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):  # адключэнне карыстальніка
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):  # адпраўка персанальнага паведамлення
        await websocket.send_text(message)

    async def broadcast(self, message: str, add_to_db: bool):  # адпраўка масавага паведамлення
        if add_to_db:
            await self.add_message_to_database(message)
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def add_message_to_database(message: str):
        async with async_session_maker() as session:
            stmt = insert(Messages).values(
                message=message,
            )
            await session.execute(stmt)
            await session.commit()


manager = ConnectionManager()


@router.get("/last_messages")
async def get_last_messages(
        session: AsyncSession = Depends(get_async_session)
):
    query = select(Messages)
    messages = await session.execute(query)
    messages = messages.all()
    messages_list = [msg._asdict() for msg in messages]
    return messages_list


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}", add_to_db=True)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat", add_to_db=False)
