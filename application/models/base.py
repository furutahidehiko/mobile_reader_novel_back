from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """宣言的マッピングの基底クラス."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment="ID")