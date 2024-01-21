"""ルーター用モジュール."""

from datetime import datetime, timedelta
from typing import Annotated, Optional
from bs4 import BeautifulSoup

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import crud
import requests
import json

from config.config import get_async_session
from config.environment import jwt_settings
from models.customer import Customer
from schemas.customer import (
    CustomerModel,
    CustomerResponse,
    LoginCustomerModel,
    LoginCustomerRespones,
)

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


@router.get("/api/maintext")
def scraping(
    *,
    ncode:str,
    episode:int
):
    
    # なろう小説API
    base_url = "http://api.syosetu.com/novelapi/api/"

    # t-w-n-k-g：小説名、作者名、Nコード、キーワード、全話数を出力
    # json形式で出力
    payload = {'of': 't-w-n-k-g', 'ncode': ncode, 'keyword': '1', 'out':'json'}
    response =  requests.get(base_url, payload).json()
    # print(response)

    all_episode = response[1]['genre']
    title = response[1]['title']

    # 前話・次話判定
    next_episode:bool = False
    prev_episode:bool = False
    if not episode == all_episode:
        next_episode = True
    if episode > 1:
        prev_episode = True

    # なろう小説URL
    target_url = f"https://ncode.syosetu.com/{ncode}/{episode}/"

    # User-Agentを変更
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

    r = requests.get(target_url,headers=headers)
    soup = BeautifulSoup(r.text,'html.parser')

    # 各話タイトル @ToDo:一旦不要
    # subtitle = soup.select_one('p', class_ = 'novel_subtitle').text
    # print(subtitle)

    # 本文
    honbun = soup.select_one("#novel_honbun").text
    honbun += "\n"

    # テキストをJSONにまとめる
    result_json = {
        "title":title,
        "text": honbun,
        "next":next_episode,
        "prev":prev_episode,
        }
    
    # JSONを表示
    print(json.dumps(result_json, indent=2, ensure_ascii=False))
        
    return result_json

