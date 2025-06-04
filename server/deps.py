# -*- coding: utf-8 -*-
from fastapi import Depends, Header, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from server.weixin_auth import verify_jwt
from server.constants import MONGO_DB_NAME
import os

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client[MONGO_DB_NAME]

async def get_db() -> AsyncIOMotorDatabase:
    return db

async def get_openid(authorization: str = Header(...)) -> str:
    openid = verify_jwt(authorization)
    if not openid:
        raise HTTPException(status_code=401, detail="Invalid token")
    return openid

