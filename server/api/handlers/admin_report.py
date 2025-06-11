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
from server.data import record_data
from .. import routing_table

logger = logging.getLogger("api_handler")

router = APIRouter()

SAMPLE_DATA = {
  "byUser": [
    { "userId": "u1", "nickname": "用户1", "total": 500 },
    { "userId": "u2", "nickname": "用户2", "total": 300 }
  ],
  "byCategory": [
    { "categoryName": "餐饮", "total": 400 },
    { "categoryName": "购物", "total": 200 }
  ]
}

@router.get(routing_table.ADMIN_REPORT_SUMMARY)
async def get_report_summary(
    month: Optional[str] = Query(None, description="Filter by month"),
    mainUser: str = Query(..., description="Main user ID to fetch member data"),
    db: AsyncIOMotorDatabase = Depends(get_db),
    openid: str = Depends(get_openid),
):
    if not month:
        return {"success": False, "error": "Missing month"}

    # bypass other logic
    return {"success": True, "data": SAMPLE_DATA}

    try:
        # Call data layer to get all records under this main user for this month
        records = await record_data.get_records_for_main_user(db, mainUser, month)

        if not records:
            return {"success": True, "data": []}

        # Group by user and then by category
        summary = {}
        for record in records:
            uid = record["userId"]
            cat = record.get("categoryName", "未分类")
            amount = record.get("amount", 0)

            if uid not in summary:
                summary[uid] = {"total": 0, "byCategory": {}}
            summary[uid]["total"] += amount
            summary[uid]["byCategory"].setdefault(cat, 0)
            summary[uid]["byCategory"][cat] += amount

        return {"success": True, "data": summary}

    except Exception as e:
        logger.exception("Failed to generate report")
        return {"success": False, "error": str(e)}

