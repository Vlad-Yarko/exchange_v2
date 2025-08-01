from typing import Union

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from src.schemas import Authentication403
from src.schemas.user import *
from src.api.dependencies.user import (
    dependencies, 
    Users, 
    User, 
    CreatedUser, 
    UpdatedUser, 
    DeletedUser, 
    GoogleLoggedInUser, 
    LoggedInUser, 
    LoggedOutUser, 
    RefreshedToken
)


router = APIRouter(
    prefix='/users'
)


@router.get("",
            summary="Gets users. 💫 (Admins-only⚙️)",
            description="Gets **users** from database with their information via pagination. 💫",
            tags=["User_CRUDs💫"],
            response_model=UsersPublic,
            responses={
                403: {'model': Authentication403}
            })
async def get_users(data: Users):
    return data


@router.get("/one",
            summary="Gets user. 💫 (Protected🗝️)",
            description="Gets **user** from database with his information. 💫",
            tags=["User_CRUDs💫"],
            response_model=UserPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': GetUser422}
            })
async def get_user(data: User):
    return data


@router.post("",
            summary="Creates user. 💫",
            description="Creates **user** in database with his information. 💫",
            tags=["User_CRUDs💫"],
            response_model=UserPublic,
            responses={
                400: {'model': CreateUser400},
                422: {'model': CreateUser422}
            })
async def create_user(data: CreatedUser):
    return data


@router.put("",
            summary="Updates user. 💫 (Protected🗝️)",
            description="Updates **user** info in database. 💫",
            tags=["User_CRUDs💫"],
            response_model=UserPublic,
            responses={
                400: {'model': UpdateUser400},
                403: {'model': Authentication403},
                422: {'model': UpdateUser422}
            })
async def update_user(data: UpdatedUser):
    return data


@router.delete("/{id}",
            summary="Deletes user. 💫 (Admins-only⚙️)",
            description="Deletes **user** from database. 💫",
            tags=["User_CRUDs💫"],
            response_model=UserPublic,
            responses={
                403: {'model': Authentication403},
                422: {'model': DeleteUser422}
            })
async def delete_user(data: DeletedUser):
    return data


@router.get("/google/url",
            summary="Gets google redirect url. 💫",
            description="Gets **google** redirection url for oauth 2.0 authentication",
            tags=["Authentication💫"],
            response_class=RedirectResponse,
            responses={
                "400": {'model': GoogleUrl400}
            })
async def google_url_hand(data = Depends(dependencies.google_url_dep())):
    return data


@router.post("/google/callback",
            summary="Logs user in",
            description="**Logs** user in via oauth 2.0 protocol (google) and **issues** refresh token. 💫",
            tags=["Authentication💫"],
            response_model=CallbackGooglePublic,
            responses={
                400: {'model': GoogleCallback400},
                422: {'model': GoogleCallback422}
            })
async def google_callback_hand(data: GoogleLoggedInUser):
    return data



@router.post("/login",
            summary="Logs user in. 💫",
            description="**Logs** user in and **issues** refresh token. 💫",
            tags=["Authentication💫"],
            response_model=LoginUserPublic,
            responses={
                400: {'model': LoginUser400},
                422: {'model': LoginUser422}
            })
async def login_user(data: LoggedInUser):
    return data


@router.post("/logout",
            summary="Logs user out. 💫",
            description="**Logs** user out and **expires** refresh token. 💫",
            tags=["Authentication💫"],
            response_model=Union[UserPublic, LogoutUserPublic],
            responses={
                400: {'model': LogoutUser400}
            })
async def logout_user(data: LoggedOutUser):
    return data


@router.post("/refresh",
            summary="Issues access token. 💫",
            description="**Issues** access token and **refreshes** refresh token. 💫",
            tags=["Authentication💫"],
            response_model=RefreshPublic,
            responses={
                400: {'model': RefreshUser400}
            })
async def refresh_user(data: RefreshedToken):
    return data
