''' checkcon module '''

#---------------------------------------------
# gloabl variables

# enviorment variable names
VAR_REDIS_STR = 'CHECKCON_REDIS_STR'
VAR_CONFIG_FILE = 'CHECKCON_CONFIG_FILE'

# default values
DEFAULT_CONFIG_FILE = '/config.json'
DEFAULT_REDIS_STR = 'redis://localhost'

#---------------------------------------------
# gloabl variables

# basic
ERROR_ENV_NOT_SET = 1

# config
ERROR_CONFIG_NOLIST = 10
ERROR_CONFIG_EMPTY = 11


#---------------------------------------------
# text
TEXT_NOT_LIST = 'json not contain a list'
TEXT_EMPTY_LIST = 'json is empty'

TEXT_VARIABLE_NOT_SET = "environment variable {name} is not set."

TEXT_REDIS_UNABLE2CONNECT = 'unable to connect to redis: '
