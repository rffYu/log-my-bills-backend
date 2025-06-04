# -*- coding: utf-8 -*
from fastapi import FastAPI
from .handlers import auth, record


app = FastAPI()
app.include_router(auth.router)
app.include_router(record.router)

