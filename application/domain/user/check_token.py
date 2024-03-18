"""このモジュールは、トークン認証の機能を提供します."""

from domain.user.token import create_token
from fastapi import HTTPException, status
from jose import JWTError, jwt

from config.environment import jwt_settings
from models.user import User
from schemas.user import AuthUserModel, AuthUserResponse

import json


async def check_token(
    auth_data: AuthUserModel,
) -> AuthUserResponse:
    """ログイン認証を行い、アクセストークン及びリフレッシュトークンを生成する関数.

    Parameters:
    - auth_data (AuthUserModel): 認証するためのユーザー情報。

    Returns:
    - AuthUserResponse: アクセストークン及びリフレッシュトークン。
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            auth_data.refresh_token,
            jwt_settings.JWT_SECRET_KEY,
            algorithms=jwt_settings.JWT_ALGORITHM,
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    response_token = await create_token(int(user_id))
    return response_token
