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
    stmt = insert(Book).values(ncode=ncode).on_conflict_do_nothing(index_elements=['ncode'])
    result = await db.execute(stmt)
    await db.commit()

    if result.returned_rows == 0:
        # 追加された行がない場合、ncodeに対応する既存のレコードを取得
        book_query = select(Book.id).where(Book.ncode == ncode)
        book_result = await db.execute(book_query)
        book_id = book_result.scalars().first()
    else:
        # 新規追加された場合、そのbook_idを取得
        book_query = select(Book.id).where(Book.ncode == ncode)
        book_result = await db.execute(book_query)
        book_id = book_result.scalars().first()

    return book_id

async def create_or_check_existing_follow(db: AsyncSession, book_id: int) -> bool:
    """
    指定されたbook_idに基づいてFollowテーブルを検索し、存在しない場合は新しく作成する。
    既に存在する場合はTrueを返し、存在しない場合は新しく作成後にFalseを返す。
    """
    stmt = insert(Follow).values(book_id=book_id).on_conflict_do_nothing(index_elements=['book_id'])
    result = await db.execute(stmt)
    await db.commit()

    if result.rowcount == 0:
        # 既に存在する場合
        return True
    else:
        # 新しく作成された場合
        return False

async def delete_follow_by_book_id(db: AsyncSession, book_id: int) -> bool:
    """
    指定されたbook_idに基づいてFollowテーブルからエントリを削除する。
    """
    query_delete_follow = delete(Follow).where(Follow.book_id == book_id)
    result = await db.execute(query_delete_follow)
    await db.commit()

    # 削除された行があればTrue、そうでなければFalseを返す
    return result.rowcount > 0
