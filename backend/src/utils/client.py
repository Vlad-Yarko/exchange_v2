from typing import Optional, Union
from functools import wraps

from aiohttp import ClientSession, ClientResponse


class Client:
    def __init__(
        self, 
        base_url: str, 
        endpoint: str ='', 
        params: Optional[dict] = None,
        payload: Optional[dict] = None
        ):
        self.session = None
        self.base_url = base_url
        self.endpoint = endpoint
        self.params = params
        self.payload = payload
        
    async def open_session(self) -> None:
        self.session = ClientSession(
            base_url=self.base_url
        )

    async def close_session(self) -> None:
        await self.session.close()
        
    async def get(self) -> ClientResponse:
        response = await self.session.get(
            url=self.endpoint,
            params=self.params
            )
        return response
        
    async def post(self) -> ClientResponse:
        response = await self.session.post(
            url=self.endpoint, 
            json=self.payload, 
            params=self.params
            )
        return response
    
    
class JSONClient(Client):
    def __init__(
        self, 
        base_url: str, 
        endpoint: str ='', 
        params: Optional[dict] = None,
        payload: Optional[dict] = None
        ):
        super().__init__(
            base_url=base_url,
            endpoint=endpoint,
            params=params,
            payload=payload
        )
        
    async def get(self) -> Union[list, dict, None]:
        response = await super().get()
        if response.status == 200:
            return await response.json()
        return None
        
    async def post(self) -> Union[list, dict, None]:
        response = await super().post()
        if response.status == 200:
            return await response.json()
        return None


class HTMLClient(Client):
    def __init__(
        self, 
        base_url: str, 
        endpoint: str ='', 
        params: Optional[dict] = None,
        payload: Optional[dict] = None
        ):
        super().__init__(
            base_url=base_url,
            endpoint=endpoint,
            params=params,
            payload=payload
        )
        
    async def get(self) -> str:
        response = await super().get()
        data = await response.text()
        return data
        
    async def post(self) -> str:
        response = await super().post()
        data = await response.text()
        return data


def http_session(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        session_was_already_open = self.client.session is not None and not self.client.session.closed
        if not session_was_already_open:
            await self.client.open_session()
        try:
            return await func(self, *args, **kwargs)
        finally:
            if not session_was_already_open:
                await self.client.close_session()
    return wrapper
