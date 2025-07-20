import asyncio

from fastapi import WebSocket, status

from src.utils.conn_manager import connection_manager

class WSManager:

    async def connect(self, websocket: WebSocket, user) -> bool:
        if isinstance(user, str):
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return False
        try:
            await websocket.accept()
        except RuntimeError:
            return False
        connection_manager.active_connections[user.id].add(websocket)
        connection_manager.active_tasks[websocket] = (asyncio.create_task(self.ping_loop(websocket)))
        return True
        
    async def disconnect(self, websocket: WebSocket, user) -> None:
        try:
            connection_manager.active_connections[user.id].discard(websocket)
            task = connection_manager.active_tasks[websocket]
            task.cancel()
            del connection_manager.active_tasks[websocket]
        except asyncio.CancelledError:
            pass
        except KeyError:
            pass
        if not connection_manager.active_connections[user.id]:
            try:
                del connection_manager.active_connections[user.id]
            except KeyError:
                return

    async def receive(self, websocket: WebSocket) -> None:
        data = await websocket.receive_json()
        if data and data.get("type") == "pong":
            pass
        
    async def send_ping(self, websocket: WebSocket) -> None:
        await websocket.send_json({'type': 'ping'}) 
    
    async def ping_loop(self, websocket: WebSocket) -> None:
        while True:
            await self.send_ping(websocket)
            await asyncio.sleep(10) 
