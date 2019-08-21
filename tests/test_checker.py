#! /usr/bin/env python
''' test checker '''

import asyncio
import socket
import json
import pytest
import aioredis

from checkcon.checker import Checker

def test_checker():
    ''' test class checker '''
    right_key = 'tcp_127.0.0.1_80'
    redis = 'redis://localhost'
    class_object = Checker(right_key, redis)
    assert isinstance(class_object, object) is True
    assert class_object.proto == 'tcp'
    assert class_object.host == '127.0.0.1'
    assert class_object.port == 80
    assert class_object.redis_str == redis
    assert class_object.key == right_key

@pytest.mark.asyncio
async def test_call_break():
    ''' test call method , break no redis'''
    redis_str = 'redis://localhost:8888'
    right_key = 'tcp_127.0.0.1_7891'

    # redis not exists
    checker = Checker(right_key, redis_str)
    task = asyncio.create_task(checker())
    status = await asyncio.gather(task)
    assert status[0] is False

@pytest.mark.asyncio
async def test_call_cancel():
    ''' test call method, cancel task '''
    redis_str = 'redis://localhost'
    right_key = 'tcp_127.0.0.1_7891'
    checker = Checker(right_key, redis_str)
    task = asyncio.create_task(checker())
    task.cancel()

@pytest.mark.asyncio
async def test_tcp():
    ''' test tcp method '''
    redis_str = 'redis://localhost'
    test_port = 7891
    localhost = '127.0.0.1'
    right_key = 'tcp_' + localhost + '_' + str(test_port)

    # closed port
    checker = Checker(right_key, redis_str)
    result = await checker.tcp()
    assert result['msg'] == 'Connection refused'
    assert result['status'] is False
    assert result['error'] == 111
    assert result['delay'] == -1

    # open port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((localhost, test_port))
    sock.listen(1)
    result = await checker.tcp()
    assert result['msg'] == 'OK'
    assert result['status'] is True
    assert result['error'] == 0
    sock.close()

@pytest.mark.asyncio
async def test_ping():
    ''' test ping method '''
    redis_str = 'redis://localhost'
    test_port = 0
    localhost = '127.0.0.1'
    right_key = 'ping_' + localhost + '_' + str(test_port)

    checker = Checker(right_key, redis_str)
    result = await checker.ping()
    assert result['msg'] == \
            'Operation not permitted - Note that ICMP messages \
can only be sent from processes running as root.'
    assert result['status'] is False
    assert result['error'] == -1
    assert result['delay'] == -1

@pytest.mark.asyncio
async def test_post_2_redis():
    ''' test post_2_redis '''
    redis_str = 'redis://localhost'
    test_data = {}
    test_json = json.dumps(test_data)

    checker = Checker('tcp', 'localhost', '80', redis_str)
    redis = await aioredis.create_redis_pool(redis_str)
    await checker.post_2_redis(redis, test_data)

    result = await redis.execute('GET', checker.key)
    redis.close()
    await redis.wait_closed()
    assert result.decode("utf-8") == test_json
