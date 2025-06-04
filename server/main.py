# -*- coding: utf-8 -*-
import argparse
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()
import os
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parents[1].absolute()))
from server.api import handlers
from server.api.app import app
from server.utils import logger


@app.get("/")
async def read_root():
    return {"message": "Hello OLD World"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("address", type=str, help="Address of unicorn server")
    args = parser.parse_args()

    logger.initialize()

    # setup server
    host = args.address[: args.address.find(':')]
    port = int(args.address[args.address.find(':')+1:])
    uvicorn_config = uvicorn.Config("main:app", host=host, port=port, log_level="info")
    server = uvicorn.Server(uvicorn_config)
    server.run()
else:
    logger.initialize()

