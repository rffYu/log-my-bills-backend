# -*- coding: utf-8 -*
from fastapi import FastAPI
from . import handlers


app = FastAPI()
app.include_router(handler.auth.router)
app.include_router(handlers.record.router)

