"""ルーター用モジュール."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import get_async_session
from domain.narou.follow import delete_follow, post_follow
from domain.narou.main_text import get_main_text
from domain.narou.novel_info import get_novel_info
from domain.user.auth import auth_password, auth_token

from schemas.follow import FollowResponse
from schemas.novel import NovelInfoResponse, NovelResponse
from schemas.user import AuthUserModel, AuthUserResponse, GrantType

router = APIRouter()


@router.get(
    "/api/maintext",
    response_model=NovelResponse,
    summary="本文取得API",
    description="指定されたNコードとエピソード番号から小説本文に関する情報を取得します。",
    tags=["小説表示画面"],
)
async def main_text(
    *,
    ncode: str,
    episode: int,
    async_session: AsyncSession = Depends(get_async_session),
):
    """小説取得APIのエンドポイント."""
    return await get_main_text(ncode, episode, async_session)


@router.get(
    "/api/novelinfo",
    response_model=NovelInfoResponse,
    summary="小説情報取得API",
    description="指定されたNコードから目次ページに関する情報を取得します。",
    tags=["目次画面"],
)
async def novel_info(ncode: str, db: AsyncSession = Depends(get_async_session)):
    """小説情報取得APIのエンドポイント."""
    return await get_novel_info(db, ncode)


@router.post(
    "/api/follow",
    response_model=FollowResponse,
    summary="お気に入り登録API",
    description="指定されたNコードをお気に入り登録します。",
    tags=["お気に入り"],
)
async def post_follow_router(
    ncode: str, db: AsyncSession = Depends(get_async_session)
):
    """お気に入り登録APIのエンドポイント."""
    return await post_follow(db, ncode)


@router.delete(
    "/api/follow",
    response_model=FollowResponse,
    summary="お気に入り削除API",
    description="指定されたNコードをお気に入り削除します。",
    tags=["お気に入り"],
)
async def delete_follow_router(
    ncode: str, db: AsyncSession = Depends(get_async_session)
):
    """お気に入り削除APIのエンドポイント."""
    return await delete_follow(db, ncode)


@router.post(
    "/token/",
    response_model=AuthUserResponse,
    status_code=status.HTTP_200_OK,
    summary="ログイン認証・トークン生成API",
    description="ID/パスワードorリフレッシュトークンによる認証を行い新たなアクセストークンとリフレッシュトークンを発行します。",
    tags=["token"],
)
async def auth_token_router(
    auth_data: AuthUserModel,
    async_session: AsyncSession = Depends(get_async_session),
):
    """ログイン認証・トークン生成APIのエンドポイント."""
    match auth_data.grant_type:
        case GrantType.PASSWORD.value:
            return await auth_password(
                email=auth_data.user_id,
                password=auth_data.password,
                async_session=async_session,
            )
        case GrantType.REFRESH_TOKEN.value:
            return await auth_token(refresh_token=auth_data.refresh_token)
        case _:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "invalid_grant_type",
                    "error_description": "grant_typeが不明です",
                },
            )