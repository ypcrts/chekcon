#! /usr/bin/env python
''' test cmd '''

import os
import asyncio
import pytest

#from checkcon import ERROR_ENV_NOT_SET, ERROR_CONFIG_NOLIST, ERROR_CONFIG_EMPTY

from checkcon.cmd import handle_sigterm

def test_handle_sigterm():
    ''' test handle_sigterm function '''
    async def start_handle_sigterm():
        handle_sigterm()

    loop = asyncio.get_event_loop()
    loop.create_task(start_handle_sigterm())
    loop.run_forever()
    assert loop.is_running() is False
    loop.close()
