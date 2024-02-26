from requests.models import Response
from dataclasses import dataclass



@dataclass
class Count:
    """検索ヒット数."""

    allcount: int


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
    """なろうの小説APIから取得したデータを整形するクラス。"""

    def __init__(self, response: Response):
        self.count: Optional[Count] = None
        self.novel_data: Optional[NovelData] = None

        try:
            data: Dict[str, Any] = response.json()
            if data[0]:
                self.count = Count(**data[0])
            if data[1]:
                self.novel_data = NovelData(**data[1])
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error processing response data: {e}")