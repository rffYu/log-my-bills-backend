# -*- coding: utf-8 -*-
import logging
import asyncio
from typing import Optional
from datetime import datetime
import itertools
from fastapi import APIRouter, Depends, Query, Response
from motor.motor_asyncio import AsyncIOMotorDatabase
from server.schemas import RecordList
from server.deps import get_db, get_openid
from .. import routing_table

logger = logging.getLogger("api_handler")

router = APIRouter()


@router.post(routing_table.POST_RECORD)
async def save_records(
    data: RecordList,
    db: AsyncIOMotorDatabase = Depends(get_db),
    openid: str = Depends(get_openid),
):
    await db.records.delete_many({"openid": openid})
    for rec in data.records:
        await db.records.insert_one({**rec.dict(), "openid": openid})
    return {"success": True}


@router.get(routing_table.GET_RECORD)
async def get_records(
    since: Optional[datetime] = Query(None),
    db: AsyncIOMotorDatabase = Depends(get_db),
    openid: str = Depends(get_openid),
):
    query = {"openid": openid}
    if since:
        query["updatedAt"] = {"$gte": since}

    cursor = db.records.find(query)
    records = await cursor.to_list(length=100)
    return {"success": True, "updatedRecords": records}

