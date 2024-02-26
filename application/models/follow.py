from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship

from models.base import Base


class Follow(Base):
    """お気に入りテーブルのORM."""

    __tablename__ = "follow"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    is_follow = Column(Boolean, default=False, nullable=False)