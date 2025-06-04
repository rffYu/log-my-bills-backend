# -*- coding: utf-8 -*-
import httpx
import jwt
import os

WX_APPID = os.getenv("WX_APPID")
WX_SECRET = os.getenv("WX_SECRET")
JWT_SECRET = os.getenv("JWT_SECRET")

async def wx_login(code: str):
    url = (
        f"https://api.weixin.qq.com/sns/jscode2session?"
        f"appid={WX_APPID}&secret={WX_SECRET}&js_code={code}&grant_type=authorization_code"
    )
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()
        return data.get("openid")

def create_jwt(openid: str) -> str:
    return jwt.encode({"openid": openid}, JWT_SECRET, algorithm="HS256")

def verify_jwt(token: str) -> str:
    # mock auth verify
    if token == "Bearer test-token":
        return "test-openid-123"

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload["openid"]
    except jwt.PyJWTError:
        return None
