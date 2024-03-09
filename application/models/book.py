"""このモジュールでは、小説情報を表現するためのデータベースモデルを提供します."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Book(Base):
    """小説情報のORM."""

    __tablename__ = "book"

    ncode: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, comment="小説コード"
    )

    # ReadHistoryとのone-to-oneの関係を定義
    read_history = relationship(
        "ReadHistory", back_populates="book", uselist=False
    )
