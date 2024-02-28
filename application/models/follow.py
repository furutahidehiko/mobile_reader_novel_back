from sqlalchemy import Column, Integer, Boolean, ForeignKey

from models.base import Base


class Follow(Base):
    """お気に入りテーブルのORM."""

    __tablename__ = "follow"

    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)