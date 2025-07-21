from typing import Annotated, Callable, Awaitable

from fastapi import Depends

from src.api.utils.dependency_factory import DependencyFactory, check_for_exception
from src.api.dependencies.db import DBSession
from src.repositories import UserRepository
from src.services import UserService
from src.schemas.user import UserBody, UserPublic, UsersPublic


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
        
    def create_one_dep(self) -> Callable[[], Awaitable[UserPublic]]:
        async def dep(
            body: UserBody,
            service: UserService = Depends(self.service),
            email: bool = Depends(self.verified_email_dep())) -> UserPublic:
            data = await service.create_one(body.model_dump())
            check_for_exception(data)
            response = UserPublic(**data)
            return response
        return dep
    
    def update_one_dep(self) -> Callable[[], Awaitable[UserPublic]]:
        async def dep(
            body: UserBody,
            service: UserService = Depends(self.service),
            email: bool = Depends(self.verified_email_dep())) -> UserPublic:
            data = await service.update_one(body.model_dump())
            check_for_exception(data)
            response = UserPublic(**data)
            return response
        return dep


dependencies = UserDependencyFactory()


# CRUDs
Users = Annotated[UsersPublic, Depends(dependencies.get_dep())]
User = Annotated[UserPublic, Depends(dependencies.get_one_dep())]
CreatedUser = Annotated[UserPublic, Depends(dependencies.create_one_dep())]
UpdatedUser = Annotated[UserPublic, Depends(dependencies.update_one_dep())]
DeletedUser = Annotated[UserPublic, Depends(dependencies.delete_one_dep())]
