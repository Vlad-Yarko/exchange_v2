from fastapi import APIRouter

from src.schemas import Authentication403
from src.schemas.user import UserPublic, UsersPublic, GetUser422, CreateUser422, UpdateUser422, DeleteUser422
from src.api.dependencies.user import Users, User, CreatedUser, UpdatedUser, DeletedUser


router = APIRouter(
    prefix='/users'
)


@router.get("",
            summary="Gets users. 💫",
            description="Gets **users** from database with their information via pagination. 💫",
            tags=["User_CRUDs💫"],
            response_model=UsersPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_crypto(data: Users):
    return data


@router.get("/{id}",
            summary="Gets user. 💫",
            description="Gets **user** from database with its information. 💫",
            tags=["User_CRUDs💫"],
            response_model=UserPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': GetUser422}
            })
async def get_user(data: User):
    return data


@router.post("",
            summary="Creates crypto currency. 💫",
            description="Creates **crypto** currency in database with its information. 💫",
            tags=["User_CRUDs💫"],
            response_model=UserPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': CreateUser422}
            })
async def get_user(data: CreatedUser):
    return data


@router.put("/{id}",
            summary="Updates crypto currency. 💫",
            description="Updates **crypto** currency in database. 💫",
            tags=["User_CRUDs💫"],
            response_model=UserPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': UpdateUser422}
            })
async def get_user(data: UpdatedUser):
    return data


@router.delete("/{id}",
            summary="Deletes crypto currency. 💫",
            description="Deletes **crypto** currency from database. 💫",
            tags=["User_CRUDs💫"],
            response_model=UserPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': DeleteUser422}
            })
async def get_user(data: DeletedUser):
    return data
