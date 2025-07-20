from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Config, Server

from src.utils.application import Application
from src.databases.mysql_manager import sessionmanager
from src.api.tags_metadata import tags_metadata
from src.api.origins import origins
from src.api.routers import *
from src.api.websockets import *


class API(Application):
    def __init__(self):
        super().__init__()
        self.title = "Exchange"
        self.tags_metadata = tags_metadata
        self.origins = origins
        self.routers = [
            user_router,
            crypto_router,
            currency_router
        ]
        self.websockets = [

        ]
    
    @staticmethod
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        sessionmanager.connect_to_db()
        yield
        await sessionmanager.close()

    def create(self) -> FastAPI:
        self.app = FastAPI(
            title=self.title,
            lifespan=self.lifespan,
            openapi_tags=self.tags_metadata
        )
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],  
        )
        for router in self.routers:
            self.app.include_router(router)
        for websocket in self.websockets:
            self.app.include_router(websocket)
        return self.app

    async def run(self, port: int = 8000) -> None:
        server_config = Config(
            app=self.app,
            port=port
        )
        server = Server(server_config)
        await server.serve()
