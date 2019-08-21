#! /usr/bin/env python
''' checker class to do the connection tests '''

import os
import time
import errno
import json
import asyncio
import aioping
import aioredis

from checkcon import TEXT_REDIS_UNABLE2CONNECT, TEXT_WRONG_INPUT

from .helper import validate_uri

class Checker():
    ''' class to check connections '''
    def __init__(self, data_str, redis_str, interval=10, timeout=5):
        self.interval = interval
        self.timeout = timeout
        self.redis_str = redis_str
        self.key = data_str
        self.proto, self.host, self.port = validate_uri(data_str)

    async def __call__(self):
        if self.proto is False or self.host is False or self.port is False:
            print(TEXT_WRONG_INPUT.format(string=self.key))
            return False

        try:
            redis = await aioredis.create_redis_pool(self.redis_str)
        except (aioredis.RedisError, OSError) as e:
            print(TEXT_REDIS_UNABLE2CONNECT + str(e))
            return False

        while True:
            start_time = time.time()
            if self.proto == 'tcp':
                data = await self.tcp()
            elif self.proto == 'ping':
                data = await self.ping()

            await self.post_2_redis(redis, data)

            end_time = time.time()
            duration = end_time - start_time
            await asyncio.sleep(self.interval - duration)

    async def tcp(self):
        ''' see if we can establish a tcp connection '''
        result = {}
        conn = asyncio.open_connection(self.host, self.port)
        try:
            start = time.time()
            _, writer = await asyncio.wait_for(conn, timeout=self.timeout)
            end = time.time()
        except asyncio.TimeoutError:
            result['status'] = False
            result['error'] = errno.ETIMEDOUT
            result['delay'] = -1
            result['msg'] = os.strerror(errno.ETIMEDOUT)
        except OSError as exception:
            result['status'] = False
            result['delay'] = -1
            if exception.errno is not None:
                result['error'] = exception.errno
                result['msg'] = os.strerror(exception.errno)
            else:
                result['error'] = -1
                result['msg'] = str(exception)
        else:
            result['status'] = True
            result['error'] = 0
            result['msg'] = 'OK'
            result['delay'] = (end - start) * 1000
            writer.close()
        return result

    async def ping(self):
        ''' ping the host '''
        result = {}
        try:
            result['delay'] = await aioping.ping(self.host, self.timeout) * 1000
        except TimeoutError:
            result['status'] = False
            result['error'] = errno.ETIMEDOUT
            result['delay'] = -1
            result['msg'] = os.strerror(errno.ETIMEDOUT)
        except OSError as exception:
            result['status'] = False
            result['delay'] = -1
            if exception.errno is not None:
                result['msg'] = os.strerror(exception.errno)
                result['error'] = exception.errno
            else:
                result['msg'] = str(exception)
                result['error'] = -1
        else:
            result['status'] = True
            result['error'] = 0
            result['msg'] = 'OK'
        return result

    async def post_2_redis(self, redis, data):
        ''' post state to redis '''
        j = json.dumps(data)
        try:
            _ = await redis.execute('SETEX', self.key, self.interval, j)
        except (aioredis.RedisError, OSError) as e:
            print(TEXT_REDIS_UNABLE2CONNECT + str(e))
