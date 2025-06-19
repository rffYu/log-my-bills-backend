# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
from typing import Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from server.utils import mock_db

USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"


async def get_mock_records(openid: str, since: Optional[datetime]=None) -> list[dict]:
    records = mock_db.get_mock_records_json_file()

    filtered = [
        r for r in records
        if r.get("user_id") == openid and (
            not since or datetime.fromisoformat(r["updated_at"].replace("Z", "+00:00")) >= since
        )
    ]
    return filtered


async def get_db_records(openid: str, db: AsyncIOMotorDatabase, since: Optional[datetime]=None) -> list[dict]:
    query = {"user_id": openid}
    if since:
        query["updated_at"] = {"$gte": since}
    cursor = db.records.find(query)
    return await cursor.to_list(length=100)


async def get_records(openid: str, since: Optional[datetime]=None, db: Optional[AsyncIOMotorDatabase]=None):
    if USE_MOCK:
        return await get_mock_records(openid, since=since)
    return await get_db_records(openid, since=since, db=db)

