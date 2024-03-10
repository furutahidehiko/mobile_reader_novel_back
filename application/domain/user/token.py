"""このモジュールは、トークン認証の機能を提供します."""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from config.config import get_async_session
from config.environment import jwt_settings
from models.user import User
from schemas.user import AuthUserModel, AuthUserResponse


async def auth_token(
    auth_data: AuthUserModel,
    async_session: AsyncSession = Depends(get_async_session),
) -> AuthUserResponse:
    """ログイン認証を行い、アクセストークン及びリフレッシュトークンを生成する関数.

    Parameters:
    - auth_data (AuthUserModel): 認証するためユーザー情報。
    - async_session (AsyncSession): DBとのセッション。

    Returns:
    - AuthUserResponse: アクセストークン及びリフレッシュトークン。
    """

    def authenticate_user(user: Optional[User]):
        if user is None:
            return False
        return user.check_password(auth_data.password)

    result = await async_session.execute(
        select(User).where(User.id == auth_data.id)
    )
    user = result.scalar_one_or_none()
    if not authenticate_user(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="idかpasswordが異なります.",
        )
    min = timedelta(minutes=jwt_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    month = timedelta(days=jwt_settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + min
    refresh_expire = datetime.utcnow() + month
    access_token = jwt.encode(
        {"sub": user.id, "exp": expire},
        jwt_settings.JWT_SECRET_KEY,
        algorithm=jwt_settings.JWT_ALGORITHM,
    )
    refresh_token = jwt.encode(
        {"sub": user.id, "exp": refresh_expire},
        jwt_settings.JWT_SECRET_KEY,
        algorithm=jwt_settings.JWT_ALGORITHM,
    )
    return AuthUserResponse(
        access_token=access_token, refresh_token=refresh_token
    )
