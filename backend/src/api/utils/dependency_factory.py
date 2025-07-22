from typing import Callable, Awaitable, Type, Optional, Union, Any

from fastapi import Depends, HTTPException, status, Response, Path, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.utils.service import Service
from src.services.email import email_service
from src.types.dependency_factory import TSchemaBody, TSchemaPublic, TDataSchemaPublic


def check_for_exception(data: Any) -> None:
    if isinstance(data, tuple):
        raise HTTPException(
            status_code=data[0],
            detail=data[1]
        )


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
        self.email_service = email_service
            
    def verified_email_dep(self) -> Callable[[], Awaitable[bool]]:
        SchemaBody = self.SchemaBody
        async def dep(
            body: SchemaBody) -> bool:
            # data = await self.email_service.is_verified_email(body.email)
            # check_for_exception(data)
            return True
        return dep
        
    def token_dep(self) -> Callable[[], Awaitable[dict]]:
        async def dep(
            service: Service = Depends(self.service_dep),
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
            token: str = Depends(self.token_dep()),
            page: Optional[int] = Query(None, examples=[1], description="Number of pagination page. 💫", ge=1),
            service: Service = Depends(self.service_dep)) -> TDataSchemaPublic:
            data = await service.get(page)
            d = [
                self.SchemaPublic.model_validate(item, from_attributes=True)
                for item in data.get('data')
            ]
            data["data"] = d
            response = self.DataSchemaPublic(**data)
            return response
        return dep
    
    def get_one_dep(self) -> Callable[[], Awaitable[TSchemaPublic]]:
        async def dep(
            token: str = Depends(self.token_dep()),
            service: Service = Depends(self.service_dep),
            id: int = Path(..., examples=[1], description="Unique identifier of an object. 💫", ge=1)) -> TSchemaPublic:
            data = await service.get_one(id)
            check_for_exception(data)
            response = self.SchemaPublic.model_validate(data, from_attributes=True)
            return response
        return dep
        
    def create_one_dep(self) -> Callable[[], Awaitable[TSchemaPublic]]:
        SchemaBody = self.SchemaBody
        async def dep(
            body: SchemaBody,
            token: str = Depends(self.token_dep()),
            service: Service = Depends(self.service_dep)) -> TSchemaPublic:
            data = await service.create_one(body.model_dump())
            check_for_exception(data)
            # d = body.model_dump()
            # d["id"] = data
            # if self.alert_func:
            #     await self.alert_func(d)
            # response = self.SchemaPublic.model_validate(data)
            response = self.SchemaPublic(**data)
            return response
        return dep
    
    def update_one_dep(self) -> Callable[[], Awaitable[TSchemaPublic]]:
        SchemaBody = self.SchemaBody
        async def dep(
            body: SchemaBody,
            token: str = Depends(self.token_dep()),
            service: Service = Depends(self.service_dep),
            id: int = Path(..., examples=[1], description="Unique identifier of an object. 💫", ge=1)) -> TSchemaPublic:
            data = await service.update_one(id, body.model_dump())
            check_for_exception(data)
            # response = self.SchemaPublic.model_validate(data, from_attributes=True)
            response = self.SchemaPublic(**data)
            return response
        return dep
    
    def delete_one_dep(self) -> Callable[[], Awaitable[TSchemaPublic]]:
        async def dep(
            token: str = Depends(self.token_dep()),
            service: Service = Depends(self.service_dep),
            id: int = Path(..., examples=[1], description="Unique identifier of an object. 💫", ge=1)) -> TSchemaPublic:
            data = await service.delete_one(id)
            check_for_exception(data)
            # response = self.SchemaPublic.model_validate(data, from_attributes=True)
            response = self.SchemaPublic(**data)
            return response
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
