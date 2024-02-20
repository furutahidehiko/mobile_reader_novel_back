from fastapi import HTTPException

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker

from models.follow import Follow, FollowResponse
from models.read_history import ReadHistory

async def post_follow(db: AsyncSession, ncode: str):
    """
    指定されたncodeに基づいて小説の情報を取得し、それをお気に入りに設定する関数。

    Parameters:
    - db (AsyncSession): 非同期SQLAlchemyセッション。データベースとの非同期通信。
    - ncode (str): 検索対象の小説コード。

    Returns:
    - FollowResponse: レスポンスモデルのインスタンス。
    """

    # ReadHistoryからncodeに対応するエントリを検索
    query_read_history = select(ReadHistory).filter(ReadHistory.ncode == ncode)
    result_read_history = await db.execute(query_read_history)
    read_history = result_read_history.scalars().first()

    if not read_history:
        # ReadHistoryに対応するエントリがなければエラー
        raise HTTPException(status_code=404, detail="ReadHistory not found")

    # Followテーブルで対応するエントリを検索
    query_follow = select(Follow).filter(Follow.read_history_id == read_history.id)
    result_follow = await db.execute(query_follow)
    follow = result_follow.scalars().first()

    if follow:
        # Followエントリが既に存在する場合、followをTrueに更新
        follow.follow = True
    else:
        # Followエントリが存在しない場合、新しく作成してfollowをTrueに設定
        follow = Follow(read_history_id=read_history.id, follow=True)
        db.add(follow)

    await db.commit()  # 変更をコミット

    return FollowResponse(is_success=True)


async def delete_follow(db: AsyncSession, ncode: str):
    """
    指定されたncodeに基づいて小説の情報を取得し、それをお気に入り削除する関数。

    Parameters:
    - db (AsyncSession): 非同期SQLAlchemyセッション。データベースとの非同期通信。
    - ncode (str): 検索対象の小説コード。

    Returns:
    - FollowResponse: レスポンスモデルのインスタンス。
    """
    # ReadHistoryからncodeに対応するエントリを検索
    query_read_history = select(ReadHistory.id).filter(ReadHistory.ncode == ncode)
    result_read_history = await db.execute(query_read_history)
    read_history_id = result_read_history.scalars().first()

    if not read_history_id:
        # ReadHistoryに対応するエントリがなければエラー
        raise HTTPException(status_code=404, detail="ReadHistory not found")

    # Followテーブルで対応するエントリを検索し、削除する
    query_delete_follow = delete(Follow).where(Follow.read_history_id == read_history_id).where(Follow.follow == True)
    result = await db.execute(query_delete_follow)
    
    # 削除が実行されたか確認
    if result.rowcount:
        # 変更をコミット
        await db.commit()
        return FollowResponse(is_success=True)
    else:
        # 削除対象がなかった場合
        raise HTTPException(status_code=404, detail="Follow entry not found or already unfollowed")
