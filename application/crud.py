from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from models.book import Book
from models.read_history import ReadHistory
from models.follow import Follow

async def ensure_book_exists(db: AsyncSession, ncode: str) -> int:
    """
    指定されたncodeに基づいてBookテーブルを検索し、存在しない場合は新規追加する関数。
    追加または検索によって得られたbook_idを返す。
    """
    # UPSERT操作
    stmt = insert(Book).values(ncode=ncode).on_conflict_do_nothing(index_elements=['ncode'])
    await db.execute(stmt)
    await db.commit()

    # ncodeに対応するbook_idを取得
    book_query = select(Book.id).where(Book.ncode == ncode)
    book_result = await db.execute(book_query)
    book_id = book_result.scalars().first()

    return book_id

async def insert_read_history_if_not_exists(db: AsyncSession, book_id: int, episode: int):
    """
    指定されたbook_idとエピソードに対応する既読情報が存在しなければ、データを挿入する関数。
    """
    stmt = (
        insert(ReadHistory).
        values(book_id=book_id, read_episode=episode).
        on_conflict_do_nothing(index_elements=['book_id', 'read_episode'])
    )
    await db.execute(stmt)
    await db.commit()

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


async def check_follow_exists_by_ncode(db: AsyncSession, ncode: str) -> bool:
    """
    指定されたncodeに基づき、Bookテーブルからbook_idを取得し、
    そのbook_idに紐づくFollowレコードの存在有無に基づいてフォローの有無を返す関数。
    """
    # Bookテーブルからncodeに基づくbook_idを取得
    book_query = select(Book.id).where(Book.ncode == ncode)
    book_result = await db.execute(book_query)
    book_id = book_result.scalars().first()

    if book_id is None:
        # book_idが取得できなければ、フォローされていないと判断
        return False

    # Followテーブルからbook_idに紐づくレコードの存在チェック
    follow_existence_query = select(Follow.id).filter(Follow.book_id == book_id)
    follow_existence_result = await db.execute(follow_existence_query)
    follow_exists = follow_existence_result.scalars().first() is not None

    return follow_exists
