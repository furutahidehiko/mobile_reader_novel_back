"""このスクリプトは、データベース操作に関連する複数の非同期関数を含んでいます."""
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.book import Book
from models.follow import Follow
from models.read_history import ReadHistory


async def ensure_book_exists(db: AsyncSession, ncode: str) -> int:
    """指定されたncodeに基づいてBookテーブルを検索し、存在しない場合は新規追加する関数.

    追加または検索によって得られたbook_idを返す。
    """
    # UPSERT操作
    stmt = (
        insert(Book)
        .values(ncode=ncode)
        .on_conflict_do_nothing(index_elements=["ncode"])
    )
    await db.execute(stmt)
    await db.commit()

    # ncodeに対応するbook_idを取得
    book_query = select(Book.id).where(Book.ncode == ncode)
    book_result = await db.execute(book_query)
    book_id = book_result.scalars().first()

    return book_id


async def create_or_check_existing_follow(
    db: AsyncSession, book_id: int
) -> bool:
    """指定されたbook_idに基づいてFollowテーブルを検索し、存在しない場合は新しく作成する.

    既に存在する場合はTrueを返し、存在しない場合は新しく作成後にFalseを返す.
    """
    stmt = (
        insert(Follow)
        .values(book_id=book_id)
        .on_conflict_do_nothing(index_elements=["book_id"])
    )
    result = await db.execute(stmt)
    await db.commit()

    return result.rowcount == 0


async def delete_follow_by_book_id(db: AsyncSession, book_id: int) -> bool:
    """指定されたbook_idに基づいてFollowテーブルからエントリを削除する."""
    query_delete_follow = delete(Follow).where(Follow.book_id == book_id)
    result = await db.execute(query_delete_follow)
    await db.commit()

    return result.rowcount > 0


async def update_or_create_read_history(
    db: AsyncSession, book_id: int, episode: int
):
    """指定されたbook_idに対応する既読情報を更新する。既読情報が存在しない場合は新たに挿入する."""
    stmt = insert(ReadHistory).values(book_id=book_id, read_episode=episode)
    stmt = stmt.on_conflict_do_update(
        index_elements=["book_id"],
        set_={"read_episode": stmt.excluded.read_episode},
        where=(ReadHistory.read_episode != stmt.excluded.read_episode),
    )
    await db.execute(stmt)
    await db.commit()


async def get_latest_read_episode_by_book_id(
    db: AsyncSession, book_id: int
) -> int:
    """指定されたbook_idに対応する既読エピソード数を非同期で取得する関数."""
    query = select(ReadHistory.read_episode).filter(
        ReadHistory.book_id == book_id
    )
    result = await db.execute(query)
    latest_read_episode = result.scalar()

    if latest_read_episode is None:
        latest_read_episode = 0
    return latest_read_episode


async def check_follow_exists_by_book_id(
    db: AsyncSession, book_id: int
) -> bool:
    """指定されたbook_idに紐づくFollowレコードの存在有無に基づいてフォローの有無を返す関数."""
    # Followテーブルからbook_idに紐づくレコードの存在チェック
    follow_existence_query = select(Follow.id).filter(Follow.book_id == book_id)
    follow_existence_result = await db.execute(follow_existence_query)
    if follow_existence_result.scalars().first() is None:
        return False
    return True
