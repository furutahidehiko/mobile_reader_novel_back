from sqlalchemy import String,Integer
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base



class ReadHistory(Base):
    """既読テーブルのORM."""

    __tablename__ = "read_history"

    ncode: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, comment="小説コード")
    read_episode: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="既読した話数")
