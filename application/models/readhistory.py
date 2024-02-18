"""ReadHistoryテーブルのORM."""

from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class ReadHistory(Base):
    """本テーブルのORM."""

    __tablename__ = "readhistory"

    ncode: Mapped[str] = mapped_column(comment="小説コード", nullable=False)
    read_episode: Mapped[int] = mapped_column(comment="既読した話数", nullable=False)

    def __str__(self):
        """idと小説コードを設定."""
        return f"ReadHistory_{self.id}:{self.ncode}"
