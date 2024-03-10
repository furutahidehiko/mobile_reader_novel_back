"""CustomerテーブルのORM."""


from models.base import Base, PasswordMixin


class User(Base, PasswordMixin):
    """ユーザーテーブルのORM."""

    __tablename__ = "user"
