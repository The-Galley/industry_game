from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Response
from fastapi.exceptions import HTTPException

from industry_game.utils.exceptions import UserWithUsernameAlreadExistsException
from industry_game.utils.http.auth.jwt import (
    AUTH_COOKIE,
    MAYBE_AUTH,
    REQUIRE_ADMIN_AUTH,
    REQUIRE_AUTH,
)
from industry_game.utils.http.models import StatusResponse
from industry_game.utils.overrides import (
    GetLoginProvider,
    GetUserStorage,
)
from industry_game.utils.users.base import (
    AuthToken,
    AuthUser,
    AuthUserModel,
    RegisterPlayerModel,
    UserType,
)
from industry_game.utils.users.models import FullUserModel, UserPaginationModel
from industry_game.utils.users.providers import LoginProvider
from industry_game.utils.users.storage import UserStorage

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/", dependencies=[Depends(REQUIRE_ADMIN_AUTH)])
async def list_users(
    page: int = Query(default=1, ge=1, title="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, title="Page size"),
    user_storage: UserStorage = Depends(GetUserStorage),
) -> UserPaginationModel:
    return await user_storage.pagination(
        page=page,
        page_size=page_size,
    )


@router.get(
    "/{user_id}/",
    response_model=FullUserModel,
    responses={
        HTTPStatus.NOT_FOUND: {
            "model": StatusResponse,
            "description": "Player not found",
        }
    },
)
async def read_user(
    user_id: int,
    auth_user: AuthUser = Depends(REQUIRE_AUTH),
    user_storage: UserStorage = Depends(GetUserStorage),
) -> FullUserModel:
    if auth_user.type != UserType.ADMIN and auth_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Forbidden",
        )
    user = await user_storage.read_by_id(user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )
    return user


@router.post(
    "/login/",
    responses={
        HTTPStatus.UNAUTHORIZED: {
            "model": StatusResponse,
            "description": "Wrong username or password",
        },
        HTTPStatus.CONFLICT: {
            "model": StatusResponse,
            "description": "You are already logged in",
        },
    },
)
async def login(
    user: AuthUserModel,
    response: Response,
    login_provider: LoginProvider = Depends(GetLoginProvider),
    auth_user: AuthUser | None = Depends(MAYBE_AUTH),
) -> AuthToken:
    if auth_user is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="You are already logged in",
        )
    auth_token = await login_provider.login(user)
    if auth_token is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Wrong username or password",
        )
    response.set_cookie(AUTH_COOKIE, auth_token.token)
    return auth_token


@router.post(
    "/register/",
    status_code=201,
    responses={
        HTTPStatus.BAD_REQUEST: {
            "model": StatusResponse,
            "description": "User with that username already exists",
        },
        HTTPStatus.CONFLICT: {
            "model": StatusResponse,
            "description": "You are already logged in",
        },
    },
)
async def register_player(
    new_player: RegisterPlayerModel,
    response: Response,
    login_provider: LoginProvider = Depends(GetLoginProvider),
    auth_user: AuthUser | None = Depends(MAYBE_AUTH),
) -> AuthToken:
    if auth_user is not None:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="You are already logged in",
        )
    try:
        auth_token = await login_provider.register_player(player=new_player)
    except UserWithUsernameAlreadExistsException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="User with that username already exists",
        )
    response.set_cookie(AUTH_COOKIE, auth_token.token)
    return auth_token
