# -*- coding: utf-8 -*
from fastapi import FastAPI
from .handlers import auth, record, admin_report


app = FastAPI()
app.include_router(auth.router)
app.include_router(record.router)
app.include_router(admin_report.router)

