"""ルーター用モジュール."""

from datetime import datetime, timedelta
from typing import Annotated, Optional

from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import crud
from apis.request import request_get
from config.config import get_async_session
from config.environment import jwt_settings
from models.customer import Customer
from models.novel import NovelResponse
from schemas.customer import (
    CustomerModel,
    CustomerResponse,
    LoginCustomerModel,
    LoginCustomerRespones,
)
from urls import Url

router = APIRouter()


@router.post(
    "/customer/",
    tags=["customer"],
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer_api(
    customer_model: CustomerModel,
    async_session: AsyncSession = Depends(get_async_session),
):
    """顧客生成用API."""
    customer = await crud.create_customer(async_session, customer_model)
    return CustomerResponse(id=customer.id, name=customer.name)


@router.post(
    "/login/",
    tags=["customer"],
    response_model=LoginCustomerRespones,
    status_code=status.HTTP_200_OK,
)
async def login(
    login_data: LoginCustomerModel,
    async_session: AsyncSession = Depends(get_async_session),
):
    """ログインAPI."""

    def authenticate_user(customer: Optional[Customer]):
        if customer is None:
            return False
        return customer.check_password(login_data.password)

    result = await async_session.execute(
        select(Customer).where(Customer.id == login_data.id)
    )
    customer = result.scalar_one_or_none()
    if not authenticate_user(customer):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="idかpasswordが異なります.",
        )
    min = timedelta(minutes=jwt_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + min
    access_token = jwt.encode(
        {"sub": customer.id, "exp": expire},
        jwt_settings.JWT_SECRET_KEY,
        algorithm=jwt_settings.JWT_ALGORITHM,
    )
    return LoginCustomerRespones(access_token=access_token)


@router.get("/items/")
async def read_items(
    current_customer: Annotated[Customer, Depends(crud.get_current_customer)]
):
    """テスト."""
    print(current_customer)
    return {"customer_name": current_customer.name}


@router.get(
    "/api/maintext",
    response_model=NovelResponse,
)
def get_novel(*, ncode: str, episode: int):
    """小説取得API."""
    # t-ga：小説名、全話数を出力
    # lim: 取得数をlimit(1)の数に制限
    # json形式で出力
    limit = 1
    payload = {
        "of": "t-ga",
        "ncode": {ncode},
        "lim": limit,
        "out": "json",
    }
    response = request_get(Url.API_URL.value, payload=payload)

    all_count = response.json()[0]  # all_count(検索ヒット数)
    novel_data = response.json()[
        1
    ]  # novel_data(全話数(general_all_no),小説タイトル(title))

    # 不正なnコードかどうかのチェック・存在しないエピソードかどうかのチェック
    # all_count(検索ヒット数)とlimit数が一致していない場合はエラーを返す
    # フロントから渡された話数と全話数が一致していない場合はエラーを返す
    # print(all_count["allcount"])
    # print(novel_data["general_all_no"])
    if (
        not all_count["allcount"] == limit
        or episode > novel_data["general_all_no"]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nコードか話数が存在しません",
        )

    # 前話・次話判定
    next_episode: bool = not episode == novel_data["general_all_no"]
    prev_episode: bool = episode > 1

    # なろう小説URL
    novel_url = Url.NOVEL_URL.join(ncode, str(episode))

    # User-Agentを設定
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/97.0.4692.71 Safari/537.36"
        )
    }

    novel_response = request_get(novel_url, headers, payload)
    soup = BeautifulSoup(novel_response.text, "html.parser")

    # 各話タイトル
    subtitle = soup.select_one("p.novel_subtitle").text
    print(soup.select_one("p", class_="novel_subtitle").text)

    # 本文
    honbun = soup.select_one("#novel_honbun").text
    honbun += "\n"
    # 空白行も含めてリストにする
    result_list = honbun.split("\n")

    # @Todo 既読更新処理(DB連携)
    novel = NovelResponse(
        title=novel_data["title"],
        subtitle=subtitle,
        text=result_list,
        next=next_episode,
        prev=prev_episode,
    )

    return novel
