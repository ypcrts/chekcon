#! /usr/bin/env python
''' main cmd routine '''

import signal
import asyncio
import uvloop

from . import VAR_REDIS_STR, VAR_CONFIG_FILE, DEFAULT_REDIS_STR, DEFAULT_CONFIG_FILE
from .helper import read_env, read_config_file
from .checker import Checker


def handle_sigterm():
    ''' close all task if sigterm is received '''
    loop = asyncio.get_running_loop()
    loop.stop()

def create_tasks(loop, redis_conn_str, config_list):
    ''' create task on loop, for every item in the config_list '''
    for i in config_list:
        check = Checker(i, redis_conn_str)
        loop.create_task(check())

def checkcon():
    ''' main function '''
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)

    redis_conn_str = read_env(VAR_REDIS_STR, default=DEFAULT_REDIS_STR)
    config_file = read_env(VAR_CONFIG_FILE, default=DEFAULT_CONFIG_FILE)
    config = read_config_file(config_file)

    create_tasks(loop, redis_conn_str, config)

    loop.add_signal_handler(signal.SIGTERM, handle_sigterm)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print('')
