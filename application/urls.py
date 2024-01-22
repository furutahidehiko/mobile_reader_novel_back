"""fetch用のURL."""

from enum import Enum


class Url(Enum):
    """なろう小説のURL.

    Parameters
    ----------
    API_URL : なろうAPIのエンドポイント
    NOVEL_URL : スクレイピング用(なろう小説)

    """

    API_URL = "http://api.syosetu.com/novelapi/api/"
    NOVEL_URL = "https://ncode.syosetu.com/"
