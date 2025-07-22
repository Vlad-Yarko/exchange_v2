from typing import Annotated, Callable, Awaitable, Optional

from fastapi import Depends, HTTPException, status, Cookie

from src.api.utils.dependency_factory import DependencyFactory, check_for_exception
from src.api.dependencies.db import DBSession
from src.repositories import UserRepository
from src.services import UserService
from src.schemas.user import UserBody, UserPublic, UsersPublic, LoginUserBody, LoginUserPublic, RefreshPublic


async def service_dep(session: DBSession) -> UserService:
    return UserService(
        session=session,
        user_repo=UserRepository
    )


class UserDependencyFactory(DependencyFactory):
    def __init__(self):
        super().__init__(
            service_dep=service_dep,
            SchemaBody=UserBody,
            SchemaPublic=UserPublic,
            DataSchemaPublic=UsersPublic
        )
        
    def get_one_dep(self) -> Callable[[], Awaitable[UserPublic]]:
        async def dep(
            token: str = Depends(self.token_dep()),
            service: UserService = Depends(self.service_dep)) -> UserPublic:
            pass
        return dep
        
    def create_one_dep(self) -> Callable[[], Awaitable[UserPublic]]:
        async def dep(
            body: UserBody,
            service: UserService = Depends(self.service_dep),
            email: bool = Depends(self.verified_email_dep())) -> UserPublic:
            data = await service.create_one(body.model_dump())
            check_for_exception(data)
            response = UserPublic(**data)
            return response
        return dep
    
    def update_one_dep(self) -> Callable[[], Awaitable[UserPublic]]:
        async def dep(
            body: UserBody,
            token: str = Depends(self.token_dep()),
            service: UserService = Depends(self.service_dep),
            email: bool = Depends(self.verified_email_dep())) -> UserPublic:
            data = await service.update_one(body.model_dump())
            check_for_exception(data)
            response = UserPublic(**data)
            return response
        return dep
    
    def login_user_dep(self) -> Callable[[], Awaitable[LoginUserPublic]]:
        async def dep(
            body: LoginUserBody,
            service: UserService = Depends(self.service_dep),
            refreshToken: Optional[str] = Cookie(None, examples=[None], description="Refresh token id. (You do not need to pass it). 💫")) -> LoginUserPublic:
            if refreshToken:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User is authenticated. Refresh token has found"
                )
            data = await service.login_user(body.model_dump())
            check_for_exception(data)
            response = LoginUserPublic(**data)
            return response
        return dep
    
    def refresh_user_dep(self) -> Callable[[], Awaitable[RefreshPublic]]:
        async def dep(
            service: UserService = Depends(self.service_dep),
            refreshToken: Optional[str] = Cookie(None, examples=[None], description="Refresh token id. (You do not need to pass it). 💫")) -> RefreshPublic:
            if not refreshToken:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User is not authenticated. Refresh token has not found"
                )
            data = await service.refresh_user()
            check_for_exception(data)
            response = RefreshPublic(**data)
            return response
        return dep


dependencies = UserDependencyFactory()


# CRUDs
Users = Annotated[UsersPublic, Depends(dependencies.get_dep())]
User = Annotated[UserPublic, Depends(dependencies.get_one_dep())]
CreatedUser = Annotated[UserPublic, Depends(dependencies.create_one_dep())]
UpdatedUser = Annotated[UserPublic, Depends(dependencies.update_one_dep())]
DeletedUser = Annotated[UserPublic, Depends(dependencies.delete_one_dep())]

# Authentication
LoggedInUser = Annotated[UsersPublic, Depends(dependencies.login_user_dep())]
RefreshedToken = Annotated[RefreshPublic, Depends(dependencies.refresh_user_dep())]
