"""Jsonデータのマッピングクラス."""
from dataclasses import dataclass


@dataclass
class Count:
    """検索ヒット数."""

    allcount: int


@dataclass
class NovelData:
    """小説情報."""

    title: str
    general_all_no: int


class NarouData:
    """なろうの小説APIで取得したデータ."""

    def __init__(self, data):
        """なろうの小説APIで取得したデータを整形."""

        def get_condition(item, dataclass_name):
            return item.keys() == dataclass_name.__dataclass_fields__.keys()

        for item in data.json():
            if get_condition(item, Count):
                self.count = Count(**item)
            elif get_condition(item, NovelData):
                self.novel_data = NovelData(**item)
