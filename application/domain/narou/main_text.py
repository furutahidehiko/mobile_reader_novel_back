"""小説取得API."""
from bs4 import BeautifulSoup
from fastapi import Depends, HTTPException, status
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from apis.request import request_get
from apis.urls import Url
from apis.user_agent import UserAgentManager
from config.config import get_async_session
from domain.narou.narou_data import NarouData
from models.book import Book
from models.read_history import ReadHistory
from schemas.novel import NovelResponse

async def get_main_text(
    ncode: str,
    episode: int,
    db: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    指定されたncode(小説コード)とepisode(話数)の小説本文をスクレイピングで取得する関数。

    Parameters:
    - ncode (str): スクレイピング対象の小説のNコード。
    - episodes (int): 小説のエピソード。
    Returns:
    - dict: 小説のタイトル、サブタイトル、本文(リスト形式)、次話・全話有無を含む辞書。
    """

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

    # ユーザーエージェントを設定
    ua_manager = UserAgentManager()
    headers = ua_manager.get_random_user_headers()

    novel_response = request_get(novel_url, headers, payload)
    soup = BeautifulSoup(novel_response.text, "html.parser")

    subtitle = soup.select_one("p.novel_subtitle").text

    honbun = soup.select_one("#novel_honbun").text
    honbun += "\n"
    result_list = honbun.split("\n")

    # Bookテーブルからncodeに対応するbook_idを取得
    book_query = select(Book.id).where(Book.ncode == ncode)
    book_result = await db.execute(book_query)
    book_record = book_result.scalars().first()
    if not book_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    book_id = book_record

    # 既読していなければ、データを挿入
    stmt = (
    insert(ReadHistory).
    values(book_id=book_id, read_episode=episode).
    on_conflict_do_nothing(index_elements=['book_id', 'read_episode'])
    )
    
    await db.execute(stmt)
    await db.commit()
        

    novel = NovelResponse(
        title=novel_data.title,
        subtitle=subtitle,
        text=result_list,
        next=next_episode,
        prev=prev_episode,
    )


    return novel