from typing import Callable, Awaitable, Type, Optional, Union, Any
import uuid

from fastapi import Depends, HTTPException, status, Response, Path, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.utils.service import Service
from src.services.email import EmailService
from src.repositories import TelegramUserRepository, UserRepository
from src.services.phone_number import PhoneNumberService
from src.types.dependency_factory import TSchemaBody, TSchemaPublic, TDataSchemaPublic, TPhoneNumberBody, TEmailBody
from src.enums.user import RoleEnum
from src.models import User
from src.api.dependencies.db import DBSession


class DependencyFactory:
    def __init__(
        self,
        service_dep: Optional[Callable[[], Awaitable[Service]]] = None,
        SchemaBody: Optional[Type[TSchemaBody]] = None,
        SchemaPublic: Optional[Type[TSchemaPublic]] = None,
        DataSchemaPublic: Optional[Type[TDataSchemaPublic]] = None,
        PhoneNumberBody: Optional[Type[TPhoneNumberBody]] = None,
        EmailBody: Optional[Type[TEmailBody]] = None,
        alert_func: Optional[Callable[[], Awaitable]] = None
    ):
        self.service_dep = service_dep
        self.SchemaBody = SchemaBody
        self.SchemaPublic = SchemaPublic
        self.DataSchemaPublic = DataSchemaPublic
        self.PhoneNumberBody = PhoneNumberBody
        self.EmailBody = EmailBody
        self.security = HTTPBearer()
        self.alert_func = alert_func
        
    def email_service_dep(self) -> Callable[[], Awaitable[EmailService]]:
        async def dep(
            session: DBSession) -> EmailService:
            return EmailService(
                session=session,
                user_repo=UserRepository
            )
        return dep
        
    def phone_number_service_dep(self) -> Callable[[], Awaitable[PhoneNumberService]]:
        async def dep(
            session: DBSession) -> PhoneNumberService:
            return PhoneNumberService(
                session=session,
                telegram_user_repo=TelegramUserRepository,
                user_repo=UserRepository
            )
        return dep
        
    def check_for_exception(self, data: Union[dict, str, list, Any]) -> None:
        if isinstance(data, tuple):
            raise HTTPException(
                status_code=data[0],
                detail=data[1]
            )
            
    def verified_email_dep(self) -> Callable[[], Awaitable[bool]]:
        EmailBody = self.EmailBody
        async def dep(
            body: EmailBody,
            service: EmailService = Depends(self.email_service_dep())
            ) -> bool:
            email = body.model_dump().get("email")
            if email:
                data = await service.is_verified({"email": email})
                self.check_for_exception(data)
                if email != data.get("email"):
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Email is not verified"
                    )
            return True
        return dep
    
    def verified_phone_number_dep(self) -> Callable[[], Awaitable[bool]]:
        PhoneNumberBody = self.PhoneNumberBody
        async def dep(
                body: PhoneNumberBody,
                service: PhoneNumberService = Depends(self.phone_number_service_dep()),
                user: User = Depends(self.token_dep()),
            ) -> bool:
            phone_number = body.model_dump().get("phoneNumber")
            if phone_number:
                data = await service.is_verified(user.id, {"phoneNumber": phone_number})
                self.check_for_exception(data)
                if phone_number != data.get("phoneNumber"):
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail="Phone number is not verified"
                    )
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
                    detail="Access denied. Admins-only"
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
            secure=True, # True # False
            samesite="none", # none # lax
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
