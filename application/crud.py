from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from models.book import Book
from models.read_history import ReadHistory
from models.follow import Follow


async def get_read_episode_by_ncode(db: AsyncSession, ncode: str) -> int:
    """
    指定されたncodeに基づいてread_episodeの値を非同期で取得する関数。
    """
    # Bookテーブルからncodeに基づくbook_idを取得
    book_query = select(Book.id).where(Book.ncode == ncode)
    book_result = await db.execute(book_query)
    book_id = book_result.scalars().first()

    if book_id is None:
        return 0

    # ReadHistoryからbook_idに基づくread_episodeの最大値を取得
    query = select(func.max(ReadHistory.read_episode)).filter(ReadHistory.book_id == book_id)
    result = await db.execute(query)
    max_read_episode = result.scalars().first()

    return max_read_episode if max_read_episode is not None else 0


async def get_follow_status_by_ncode(db: AsyncSession, ncode: str) -> bool:
    """
    指定されたncodeに基づいてfollowの値を非同期で取得する関数。
    """
    # Bookテーブルからncodeに基づくbook_idを取得
    book_query = select(Book.id).where(Book.ncode == ncode)
    book_result = await db.execute(book_query)
    book_id = book_result.scalars().first()

    if book_id is None:
        return False

    # Followテーブルからbook_idに基づくis_followステータスを取得
    query_follow_status = select(Follow.is_follow).filter(Follow.book_id == book_id)
    result_follow_status = await db.execute(query_follow_status)
    follow_status = result_follow_status.scalars().first()

    return follow_status if follow_status is not None else False
