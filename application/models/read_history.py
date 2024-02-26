from sqlalchemy import Column,Integer,ForeignKey,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base

class ReadHistory(Base):
    """既読テーブルのORM."""

    __tablename__ = "read_history"
    __table_args__ = (UniqueConstraint('book_id', 'read_episode'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    read_episode: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="既読した話数")
