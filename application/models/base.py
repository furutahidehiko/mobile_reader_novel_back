"""このモジュールは、SQLAlchemyを用いたデータベースモデル定義の基底クラスを提供します.

基底クラス Base は、非同期対応の SQLAlchemy の宣言的マッピングを行うための基礎構造を
定義します。
これにより、他のデータベースモデルクラスはこの基底クラスを継承して、
非同期操作を含むデータベースの操作が可能になります。
"""
import bcrypt
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """宣言的マッピングの基底クラス."""

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, comment="ID"
    )


class PasswordMixin:
    """ハッシュ化したパスワードを設定する用のMixin."""

    _password: Mapped[str] = mapped_column("password", String(60))

    def set_password(self, password):
        """パスワードをハッシュ化して設定."""
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        self._password = bcrypt.hashpw(password=pwd_bytes, salt=salt)

    def check_password(self, password):
        """設定したパスワードと一致するかどうかを検証."""
        input_password_hash = password.encode("utf-8")
        hashed_password = self._password.encode("utf-8")
        return bcrypt.checkpw(input_password_hash, hashed_password)
