# -*- coding: utf-8 -*-
import logging
import asyncio
import itertools
from fastapi import APIRouter, Response
from pydantic import BaseModel
from server.auth import wx_login, create_jwt
from .. import routing_table

logger = logging.getLogger("api_handler")

router = APIRouter()

class LoginRequest(BaseModel):
    code: str

@router.post(routing_table.LOGIN)
async def login(body: LoginRequest):
    openid = await wx_login(body.code)
    if not openid:
        return {"error": "登录失败"}
    token = create_jwt(openid)
    return {"token": token}

