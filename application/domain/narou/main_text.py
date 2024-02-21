"""小説取得API."""
from bs4 import BeautifulSoup
from fastapi import Depends, HTTPException, status
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from apis.request import request_get
from config.config import get_async_session
from domain.narou.narou_data import NarouData
from models.novel import NovelResponse
from models.readhistory import ReadHistory
from urls import Url


async def get_main_text(
    ncode: str,
    episode: int,
    async_session: AsyncSession = Depends(get_async_session),
):
    """小説取得API."""
    # t-ga：小説名、全話数を出力
    payload = {
        "of": "t-ga",
        "ncode": {ncode},
        "lim": 1,
        "out": "json",
    }
    response = request_get(Url.API_URL.value, payload=payload)
    json_data = NarouData(response)

    all_count = json_data.count.allcount
    novel_data = json_data.novel_data

    # 不正なnコードかどうかのチェック・存在しないエピソードかどうかのチェック
    # all_count(検索ヒット数)とlimit数が一致していない場合はエラーを返す
    # フロントから渡された話数と全話数が一致していない場合はエラーを返す
    if not all_count == 1 or episode > novel_data.general_all_no:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nコードか話数が存在しません",
        )

    next_episode = not episode == novel_data.general_all_no
    prev_episode = episode > 1

    novel_url = Url.NOVEL_URL.join(ncode, str(episode))
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/97.0.4692.71 Safari/537.36"
        )
    }

    novel_response = request_get(novel_url, headers, payload)
    soup = BeautifulSoup(novel_response.text, "html.parser")

    subtitle = soup.select_one("p.novel_subtitle").text

    honbun = soup.select_one("#novel_honbun").text
    honbun += "\n"
    result_list = honbun.split("\n")

    try:
        # レコードがある場合は更新、無い場合は作成する
        stmt = insert(ReadHistory).values(ncode=ncode, read_episode=episode)
        stmt = stmt.on_conflict_do_update(
            index_elements=["ncode"],
            set_={"read_episode": stmt.excluded.read_episode},
        )
        await async_session.execute(stmt)
        await async_session.commit()

        novel = NovelResponse(
            title=novel_data.title,
            subtitle=subtitle,
            text=result_list,
            next=next_episode,
            prev=prev_episode,
        )

        return novel

    except Exception:
        # トランザクション内でのエラー処理
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="サーバーエラーが発生しました。",
        )
