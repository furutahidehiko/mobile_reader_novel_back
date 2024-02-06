"""ルーター用モジュール."""


from fastapi import APIRouter

from domain.narou.main_text import get_main_text
from models.novel import NovelResponse

router = APIRouter()


@router.get(
    "/api/maintext",
    response_model=NovelResponse,
)
def main_text(*, ncode: str, episode: int):
    """小説取得APIのエンドポイント."""
    return get_main_text(ncode, episode)
