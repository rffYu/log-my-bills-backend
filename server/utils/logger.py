# -*- coding: utf-8 -*-
# __author__ = 'Liu Anon'
import logging
import os
from typing import Optional
from threading import Lock

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s [-] %(message)s"
CONSOLE_LOG = True
# DEFAULT_LOG_FILE = os.path.join(Path(__file__), '..{sep}..{sep}..{sep}log{sep}tradeoff.log'.format(sep=os.sep))
DEFAULT_LOG_FILE = None
DEFAULT_LOG_LEVEL = logging.INFO
LOG_FILE_ENV_KEY = "LOG_FILE"
LOG_LEVEL_ENV_KEY = "LOG_LEVEL"

LOG_FILE = os.environ.get(LOG_FILE_ENV_KEY) or DEFAULT_LOG_FILE
LEVEL = int(os.environ.get(LOG_LEVEL_ENV_KEY) or DEFAULT_LOG_LEVEL)

init_lock = Lock()
rootLoggerInit = False
rootMultiProcessLoggerInit = False


def set_handler_format(handler) -> None:
    handler.setFormatter(logging.Formatter(LOG_FORMAT))


def init_logger(logger) -> None:
    logger.setLevel(LEVEL)

    if LOG_FILE is not None:
        fileHandler = logging.FileHandler(LOG_FILE)
        set_handler_format(fileHandler)
        logger.addHandler(fileHandler)

    if CONSOLE_LOG:
        consoleHandler = None

        # try to get StreamHandler
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                consoleHandler = handler
                break

        # if StreamHandler not exist
        if consoleHandler is None:
            consoleHandler = logging.StreamHandler()
            set_handler_format(consoleHandler)
            logger.addHandler(consoleHandler)
        else:
            set_handler_format(consoleHandler)


def initialize() -> None:
    global rootLoggerInit
    with init_lock:
        if not rootLoggerInit:
            init_logger(logging.getLogger())  # root logger
            rootLoggerInit = True


def get_logger(name: Optional[str]=None):
    initialize()
    return logging.getLogger(name)
