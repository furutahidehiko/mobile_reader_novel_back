"""ルーター用モジュール."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import get_async_session
from domain.narou.main_text import get_main_text
from domain.narou.novel_info import get_novel_info
from schemas.novel import NovelInfoResponse, NovelResponse

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
    return await get_main_text(ncode, episode, async_session)

@router.get(
    "/api/novelinfo",
    response_model=NovelInfoResponse,
    summary="目次情報を取得",
    description="指定されたNコードから目次ページに関する情報を取得します。",
    tags=["目次画面"]
)
async def novel_info(ncode: str, db: AsyncSession = Depends(get_async_session)):
    return await get_novel_info(db, ncode)
