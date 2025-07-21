from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from uvicorn import Config, Server

from src.utils.application import Application
from src.databases.mysql_manager import sessionmanager
from src.api.metadata.tags_metadata import tags_metadata
from src.api.origins import origins
from src.api.routers import *
from src.api.websockets import *
from src.api.metadata import *


class API(Application):
    def __init__(self):
        super().__init__()
        self.title = title
        self.summary = summary
        self.description = description
        self.version = version
        self.openapi_url = openapi_url
        self.tags_metadata = tags_metadata
        self.default_response_class = ORJSONResponse
        self.terms_of_service = terms_of_service
        self.contact = contact
        self.license_info = license_info
        self.swagger_ui_parameters = swagger_ui_parameters
        self.origins = origins
        self.routers = [
            user_router,
            crypto_router,
            currency_router,
            email_router
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
            openapi_tags=self.tags_metadata,
            summary=self.summary,
            description=self.description,
            version=self.version,
            openapi_url=self.openapi_url,
            default_response_class=self.default_response_class,
            terms_of_service=self.terms_of_service,
            contact=self.contact,
            license_info=self.license_info,
            swagger_ui_parameters=self.swagger_ui_parameters
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
