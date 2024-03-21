"""環境変数の読み込み."""

from typing import List

from pydantic_settings import BaseSettings


class VariableSettings(BaseSettings):
    """環境変数を取得する設定クラス."""

    DEBUG: bool = True
    """DEBUGモードで起動（True）"""

    TRUSTED_ORIGINS: List[str] = ["http://localhost:3000"]
    """CORSで許可するオリジン"""
    # CSRF_COOKIE_DOMAIN: str = ""
    """CSRFCookieを設定するときに使用されるドメイン"""


class PostgresSettings(BaseSettings):
    """Postgres関連の設定クラス."""

    POSTGRES_NAME: str
    """PostgreSQLのデータベース名"""
    POSTGRES_USER: str
    """PostgreSQLのユーザ名"""
    POSTGRES_PASSWORD: str
    """PostgreSQLのパスワード"""
    POSTGRES_HOST: str
    """PostgreSQLのホスト名"""
    POSTGRES_PORT: int
    """PostgreSQLのポート番号"""


class JWTSettings(BaseSettings):
    """JWT関連の設定クラス."""

    JWT_SECRET_ACCESS_KEY: str
    """シークレットキー

    下記コマンドで生成可能
    $ openssl rand -hex 32
    """

    JWT_SECRET_REFRESH_KEY: str
    """シークレットキー(リフレッシュトークン用)

    下記コマンドで生成可能
    $ openssl rand -hex 64
    """

    JWT_ALGORITHM: str = "HS256"
    """JWTトークンの署名に使用するアルゴリズム"""

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 9
    """アクセストークンの有効期限(時間)"""

    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 90
    """リフレッシュトークンの有効期限(日)"""


settings = VariableSettings()
"""環境変数"""

postgres_settings = PostgresSettings()
"""postgres関連の環境変数"""

jwt_settings = JWTSettings()
"""JWT関連の環境変数"""
