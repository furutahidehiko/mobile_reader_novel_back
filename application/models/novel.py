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
    text: List[str] = Field(..., title="本文")
    next: bool = Field(False, title="次ページ有無")
    prev: bool = Field(False, title="前ページ有無")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "異世界に行ったので手に職を持って生き延びます",
                    "subtitle": "１．真っ白い世界で",
                    "text": [
                        "",
                        "",
                        "",
                        "〔お前たちを異世界に転移させる。どのように転移するかを自分で選ぶといい、時間は３時間だ〕",
                        "",
                        " 突然、頭の中に声ではない何かが響いた。",
                        "驚いて、きょろきょろと視線を周囲に向け、様子をうかがう。",
                    ],
                    "next": True,
                    "prev": False,
                }
            ]
        }
    }
