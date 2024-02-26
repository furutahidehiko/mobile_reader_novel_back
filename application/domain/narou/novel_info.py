from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession

from apis.request import request_get
from apis.urls import Url
from apis.user_agent import UserAgentManager
from crud import get_read_episode_by_ncode,get_follow_status_by_ncode
from domain.narou.common import BigGenre,Genre
from domain.narou.narou_data import NarouData
from models.follow import Follow
from schemas.novel import NovelInfoResponse


def scrape_narou_chapters(ncode: str, total_episodes: int) -> list:
    """
    指定されたncodeの小説の目次情報をスクレイピングで取得する関数。

    Parameters:
    - ncode (str): スクレイピング対象の小説のNコード。
    - total_episodes (int): 小説の総エピソード数。

    Returns:
    - list: 各章のタイトルとその下のサブタイトルのリストを含む辞書のリスト。
    """

    # 総エピソード数を基にページ数を計算
    quotient, remainder = divmod(total_episodes, 100)
    page_count = quotient + (1 if remainder > 0 else 0)

    # Response用の変数を準備
    chapters = []
    last_chapter_title = ""
    sub_titles = []

    # ユーザーエージェントを設定
    ua_manager = UserAgentManager()
    headers = ua_manager.get_random_user_headers()

    # 指定されたページ数だけループして目次情報を取得
    for page in range(1, page_count + 1):
        payload = {
        "ncode": {ncode},
        "p": {page},
        }
        resp = request_get(Url.NOVEL_URL.value, headers=headers,payload=payload)
        if resp is None:
            continue

        soup = BeautifulSoup(resp.content, 'html.parser')
        
        for child in soup.select('.index_box > *'):
            if 'chapter_title' in child.get('class', []):
                chapter_title = child.get_text(strip=True)
                if chapter_title != last_chapter_title:
                    if last_chapter_title or sub_titles:
                        chapters.append({
                            "chapter_title": last_chapter_title,
                            "sub_titles": sub_titles,
                        })
                        sub_titles = []
                    last_chapter_title = chapter_title
            elif 'novel_sublist2' in child.get('class', []):
                for sub in child.select('.subtitle'):
                    clean_subtitle = sub.get_text(strip=True).replace("\n", "")
                    sub_titles.append(clean_subtitle)
    
    # 最後の章をリストに追加
    if last_chapter_title or sub_titles:
        chapters.append({
            "chapter_title": last_chapter_title,
            "sub_titles": sub_titles,
        })

    return chapters

async def get_novel_info(db: AsyncSession, ncode: str):
    """
    指定されたncodeに基づいて小説の情報を取得し、それをレスポンスモデルに設定する関数。

    Parameters:
    - db (AsyncSession): 非同期SQLAlchemyセッション。データベースとの非同期通信。
    - ncode (str): 検索対象の小説コード。

    Returns:
    - NovelInfoResponse: 取得した小説情報を含むレスポンスモデルのインスタンス。
    """
    # t-ga：小説名、全話数を出力
    payload = {
        "of": "t-ga-w-gf-k-s-bg-g-gl",
        "ncode": {ncode},
        "lim": 1,
        "out": "json",
    }
    response = request_get(Url.API_URL.value, payload=payload)
    data = NarouData(response)

    # 非同期データベースクエリを実行してread_episodeを取得
    read_episode = await get_read_episode_by_ncode(db, ncode)
    # 非同期データベースクエリを実行してis_followを取得
    is_follow = await get_follow_status_by_ncode(db, ncode)
    
    # APIレスポンスから小説データを抽出
    novel_data = {
    "title": data.novel_data.title,
    "author": data.novel_data.writer,
    "episode_count": data.novel_data.general_all_no, 
    "release_date": data.novel_data.general_firstup,
    "tag": data.novel_data.keyword.split(" "),
    "summary": data.novel_data.story.split("\n"),
    "category": BigGenre.get_label_by_id(data.novel_data.biggenre),
    "sub_category": Genre.get_label_by_id(data.novel_data.genre),
    "updated_at": data.novel_data.general_lastup,
    "read_episode": read_episode,
    "chapters": scrape_narou_chapters(ncode, data.novel_data.general_all_no),
    "is_follow": is_follow
}

    # NovelInfoResponseモデルのインスタンスを作成して返す
    return NovelInfoResponse(**novel_data)


