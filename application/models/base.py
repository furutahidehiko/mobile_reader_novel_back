"""このモジュールは、SQLAlchemyを用いたデータベースモデル定義の基底クラスを提供します。.

基底クラス Base は、非同期対応の SQLAlchemy の宣言的マッピングを行うための基礎構造を
定義します。
これにより、他のデータベースモデルクラスはこの基底クラスを継承して、
非同期操作を含むデータベースの操作が可能になります。
"""
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """宣言的マッピングの基底クラス."""

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="ID"
    )
