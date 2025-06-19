# -*- coding: utf-8 -*-
import logging
import asyncio
from typing import Optional
from datetime import datetime
import io
import itertools
import pandas as pd
from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from server.schemas import RecordList
from server.deps import get_db, get_openid
from server.data import record_data
from .. import routing_table

logger = logging.getLogger("api_handler")

router = APIRouter()

@router.get(routing_table.USER_EXPORT_EXCEL)
async def get_excel_export(
    month: Optional[str] = Query(None, description="Filter by month"),
    db: AsyncIOMotorDatabase = Depends(get_db),
    openid: str = Depends(get_openid),
):
    if not month:
        return {"success": False, "error": "Missing month"}

    try:
        # Parse year and month
        month_date = datetime.strptime(month, "%Y-%m")

        # Compute first and last date of the month
        start_date = datetime(month_date.year, month_date.month, 1)
        if month_date.month == 12:
            end_date = datetime(month_date.year + 1, 1, 1)
        else:
            end_date = datetime(month_date.year, month_date.month + 1, 1)

        records = await record_data.get_records(openid, db=db)

        if not records:
            return {"success": False, "error": "No records found"}

        # Format into DataFrame
        df = pd.DataFrame(records)
        df.sort_values(by="datetime", inplace=True)

        # Convert to Excel in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Records")

        output.seek(0)

        filename = f"records_{month}.xlsx"
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
        return StreamingResponse(output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)

    except Exception as e:
        logger.exception("Failed to export Excel")
        return {"success": False, "error": str(e)}

