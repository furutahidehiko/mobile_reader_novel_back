"""このスクリプトは、コマンドラインから特定のコマンドを実行するためのものです。.

コマンドライン引数に応じて、異なる機能を実行します。

使い方:
    python [スクリプト名] [コマンド]

利用可能なコマンド:
    load_json: JSONファイルを読み込み、指定された処理を実行します。

注意:
    コマンドライン引数が適切でない場合、エラーメッセージを表示します。
"""
import asyncio
import sys

from command import load_json

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("実行するコマンドを指定してください", file=sys.stderr)
    if args[1] == "load_json":
        asyncio.run(load_json.run(args))
