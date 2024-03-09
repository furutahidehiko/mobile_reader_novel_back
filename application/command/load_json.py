"""このスクリプトはJSONファイルからデータを読み込み、データベースに挿入するために使用されます。.

このスクリプトはコマンドラインから実行され、JSONファイルのパスを引数として受け取ります。
指定されたJSONファイルからデータを読み込み、SQLAlchemyを使用してデータベースに挿入します。
"""
import json
import sys
from importlib import import_module
from pathlib import Path

from sqlalchemy.dialects.postgresql import insert

from config.config import get_async_session


def create_file_path(args):
    """コマンドライン引数からJSONファイルのパスを生成します。.

    引数:
        args (list): コマンドライン引数のリスト。

    戻り値:
        Path|None: 正しいファイルパスが指定されていればPathオブジェクトを、
                そうでなければNoneを返します。
    """
    if not len(args) == 3:
        print("対象のJSONファイルだけを指定してください", file=sys.stderr)
        return

    dir_path = Path("fixtures")
    if not dir_path.is_dir():
        print("fixturesディレクトリを作成してください", file=sys.stderr)
        return

    file_path = dir_path / args[2]
    if not file_path.exists():
        print(f"{file_path}が存在していないです", file=sys.stderr)
        return

    if not file_path.suffix == ".json":
        print(f"{file_path}の拡張子がjsonではありません", file=sys.stderr)
        return
    return file_path


async def run(args):
    """スクリプトのメイン実行関数。.

    JSONファイルを読み込み、データベースにデータを挿入します。

    引数:
        args (list): コマンドライン引数のリスト。
    """
    file_path = create_file_path(args)
    if file_path is None:
        return

    db = await get_async_session().__anext__()
    print(db)

    with open(file_path) as f:
        for data in json.load(f):
            module = import_module(f"models.{data['file']}")
            model = getattr(module, data["model"])
            stmt = insert(model).values(**data["fields"])
            await db.execute(stmt)
    await db.commit()
