from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.read_history import ReadHistory

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
    query_follow_status = select(Follow.is_follow).filter(Follow.read_history_id == read_history_id)
    result_follow_status = await db.execute(query_follow_status)
    follow_status = result_follow_status.scalars().first()

    return follow_status if follow_status is not None else False