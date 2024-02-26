"""Jsonデータのマッピングクラス."""
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
    """なろうの小説APIで取得したデータを整形するクラス。"""

    def __init__(self, response):
        self.count = None
        self.novel_data = None

        data = response.json()
        if len(data) > 0 and 'allcount' in data[0]:
            self.count = Count(**data[0])
        
        for item in data[1:]:
            if 'title' in item and 'general_all_no' in item:
                self.novel_data = NovelData(**item)
                break