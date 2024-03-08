"""このモジュールは、小説家になろうAPIから取得したデータを扱うためのクラスとデータ構造を定義しています。."""

from dataclasses import dataclass
from typing import Any, Dict, Optional

from requests.models import Response


@dataclass
class Count:
    """検索ヒット数."""

    allcount: int = 0


@dataclass
class NovelData:
    """小説情報."""

    title: str = ""
    general_all_no: int = 0
    writer: str = ""
    general_firstup: str = ""
    keyword: str = ""
    story: str = ""
    biggenre: int = 0
    genre: int = 0
    general_lastup: str = ""


class NarouData:
    """なろうの小説APIから取得したデータを整形するクラス。."""

    def __init__(self, response: Response):
        """NarouDataクラスのコンストラクタ。.

        引数:
            response (Response): なろうAPIからのレスポンス。

        処理:
            レスポンスから必要なデータを抽出し、CountとNovelDataのインスタンスを生成する。
            エラーが発生した場合はメッセージを表示し、属性をNoneに設定する。
        """
        self.count: Optional[Count] = None
        self.novel_data: Optional[NovelData] = None

        try:
            data: Dict[str, Any] = response.json()
            self.count = Count(**data[0])
            self.novel_data = NovelData(**data[1])
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error processing response data: {e}")
