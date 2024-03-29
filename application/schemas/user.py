"""ユーザ関連のスキーマ用モジュール."""

from enum import Enum

from pydantic import BaseModel, Field


class GrantType(str, Enum):
    """認証に使う情報の種類を表すEnumクラス.

    - PASSWORD: ID・passwordによる認証を行うという意味
    - REFRESH_TOKEN: refresh_tokenによる認証を行うという意味
    """

    PASSWORD: str = "password"
    REFRESH_TOKEN: str = "refresh_token"


class AuthUserModel(BaseModel):
    """トークンAPIで使用するバリデーションモデル."""

    user_id: str | None = Field(
        ...,
        title="メールアドレス",
        description="ユーザー自身が設定したメールアドレス",
        example="test01@example.com",
    )
    password: str | None = Field(
        ..., title="パスワード", description="パスワード", example="pass"
    )
    refresh_token: str | None = Field(
        ...,
        title="リフレッシュトークン",
        description="リフレッシュトークン",
        example="sdhjjhjhsasfak",
    )
    grant_type: str = Field(
        ..., title="認証方式", description="認証方式", example="password"
    )


class AuthUserResponse(BaseModel):
    """トークンAPIのレスポンス用モデル."""

    access_token: str = Field(
        title="アクセストークン",
        description="アクセストークン",
        example="eyJhbGciO5cCI6IkpXVCJ9.eyJzdWIiOiIxqxLYGqmuL1Pw",
    )
    refresh_token: str = Field(
        title="リフレッシュトークン",
        description="リフレッシュトークン",
        example="dsfhgfsfa,.fklsijashkhiafeyehjoszxcsa/j;w",
    )
