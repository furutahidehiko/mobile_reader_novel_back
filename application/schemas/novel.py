"""フロントへのレスポンス定義(小説本文データ)."""
from typing import List

from pydantic import BaseModel, Field


class NovelResponse(BaseModel):
    """小説本文データ.

    Parameters:
    ----------
    title : 小説のタイトル
    sub_title : エピソードタイトル
    main_text : 本文
    next : 次ページ有無
    prev : 前ページ有無.
    """

    title: str = Field(..., title="小説のタイトル")
    sub_title: str = Field(..., title="エピソードタイトル")
    main_text: List[str] = Field(..., title="本文")
    prev: bool = Field(False, title="前ページ有無")
    next: bool = Field(False, title="次ページ有無")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "異世界に行ったので手に職を持って生き延びます",
                    "sub_title": "１．真っ白い世界で",
                    "main_text": [
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


class Chapter(BaseModel):
    """目次情報.

    Parameters:
    ----------
    chapter_title : 章題
    sub_titles : 小説のサブタイトル
    """

    chapter_title: str = Field(..., title="章題")
    sub_titles: List[str] = Field(..., title="小説のサブタイトル")


class NovelInfoResponse(BaseModel):
    """小説情報.

    Parameters:
    ----------
    title : 小説名
    author : 作者名
    episode_count : 全話数
    release_date : 公開日
    tag : 小説のタグ
    summary : あらすじ
    category : 大ジャンル
    sub_category : ジャンル
    updated_at : 作品の最終更新日
    read_episode : 既読した話数
    chapters : 章
    is_follow : お気に入り登録してるかどうか
    """

    title: str = Field(..., title="小説名")
    author: str = Field(..., title="作者名")
    episode_count: int = Field(..., title="全話数")
    release_date: str = Field(..., title="公開日")
    tag: List[str] = Field(..., title="小説のタグ")
    summary: str = Field(..., title="あらすじ")
    category: str = Field(..., title="大ジャンル")
    sub_category: str = Field(..., title="ジャンル")
    updated_at: str = Field(..., title="作品の最終更新日")
    read_episode: int = Field(..., title="既読した話数")
    chapters: List[Chapter] = Field(..., title="章")
    is_follow: bool = Field(..., title="お気に入り登録してるかどうか")

    class Config:
        """Pydanticモデルの設定クラス.

        json_schema_extra: スキーマの例を定義します。
                        この例はAPIのドキュメントで使用され、
                        APIの使用方法を理解しやすくするために役立ちます。
        """

        json_schema_extra = {
            "example": {
                "title": "異世界冒険記",
                "author": "山田太郎",
                "episode_count": 50,
                "release_date": "2023-01-01",
                "tag": ["ファンタジー", "冒険", "魔法"],
                "summary": "異世界に転生した主人公が冒険を繰り広げる物語。",
                "category": "ファンタジー",
                "sub_category": "異世界冒険",
                "updated_at": "2023-12-31",
                "read_episode": 20,
                "chapters": [
                    {
                        "chapter_title": "序章",
                        "sub_titles": ["第一話：異世界への扉", "第二話：新たなる出会い"],
                    }
                ],
                "is_follow": True,
            }
        }
