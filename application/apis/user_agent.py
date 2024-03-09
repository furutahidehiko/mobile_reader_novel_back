"""このファイルでは、UserAgentManagerクラスを定義しています.

UserAgentManagerクラスは、fake_useragentライブラリを使用して、
ランダムなユーザーエージェント文字列を生成する機能を提供します.
"""

from fake_useragent import UserAgent


class UserAgentManager:
    """ランダムなユーザーエージェント文字列を生成するクラス.

    fake_useragentライブラリを使用して、さまざまなブラウザからのリクエストを模倣する
    ランダムなユーザーエージェント文字列を生成します。
    """

    def __init__(self):
        """UserAgentManagerの初期化を行います."""
        self.ua = UserAgent()

    def get_random_user_headers(self):
        """ランダムなユーザーエージェントのヘッダーを返します.

        Returns:
            dict: ヘッダー情報を含む辞書。
                キーは"User-Agent"、値はランダムなユーザーエージェント文字列。
        """
        return {"User-Agent": self.ua.random}
