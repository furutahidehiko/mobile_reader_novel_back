"""このモジュールは、SQLAlchemyを用いたデータベースモデル定義の基底クラスを提供します.

基底クラス Base は、非同期対応の SQLAlchemy の宣言的マッピングを行うための基礎構造を
定義します。
これにより、他のデータベースモデルクラスはこの基底クラスを継承して、
非同期操作を含むデータベースの操作が可能になります。
"""
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from passlib.context import CryptContext


class Base(AsyncAttrs, DeclarativeBase):
    """宣言的マッピングの基底クラス."""

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="ID"
    )

class PasswordMixin:
    """ハッシュ化したパスワードを設定する用のMixin."""

    _password: Mapped[str] = mapped_column("password", String(60))

    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def set_password(self, password):
        """パスワードをハッシュ化して設定."""
        self._password = PasswordMixin._pwd_context.hash(password)

    def check_password(self, password):
        """設定したパスワードと一致するかどうかを検証."""
        return PasswordMixin._pwd_context.verify(password, self._password)