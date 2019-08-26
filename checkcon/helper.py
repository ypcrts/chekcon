#! /usr/bin/env python
''' contains basic functions '''

import sys
import os
import json
import ipaddress
from fqdn import FQDN

from . import ERROR_ENV_NOT_SET, ERROR_CONFIG_NOLIST, ERROR_CONFIG_EMPTY,\
        ERROR_CONFIG_NO_JSON, ERROR_CONFIG_UNABLE_READ
from . import TEXT_EMPTY_LIST, TEXT_NOT_LIST, TEXT_VARIABLE_NOT_SET

def i_am_root(root=0):
    ''' check if I am root '''
    if os.geteuid() == root:
        return True
    return False

def validate_proto(proto):
    ''' check if given proto is valid '''
    if proto not in ['tcp', 'ping']:
        proto = False
    return proto

def validate_host(host):
    ''' check if the given host is a valid ip, hostname '''
    try:
        ipaddress.ip_address(host)
    except ValueError:
        if not FQDN(host).is_valid:
            host = False
    return host

def validate_port(port):
    ''' check if the given port is valid '''
    try:
        port = int(port)
        if port < 1 or port > 65536:
            raise ValueError
    except ValueError:
        port = False

    return port

def validate_uri(uri):
    ''' check if the given uri is valid '''
    proto = False
    host = False
    port = False

    fields = uri.split('_')

    if len(fields) == 3:
        proto = validate_proto(fields[0])
        host = validate_host(fields[1])
        port = validate_port(fields[2])
    elif len(fields) == 2 and fields[0] == 'ping':
        if i_am_root():
            proto = validate_proto(fields[0])
            host = validate_host(fields[1])
            port = -1

    return proto, host, port

def read_env(name, default=None):
    ''' read the env given env variable '''
    if default is None:
        variable = os.getenv(name)
    else:
        variable = os.getenv(name, default)

    if variable is None:
        print(TEXT_VARIABLE_NOT_SET.format(name=name))
        sys.exit(ERROR_ENV_NOT_SET)

    return variable

def is_config_list(config):
    ''' is the configuration a list '''
    if not isinstance(config, list):
        print(TEXT_NOT_LIST)
        sys.exit(ERROR_CONFIG_NOLIST)

    if not config:
        print(TEXT_EMPTY_LIST)
        sys.exit(ERROR_CONFIG_EMPTY)

    return True

def read_config_file(file_name):
    ''' read config file and resturn struct '''
    try:
        with open(file_name, 'r') as fh:
            config = json.load(fh)
    except ValueError as e:
        print('Unable to parse json: ' + str(e))
        sys.exit(ERROR_CONFIG_NO_JSON)
    except (PermissionError, FileNotFoundError) as e:
        print(str(e))
        sys.exit(ERROR_CONFIG_UNABLE_READ)

    is_config_list(config)
    return config
