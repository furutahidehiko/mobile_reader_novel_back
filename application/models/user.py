"""CustomerテーブルのORM."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base, PasswordMixin


class User(Base, PasswordMixin):
    """ユーザーテーブルのORM."""

    __tablename__ = "user"

    email: Mapped[str] = mapped_column(
        String(254), nullable=False, unique=True, comment="メールアドレス"
    )
