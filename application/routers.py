"""ルーター用モジュール."""

from schemas.user import AuthUserModel, AuthUserResponse
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import get_async_session
from domain.narou.main_text import get_main_text
from domain.narou.novel_info import get_novel_info
from domain.user.token import auth_token
from schemas.novel import NovelInfoResponse, NovelResponse

router = APIRouter()


@router.get(
    "/api/maintext",
    response_model=NovelResponse,
    summary="本文取得API",
    description="指定されたNコードとエピソード番号から小説本文に関する情報を取得します。",
    tags=["小説表示画面"]
)
async def main_text(
    *,
    ncode: str,
    episode: int,
    async_session: AsyncSession = Depends(get_async_session),
):
    """小説取得APIのエンドポイント."""
    return await get_main_text(ncode, episode, async_session)

@router.get(
    "/api/novelinfo",
    response_model=NovelInfoResponse,
    summary="小説情報取得API",
    description="指定されたNコードから目次ページに関する情報を取得します。",
    tags=["目次画面"]
)
async def novel_info(ncode: str, db: AsyncSession = Depends(get_async_session)):
    return await get_novel_info(db, ncode)

@router.post(
    "/token/",
    response_model=AuthUserResponse,
    status_code=status.HTTP_200_OK,
    summary="トークン認証API",
    description="ID/パスワードorリフレッシュトークンによる認証を行い新たなアクセストークンとリフレッシュトークンを発行します。",
    tags=["token"],
)
async def auth_token(
    auth_data: AuthUserModel,
    async_session: AsyncSession = Depends(get_async_session),
):
    return await auth_token(auth_data=auth_data,async_session=async_session)
