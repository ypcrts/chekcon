#! /usr/bin/env python
''' test helpers '''

import os
import pytest

from checkcon import ERROR_ENV_NOT_SET, ERROR_CONFIG_NOLIST, ERROR_CONFIG_EMPTY

from checkcon.helper import i_am_root, validate_proto, validate_host, validate_port,\
    validate_uri, read_env, is_config_list

def test_i_am_root():
    ''' test i_am_root '''
    assert i_am_root() is False

def test_validate_proto():
    ''' test validate_proto '''
    assert validate_proto('tcp') == 'tcp'
    assert validate_proto('ping') == 'ping'
    assert validate_proto('udp') is False
    assert validate_proto(['udp', 'udp']) is False
    assert validate_proto(['tcp', 'ping']) is False

def test_validate_host():
    ''' test validate_host '''
    test_data = [
        ('___', False),
        ('w_w_w.example.com', False),
        ('example.com', True),
        ('::1', True),
        ('127.0.0.1', True),
        ('127.0.0.0.1', False),
        ('www.example.com', True)]

    for data, expectation in test_data:
        if expectation:
            assert validate_host(data) == data
        else:
            assert validate_host(data) is False

def test_validate_port():
    ''' test validate_port '''
    assert validate_port('8008') == 8008
    assert validate_port(443) == 443
    assert validate_port('test') is False
    pytest.raises(TypeError, validate_port, [22, 23])

def test_validate_uri():
    ''' test validate_uri '''
    assert validate_uri('tcp_www.google.com_80') ==\
                       ('tcp', 'www.google.com', 80)
    assert validate_uri('ping_www.google.com') ==\
                       (False, False, False)
    assert validate_uri('tcp_www.google.com') ==\
                       (False, False, False)
    assert validate_uri('ping_www.google.com_80') ==\
                       ('ping', 'www.google.com', 80)
    assert validate_uri('XXXX') ==\
                       (False, False, False)

def test_read_env():
    ''' test read_redis_str '''
    not_existing_variable = 'NOT_EXISTS'
    existing_variable = 'TEST_VARIABLE'
    test_string = 'test-string'
    default = 'default'

    # no env set, no default
    with pytest.raises(SystemExit) as e:
        read_env(not_existing_variable)
    assert e.value.code == ERROR_ENV_NOT_SET

    # no env set, set default
    assert read_env(not_existing_variable, default=default) == default

    # set env, no default
    os.environ[existing_variable] = test_string
    assert read_env(existing_variable) == test_string

    # set env, set default
    assert read_env(existing_variable, default=default) == test_string

def test_is_config_list():
    ''' test is_config_list '''
    # valid
    valid_list = ['string', 'string']
    assert is_config_list(valid_list) is True

    # empty list
    empty_list = []
    with pytest.raises(SystemExit) as e:
        is_config_list(empty_list)
    assert e.value.code == ERROR_CONFIG_EMPTY

    # no list
    no_list = ['string', 42, {}]
    for i in no_list:
        with pytest.raises(SystemExit) as e:
            is_config_list(i)
        assert e.value.code == ERROR_CONFIG_NOLIST
