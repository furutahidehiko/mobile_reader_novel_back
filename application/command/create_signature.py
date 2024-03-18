"""署名生成コマンド."""

from apis.signature import create_signature


def run():
    """指定されたAPIエンドポイントに対するHTTPメソッドの組み合わせに基づいて、署名を生成して表示します。.

    この関数は、予め定義されたHTTPメソッドとAPIエンドポイントのタプル（api_tuple）をループで処理します。
    各組み合わせに対して、`create_signature`関数を呼び出し、生成された署名を表示します。
    """
    api_tuple = (
        ("GET", "http://localhost:8000/api/novelinfo"),
        ("GET", "http://localhost:8000/api/maintext"),
        ("POST", "http://localhost:8000/api/follow"),
        ("DELETE", "http://localhost:8000/api/follow"),
    )
    for method, url in api_tuple:
        print(url, create_signature(method, url))
