from pydantic import BaseModel
from typing import List

class RecordModel(BaseModel):
    user_id: str
    user_category_id: str
    amount: float
    type_: int
    description: str
    record_time: str
    create_time: str
    update_time: str

class RecordList(BaseModel):
    records: List[RecordModel]

