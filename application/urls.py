"""fetch用のURL."""
from enum import Enum
from urllib.parse import urljoin


class Url(Enum):
    """なろう小説のURL.

    Parameters
    ----------
    API_URL : なろうAPIのエンドポイント
    NOVEL_URL : スクレイピング用(なろう小説)

    """

    API_URL = "https://api.syosetu.com/novelapi/api/"
    NOVEL_URL = "https://ncode.syosetu.com/"

    def join(self, *path_segments):
        """URLの結合を行う.

        Parameters
        ----------
        *path_segments : tuple
            ncodeやepisode.

        Returns:
        -------
        base_url
            fetch用urlを返す
        """
        base_url = self.value
        for url in path_segments:
            base_url = f"{urljoin(base_url, url)}/"
        return base_url
