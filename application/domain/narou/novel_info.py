import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.follow import Follow
from models.novel import NovelInfoResponse
from models.read_history import ReadHistory

# ユーザーエージェントをランダムに生成するためのオブジェクト
ua = UserAgent()

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
    headers = {'User-Agent': ua.random}  

    # 指定されたページ数だけループして目次情報を取得
    for page in range(1, page_count + 1):
        url = f"https://ncode.syosetu.com/{ncode}/?p={page}"
        resp = requests.get(url,headers=headers)
        resp.raise_for_status()

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

async def get_read_episode_by_ncode(db: AsyncSession, ncode: str) -> int:
    """
    指定されたncodeに基づいてread_episodeの値を非同期で取得する関数。

    Parameters:
    - db (AsyncSession): 非同期SQLAlchemyセッション。データベースとの非同期通信。
    - ncode (str): 検索対象の小説コード。

    Returns:
    - int: 読んだ最後のエピソード番号。該当するエピソードがない場合は0を返します。
    """
    query = select(ReadHistory.read_episode).filter(ReadHistory.ncode == ncode)
    result = await db.execute(query)
    read_episode = result.scalars().first()
    return read_episode if read_episode is not None else 0

async def get_follow_status_by_ncode(db: AsyncSession, ncode: str) -> bool:
    """
    指定されたncodeに基づいてfollowの値を非同期で取得する関数。
    
    Parameters:
    - db (AsyncSession): 非同期SQLAlchemyセッション。データベースとの非同期通信。
    - ncode (str): 検索対象の小説コード。

    Returns:
    - bool: ユーザーが指定したncodeの小説をフォローしているかどうかの真偽値。
    """

    # ReadHistoryからncodeに基づくIDを取得
    query_read_history_id = select(ReadHistory.id).filter(ReadHistory.ncode == ncode)
    result_read_history_id = await db.execute(query_read_history_id)
    read_history_id = result_read_history_id.scalars().first()

    if read_history_id is None:
        return False  # ReadHistoryに該当するレコードがない場合、Falseを返す

    # 取得したIDを基にFollowテーブルからfollowステータスを取得
    query_follow_status = select(Follow.follow).filter(Follow.read_history_id == read_history_id)
    result_follow_status = await db.execute(query_follow_status)
    follow_status = result_follow_status.scalars().first()

    return follow_status if follow_status is not None else False

async def get_novel_info(db: AsyncSession, ncode: str):
    """
    指定されたncodeに基づいて小説の情報を取得し、それをレスポンスモデルに設定する関数。

    Parameters:
    - db (AsyncSession): 非同期SQLAlchemyセッション。データベースとの非同期通信。
    - ncode (str): 検索対象の小説コード。

    Returns:
    - NovelInfoResponse: 取得した小説情報を含むレスポンスモデルのインスタンス。
    """
    # narouAPIのエンドポイントURL
    endpoint = f"https://api.syosetu.com/novelapi/api/?ncode={ncode}&out=json"
    big_genre_dict = {
		1: "恋愛", 2: "ファンタジー", 3: "文芸", 4: "SF", 99: "その他", 98: "ノンジャンル",
	}
    genre_dict = {
				1: "恋愛",
				2: "ファンタジー",
				3: "文芸",
				4: "SF",
				99: "その他",
				98: "ノンジャンル",
				101: "異世界〔恋愛〕",
				102: "現実世界〔恋愛〕",
				201: "ハイファンタジー〔ファンタジー〕",
				202: "ローファンタジー〔ファンタジー〕",
				301: "純文学〔文芸〕",
				302: "ヒューマンドラマ〔文芸〕",
				303: "歴史〔文芸〕",
				304: "推理〔文芸〕",
				305: "ホラー〔文芸〕",
				306: "アクション〔文芸〕",
				307: "コメディー〔文芸〕",
				401: "VRゲーム〔SF〕",
				402: "宇宙〔SF〕",
				403: "空想科学〔SF〕",
				404: "パニック〔SF〕",
				9901: "童話〔その他〕",
				9902: "詩〔その他〕",
				9903: "エッセイ〔その他〕",
				9904: "リプレイ〔その他〕",
				9999: "その他〔その他〕",
				9801: "ノンジャンル〔ノンジャンル〕",
			}
    
    # APIからデータを取得
    response = requests.get(endpoint)
    data = response.json()[1]  # 最初の要素はAPIのメタデータなので、小説データは[1]になる

    # 非同期データベースクエリを実行してread_episodeを取得
    read_episode = await get_read_episode_by_ncode(db, ncode)
    # 非同期データベースクエリを実行してis_followを取得
    is_follow = await get_follow_status_by_ncode(db, ncode)
    
    # APIレスポンスから小説データを抽出
    novel_data = {
        "title": data.get("title"),
        "author": data.get("writer"),
        "episode_count": data.get("general_all_no"),
        "release_date": data.get("general_firstup"),
        "tag": data.get("keyword").split(" "),
        "summary": data.get("story"),
        "category": big_genre_dict[data.get("biggenre")],
        "sub_category": genre_dict[data.get("genre")],
        "updated_at": data.get("general_lastup"),
        "read_episode": read_episode, 
        "chapters": scrape_narou_chapters(ncode,data.get("general_all_no")),
        "is_follow": is_follow
    }

    # NovelInfoResponseモデルのインスタンスを作成して返す
    return NovelInfoResponse(**novel_data)


