# -*- coding: utf-8 -*-
import logging
import asyncio
import itertools
from typing import Optional
from fastapi import APIRouter, Response, Depends
from pydantic import BaseModel
from server.auth import wx_login, create_jwt
from server.deps import get_openid
from .. import routing_table

logger = logging.getLogger("api_handler")

router = APIRouter()

class UserInfoResponse(BaseModel):
    openid: str
    role: str
    nickname: Optional[str] = ""
    avatarUrl: Optional[str] = ""
    mainUserId: Optional[str] = ""

@router.get(routing_table.USER_INFO)
async def user_info(
    openid: str = Depends(get_openid),
) -> UserInfoResponse:
    """
    获取当前登录用户的信息（openid）
    """
    return UserInfoResponse(openid=openid, role="user")

