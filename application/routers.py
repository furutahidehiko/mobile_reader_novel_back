"""ルーター用モジュール."""

from datetime import datetime, timedelta
from typing import Annotated, Optional

from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import crud
from apis.request import request_get
from config.config import get_async_session
from config.environment import jwt_settings
from models.customer import Customer
from schemas.customer import (
    CustomerModel,
    CustomerResponse,
    LoginCustomerModel,
    LoginCustomerRespones,
)
from urls import Url

router = APIRouter()


class NovelResponse(BaseModel):
    """小説本文データ.

    Parameters:
    ----------
    title : 小説のタイトル
    text : 本文
    next : 次ページ有無
    prev : 前ページ有無
    """

    title: str = None
    text: str = None
    next: bool = False
    prev: bool = False


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
    # t-w-n-k-g：小説名、作者名、Nコード、キーワード、全話数を出力
    # json形式で出力
    payload = {"of": "t-w-n-k-g", "keyword": "1", "out": "json"}
    response = request_get(payload=payload, url=Url.API_URL.value, headers=None)
    novel_data = response.json()
    all_episode = novel_data[1]["genre"]
    title = novel_data[1]["title"]

    # 前話・次話判定
    next_episode: bool = not episode == all_episode
    prev_episode: bool = episode > 1

    # なろう小説URL
    novel_url = f"{Url.NOVEL_URL.value}{ncode}/{episode}/"

    # User-Agentを設定
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/97.0.4692.71 Safari/537.36"
        )
    }

    novel_response = request_get(url=novel_url, payload=None, headers=headers)

    soup = BeautifulSoup(novel_response.text, "html.parser")

    # 各話タイトル @ToDo:一旦不要
    # subtitle = soup.select_one('p', class_ = 'novel_subtitle').text
    # print(subtitle)

    # 本文
    honbun = soup.select_one("#novel_honbun").text
    honbun += "\n"

    # JSONを表示
    print(
        NovelResponse(
            title=title, text=honbun, next=next_episode, prev=prev_episode
        )
    )

    return NovelResponse(
        title=title, text=honbun, next=next_episode, prev=prev_episode
    )
