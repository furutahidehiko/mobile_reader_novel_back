"""ルーター用モジュール."""


from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.config import get_async_session

from domain.narou.main_text import get_main_text
from models.novel import NovelResponse

router = APIRouter()


@router.get(
    "/api/maintext",
    response_model=NovelResponse,
)
async def main_text(*, ncode: str, episode: int, async_session: AsyncSession = Depends(get_async_session),):
    """小説取得APIのエンドポイント."""
    return  await get_main_text(ncode, episode, async_session)
