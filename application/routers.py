"""ルーター用モジュール."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import get_async_session
from domain.narou.main_text import get_main_text
from domain.narou.follow import post_follow,delete_follow
from models.novel import NovelResponse
from models.follow import FollowResponse


router = APIRouter()


@router.get(
    "/api/maintext",
    response_model=NovelResponse,
)
async def main_text(
    *,
    ncode: str,
    episode: int,
    async_session: AsyncSession = Depends(get_async_session),
):
    """小説取得APIのエンドポイント."""
    return get_main_text(ncode, episode)

@router.post(
    "/api/follow",
    response_model=FollowResponse,
    summary="お気に入り登録",
    description="指定されたNコードをお気に入り登録します。",
    tags=["お気に入り"]
)
async def post_follow_router(ncode: str, db: AsyncSession = Depends(get_async_session)):
    return await post_follow(db, ncode)

@router.delete(
    "/api/follow",
    response_model=FollowResponse,
    summary="お気に入り削除",
    description="指定されたNコードをお気に入り削除します。",
    tags=["お気に入り"]
)
async def delete_follow_router(ncode: str, db: AsyncSession = Depends(get_async_session)):
    return await delete_follow(db, ncode)
