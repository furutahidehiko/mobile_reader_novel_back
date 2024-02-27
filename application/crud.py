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

    Parameters:
    - db (AsyncSession): 非同期SQLAlchemyセッション。
    - ncode (int): NCode。

    Returns:
    - int: 追加または検索によって得られたbook_id。

    """
    # Bookテーブルからncodeに対応するbook_idを取得
    book_query = select(Book.id).where(Book.ncode == ncode)
    book_result = await db.execute(book_query)
    book_record = book_result.scalars().first()

    # 指定されたncodeの小説情報が存在しない場合、新規追加する
    if not book_record:
        new_book = Book(ncode=ncode)
        db.add(new_book)
        await db.commit()
        await db.refresh(new_book)
        return new_book.id
    else:
        return book_record

async def create_or_check_existing_follow(db: AsyncSession, book_id: int) -> bool:
    """
    指定されたbook_idに基づいてFollowテーブルを検索し、存在しない場合は新しく作成する。
    既に存在する場合はTrueを返し、存在しない場合は新しく作成後にFalseを返す。

    Parameters:
    - db (AsyncSession): 非同期SQLAlchemyセッション。
    - book_id (int): 検索対象のBook ID。

    Returns:
    - bool: Followエントリが既に存在するかどうか。
    """
    query_follow = select(Follow).filter(Follow.book_id == book_id)
    result_follow = await db.execute(query_follow)
    follow = result_follow.scalars().first()

    if not follow:
        follow = Follow(book_id=book_id)
        db.add(follow)
        await db.commit()
        return False
    else:
        return True

async def delete_follow_by_book_id(db: AsyncSession, book_id: int) -> bool:
    """
    指定されたbook_idに基づいてFollowテーブルからエントリを削除する。

    Parameters:
    - db (AsyncSession): 非同期SQLAlchemyセッション。
    - book_id (int): 削除対象のBook ID。

    Returns:
    - bool: 削除が成功したかどうか。
    """
    query_delete_follow = delete(Follow).where(Follow.book_id == book_id)
    result = await db.execute(query_delete_follow)
    await db.commit()

    # 削除された行があればTrue、そうでなければFalseを返す
    return result.rowcount > 0
