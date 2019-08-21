#! /usr/bin/env python
''' main cmd routine '''

import asyncio
import uvloop

from . import VAR_REDIS_STR, VAR_CONFIG_FILE, DEFAULT_REDIS_STR, DEFAULT_CONFIG_FILE
from .helper import validate_uri, read_env, read_config_file
from .checker import Checker

def create_tasks(loop, redis_conn_str, config_list):
    ''' create task on loop, for every item in the config_list '''
    tasks = {}
    for i in config_list:
        pre_proto, pre_host, pre_port = validate_uri(i)
        if pre_proto is not False or pre_host is not False or pre_port is not False:
            check = Checker(pre_proto, pre_host, pre_port, redis_conn_str)
            tasks[i] = loop.create_task(check())
    return tasks

def checkcon():
    ''' main function '''
    loop = uvloop.new_event_loop()
    asyncio.set_event_loop(loop)

    redis_conn_str = read_env(VAR_REDIS_STR, default=DEFAULT_REDIS_STR)
    config_file = read_env(VAR_CONFIG_FILE, default=DEFAULT_CONFIG_FILE)
    config = read_config_file(config_file)

    create_tasks(loop, redis_conn_str, config)

    try:
        pending = asyncio.Task.all_tasks()
        loop.run_until_complete(asyncio.gather(*pending))
    except KeyboardInterrupt:
        print('')
