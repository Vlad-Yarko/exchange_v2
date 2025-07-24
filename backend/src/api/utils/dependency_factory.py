from typing import Callable, Awaitable, Type, Optional, Union, Any
import uuid

from fastapi import Depends, HTTPException, status, Response, Path, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.utils.service import Service
from src.services.email import email_service
from src.services.phone_number import phone_number_service
from src.types.dependency_factory import TSchemaBody, TSchemaPublic, TDataSchemaPublic, TPhoneNumberBody
from src.enums.user import RoleEnum
from src.models import User


class DependencyFactory:
    def __init__(
        self,
        service_dep: Optional[Callable[[], Awaitable[Service]]] = None,
        SchemaBody: Optional[Type[TSchemaBody]] = None,
        SchemaPublic: Optional[Type[TSchemaPublic]] = None,
        DataSchemaPublic: Optional[Type[TDataSchemaPublic]] = None,
        PhoneNumberBody: Optional[Type[TPhoneNumberBody]] = None,
        alert_func: Optional[Callable[[], Awaitable]] = None
    ):
        self.service_dep = service_dep
        self.SchemaBody = SchemaBody
        self.SchemaPublic = SchemaPublic
        self.DataSchemaPublic = DataSchemaPublic
        self.PhoneNumberBody = PhoneNumberBody
        self.security = HTTPBearer()
        self.alert_func = alert_func
        self.email_service = email_service
        self.phone_number_service = phone_number_service
        self.email_schema = None
        self.phone_number_schema = None
        
    def check_for_exception(self, data: Union[dict, str, list, Any]) -> None:
        if isinstance(data, tuple):
            raise HTTPException(
                status_code=data[0],
                detail=data[1]
            )
            
    def verified_email_dep(self) -> Callable[[], Awaitable[bool]]:
        async def dep() -> bool:
            # self.email_schema
            # data = await self.email_service.is_verified_email(body.email)
            # check_for_exception(data)
            return True
        return dep
    
    def verified_phone_number_dep(self) -> Callable[[], Awaitable[bool]]:
        async def dep() -> bool:
            # self.phone_number_schema
            # if body.model_dump().get("phoneNumber"):
            #     data = await self.phone_number_service.is_verified_phone_number(body.phoneNumber)
            #     self.check_for_exception(data)
            return True
        return dep
    
    def id_dep(self) -> Callable[[], Awaitable[Union[uuid.UUID, int]]]:
        async def dep(
            id: int = Path(..., examples=[1], description="Unique identifier of an object. 💫", ge=1)
        ) -> Union[uuid.UUID, int]:
            return id
        return dep
    
    def page_dep(self) -> Callable[[], Awaitable[int]]:
        async def dep(
            page: Optional[int] = Query(None, examples=[1], description="Number of pagination page. 💫", ge=1)
        ) -> int:
            return page
        return dep
        
    def token_dep(self) -> Callable[[], Awaitable[Union[dict, User]]]:
        async def dep(
            service: Service = Depends(self.service_dep),
            authorization: HTTPAuthorizationCredentials = Depends(self.security)) -> Union[dict, User]:
            data = authorization.model_dump()
            try:
                if data.get("scheme") != "Bearer":
                    raise ValueError
                token = data["credentials"]
                d = await service.validate_token(token)
                self.check_for_exception(d)
                return d
            except (ValueError, KeyError):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authenticated"   
                )
        return dep
    
    def admin_dep(self) -> Callable[[], Awaitable[Union[dict, User]]]:
        async def dep(
            user: User = Depends(self.token_dep())) -> Union[dict, User]:
            if not user.role == RoleEnum.ADMIN.value:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authenticated. Admins-only"
                )
            return user
        return dep
    
    def get_dep(self) -> Callable[[], Awaitable[TDataSchemaPublic]]:
        async def dep(
            user: User = Depends(self.token_dep()),
            page: int = Depends(self.page_dep()),
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
            user: User = Depends(self.token_dep()),
            id: int = Depends(self.id_dep()),
            service: Service = Depends(self.service_dep),
            ) -> TSchemaPublic:
            data = await service.get_one(id)
            self.check_for_exception(data)
            response = self.SchemaPublic.model_validate(data, from_attributes=True)
            return response
        return dep
        
    def create_one_dep(self) -> Callable[[], Awaitable[TSchemaPublic]]:
        SchemaBody = self.SchemaBody
        async def dep(
            body: SchemaBody,
            admin: User = Depends(self.admin_dep()),
            service: Service = Depends(self.service_dep)) -> TSchemaPublic:
            data = await service.create_one(body.model_dump())
            self.check_for_exception(data)
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
            admin: User = Depends(self.admin_dep()),
            service: Service = Depends(self.service_dep),
            id: int = Depends(self.id_dep())) -> TSchemaPublic:
            data = await service.update_one(id, body.model_dump())
            self.check_for_exception(data)
            # response = self.SchemaPublic.model_validate(data, from_attributes=True)
            response = self.SchemaPublic(**data)
            return response
        return dep
    
    def delete_one_dep(self) -> Callable[[], Awaitable[TSchemaPublic]]:
        async def dep(
            admin: User = Depends(self.admin_dep()),
            service: Service = Depends(self.service_dep),
            id: int = Depends(self.id_dep())) -> TSchemaPublic:
            data = await service.delete_one(id)
            self.check_for_exception(data)
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
        
    def delete_cookie(
        self,
        response: Response,
        key: str) -> None:
        response.delete_cookie(key)
        
    def websocket_token_dep(self) -> Callable[[], Awaitable[Union[str, dict]]]:
        async def dep(
            service: Service = Depends(self.service_dep),
            token: str = Query(..., examples=["adfadfadf"])
        ) -> Union[str, dict]:
                data = await service.validate_token(token)
                return data
        return dep
