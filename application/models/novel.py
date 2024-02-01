"""フロントへのレスポンス定義(小説本文データ)."""
from typing import List

from pydantic import BaseModel, Field


class NovelResponse(BaseModel):
    """小説本文データ.

    Parameters:
    ----------
    title : 小説のタイトル
    subtitle : エピソードタイトル
    text : 本文
    next : 次ページ有無
    prev : 前ページ有無.
    """

    title: str = Field(..., title="小説のタイトル")
    subtitle: str = Field(..., title="エピソードタイトル")
    text: List[str] = Field(..., title="本文", example="なろう小説です")
    next: bool = Field(False, title="次ページ有無", example="boolean")
    prev: bool = Field(False, title="前ページ有無", example="boolean")
