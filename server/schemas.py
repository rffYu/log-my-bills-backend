# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List
from pydantic import BaseModel

class RecordModel(BaseModel):
    id: str
    user_id: str
    user_category_id: str
    amount: float
    type: str
    description: str
    datetime: datetime
    created_at: datetime
    updated_at: datetime

class RecordList(BaseModel):
    records: List[RecordModel]

