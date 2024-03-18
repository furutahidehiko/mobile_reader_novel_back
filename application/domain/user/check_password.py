"""このモジュールは、トークン認証の機能を提供します."""
from typing import Optional
from domain.user.token import create_token

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user import User
from schemas.user import AuthUserModel, AuthUserResponse


async def check_password(
    auth_data: AuthUserModel,
    async_session: AsyncSession,
) -> AuthUserResponse:
    """ログイン認証を行い、アクセストークン及びリフレッシュトークンを生成する関数.

    Parameters:
    - auth_data (AuthUserModel): 認証するためユーザー情報。
    - async_session (AsyncSession): DBとのセッション。

    Returns:
    - create_tokenのレスポンス
    """

    def authenticate_user(user: Optional[User]):
        if user is None:
            return False
        return user.check_password(auth_data.password)
    
    
    result = await async_session.execute(
        select(User).where(User.id == int(auth_data.id))
    )

    user = result.scalar_one_or_none()

    user_id: int = user.id

    if not authenticate_user(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="idかpasswordが異なります.",
        )
    
    return  await create_token(user_id)
