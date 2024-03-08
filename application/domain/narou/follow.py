"""このモジュールは、お気に入りの設定や解除に関する非同期関数を提供します。.

特定の小説のお気に入り設定（フォロー）と解除（アンフォロー）の機能が含まれています。
"""

from sqlalchemy.ext.asyncio import AsyncSession

from crud import (
    create_or_check_existing_follow,
    delete_follow_by_book_id,
    ensure_book_exists,
)
from schemas.follow import FollowResponse


async def post_follow(db: AsyncSession, ncode: str):
    """指定されたncodeに基づいて小説の情報を取得し、それをお気に入りに設定する関数。."""
    # Bookテーブルからncodeに対応するbook_idを取得。
    book_id = await ensure_book_exists(db, ncode)
    # Followテーブルを検索し、boolを返す。
    is_follow = not await create_or_check_existing_follow(db, book_id)

    return FollowResponse(is_success=is_follow)


async def delete_follow(db: AsyncSession, ncode: str):
    """指定されたncodeに基づいて小説の情報を取得し、それをお気に入りから削除する関数。."""
    # Bookテーブルからncodeに対応するbook_idを取得
    book_id = await ensure_book_exists(db, ncode)
    # Followテーブルで対応するエントリを検索し、削除する
    is_success = await delete_follow_by_book_id(db, book_id)

    return FollowResponse(is_success=is_success)
