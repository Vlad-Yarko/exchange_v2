from typing import Callable, Awaitable, Type, Optional, Union

from fastapi import Depends, HTTPException, status, Response, Path, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.utils.service import Service
from src.types.dependency_factory import TSchemaBody, TSchemaPublic, TDataSchemaPublic


class DependencyFactory:
    def __init__(
        self,
        service_dep: Optional[Callable[[], Awaitable[Service]]] = None,
        SchemaBody: Optional[Type[TSchemaBody]] = None,
        SchemaPublic: Optional[Type[TSchemaPublic]] = None,
        DataSchemaPublic: Optional[Type[TDataSchemaPublic]] = None,
        alert_func: Optional[Callable[[], Awaitable]] = None
    ):
        self.service_dep = service_dep
        self.SchemaBody = SchemaBody
        self.SchemaPublic = SchemaPublic
        self.DataSchemaPublic = DataSchemaPublic
        self.security = HTTPBearer()
        self.alert_func = alert_func
        
    def token_dep(self) -> Callable[[], Awaitable[dict]]:
        async def dep(
            service = Depends(self.service_dep),
            authorization: HTTPAuthorizationCredentials = Depends(self.security)) -> dict:
            data = authorization.model_dump()
            try:
                if data.get("scheme") != "Bearer":
                    raise ValueError
                token = data["credentials"]
                d = await service.validate_token(token)
                if isinstance(d, str):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=d
                    )
                return d
            except (ValueError, KeyError):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authenticated"   
                )
        return dep
    
    def get_dep(self) -> Callable[[], Awaitable[TDataSchemaPublic]]:
        async def dep(
            service = Depends(self.service_dep)) -> TDataSchemaPublic:
            pass
        return dep
    
    def get_one_dep(self) -> Callable[[], Awaitable[TSchemaPublic]]:
        async def dep(
            service = Depends(self.service_dep),
            id: int = Path(..., examples=[1])) -> TSchemaPublic:
            data = await service.get(id)
            if not data:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Id has not found"
                )
            response = self.SchemaPublic.model_validate(data, from_attributes=True)
            return response
        return dep
        
    def create_one_dep(self) -> Callable[[], Awaitable[TSchemaPublic]]:
        SchemaBody = self.SchemaBody
        async def dep(
            body: SchemaBody,
            service: Service = Depends(self.service_dep)) -> TSchemaPublic:
            data = await service.create(body)
            if isinstance(data, str):
                raise HTTPException(
                    detail=data,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            d = body.model_dump()
            d["id"] = data
            if self.alert_func:
                await self.alert_func(d)
            response = self.SchemaPublic(**d)
            return response
        return dep
    
    def update_one_dep(self) -> Callable[[], Awaitable[TSchemaPublic]]:
        async def dep(
            service: Service = Depends(self.service_dep)) -> TSchemaPublic:
            pass
        return dep
    
    def delete_one_dep(self) -> Callable[[], Awaitable[TSchemaPublic]]:
        async def dep(
            service: Service = Depends(self.service_dep)) -> TSchemaPublic:
            pass
        return dep
    
    def set_cookie(
        self,
        response: Response,
        key: str,
        value: str,
        max_age: int) -> None:
        response.set_cookie(
            key=key,
            value=value,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=max_age
        )
        
    def websocket_token_dep(self) -> Callable[[], Awaitable[Union[str, dict]]]:
        async def dep(
            service: Service = Depends(self.service_dep),
            token: str = Query(..., examples=["adfadfadf"])
        ) -> Union[str, dict]:
                data = await service.validate_token(token)
                return data
        return dep
