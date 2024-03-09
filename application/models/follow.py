"""このモジュールは、ユーザーのお気に入り（フォロー）情報を表すためのデータベースモデルを提供します."""
from sqlalchemy import Column, ForeignKey, Integer

from models.base import Base


class Follow(Base):
    """お気に入りテーブルのORM."""

    __tablename__ = "follow"

    book_id = Column(
        Integer, ForeignKey("book.id"), nullable=False, unique=True
    )
