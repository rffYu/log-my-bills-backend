# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
from typing import Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from server.utils import mock_db

USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"


async def get_mock_records(openid: str, since: Optional[datetime]) -> list[dict]:
    records = mock_db.get_mock_records_json_file()

    filtered = [
        r for r in records
        if r.get("openid") == openid and (
            not since or datetime.fromisoformat(r["updatedAt"].replace("Z", "+00:00")) >= since
        )
    ]
    return filtered


async def get_db_records(openid: str, since: Optional[datetime], db: AsyncIOMotorDatabase) -> list[dict]:
    query = {"openid": openid}
    if since:
        query["updatedAt"] = {"$gte": since}
    cursor = db.records.find(query)
    return await cursor.to_list(length=100)


async def get_records(openid: str, since: Optional[datetime], db: Optional[AsyncIOMotorDatabase] = None):
    if USE_MOCK:
        return await get_mock_records(openid, since)
    return await get_db_records(openid, since, db)

