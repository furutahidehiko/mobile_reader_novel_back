"""このモジュールは、トークン認証の機能を提供します."""
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from config.environment import jwt_settings
from crud import get_user
from domain.user.token import create_token
from models.user import User
from schemas.user import AuthUserResponse


async def auth_password(
    email: str,
    password: str,
    async_session: AsyncSession,
) -> AuthUserResponse:
    """id/passwordによる認証を行う関数.

    Parameters:
    - auth_data (AuthUserModel): 認証するためユーザー情報。
    - async_session (AsyncSession): DBとのセッション。

    Returns:
    - create_tokenのレスポンス
    """

    def authenticate_user(user: Optional[User]):
        if user is None:
            return False
        return user.check_password(password)

    user = await get_user(async_session, email)

    if not authenticate_user(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "bad_request",
                "error_description": "メールアドレスかpasswordが異なります",
            },
        )

    return await create_token(user.id)


async def auth_token(refresh_token: str) -> AuthUserResponse:
    """リフレッシュトークンによる認証を行う関数.

    Parameters:
    - auth_data (AuthUserModel): 認証するためのユーザー情報。

    Returns:
    - AuthUserResponse: アクセストークン及びリフレッシュトークン。
    """
    try:
        payload = jwt.decode(
            refresh_token,
            jwt_settings.JWT_SECRET_REFRESH_KEY,
            algorithms=jwt_settings.JWT_ALGORITHM,
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "error": "unknown_user",
                    "error_description": "不明なユーザーです",
                },
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "invalid_token",
                "error_description": "アクセストークンの有効期限切れです。",
            },
        )

    return await create_token(str(user_id))
