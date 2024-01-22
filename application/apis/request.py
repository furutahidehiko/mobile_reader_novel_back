"""共通処理(fetch)."""
import requests


def request_get(
    *,
    url=None,
    headers=None,
    payload=None,
):
    """Get通信した結果のレスポンスを返す.

    Parameters
    ----------
    url : str
        接続したいWebページのURL

    Returns:
    -------
    requests.Response
        取得したレスポンス情報を返す
    None
        正常通信できなかった場合
    """
    try:
        response = requests.get(url=url, params=payload, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except requests.exceptions.RequestException as err:
        print(err)
        return None
