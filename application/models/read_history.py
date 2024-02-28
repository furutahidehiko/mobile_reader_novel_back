from sqlalchemy import Column,Integer,ForeignKey,UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column,relationship

from models.base import Base

class ReadHistory(Base):
    """既読テーブルのORM。"""

    __tablename__ = "read_history"
    __table_args__ = (UniqueConstraint('book_id', 'read_episode'),)

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False, unique=True)
    read_episode: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="既読した話数")

    # Bookとのone-to-oneの関係を定義
    book = relationship("Book", back_populates="read_history")
