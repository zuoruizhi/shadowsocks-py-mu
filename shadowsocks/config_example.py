# !!! Please rename this file as config.py BEFORE editing it !!!

import logging
# !!! Do NOT touch this line !!!
CONFIG_VERSION = '20160618-1'

# Database Config
MYSQL_HOST = 'mengsky.net'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASS = 'root'
MYSQL_DB = 'shadowsocks'
MYSQL_USER_TABLE = 'user'
MYSQL_TIMEOUT = 30

# It is not necessary to change the password if you only listen on 127.0.0.1
MANAGE_PASS = 'passwd'
# if you want manage in other server you should set this value to global ip
MANAGE_BIND_IP = '127.0.0.1'
# make sure this port is idle
MANAGE_PORT = 23333

# SS Panel API Setting
# Version of Panel: V2 or V3. V2 not support API thus no need to change
# anything in the following settings
PANEL_VERSION = 'V2'
API_URL = 'http://domain/mu'
# API Key of SS-Panel V3 (you can find this in the .env file)
API_PASS = 'mupass'
NODE_ID = '1'
CHECKTIME = 15
SYNCTIME = 600

# Choose True if you want to use custom method
CUSTOM_METHOD = True

# BIND IP
# if you want to bind ipv4 and ipv6 please use '::'
# if you want to bind only all of ipv4 please use '0.0.0.0'
# if you want to bind a specific IP you may use something like '4.4.4.4'
SS_BIND_IP = '::'
# This default method will be replaced by database record if applicable
SS_METHOD = 'aes-256-cfb'
# Choose whether enforce Shadowsocks One Time Auth (OTA)
# OTA will still be enabled for the client if it sends an AUTH Address type(0x10)
SS_OTA = False
# Skip listening these ports
SS_SKIP_PORTS = ['80']
# Ban these outbound ports
# Members should be INTEGERS
SS_BAN_PORTS = [22, 23, 25]

# Shadowsocks Time Out
# It should > 180s as some protocol has keep-alive packet of 3 min, Eg.: bt
SS_TIMEOUT = 185
# Shadowsocks TCP Fastopen (Some OS may not support this, Eg.: Windows)
SS_FASTOPEN = False
# Shadowsocks verbose
SS_VERBOSE = False
# Banned Target IP List
SS_FORBIDDEN_IP = []

# LOG CONFIG
LOG_ENABLE = True
# Available Log Level: logging.NOTSET|DEBUG|INFO|WARNING|ERROR|CRITICAL
LOG_LEVEL = logging.INFO
LOG_FILE = 'shadowsocks.log'
# The following format is the one suggested for debugging
# LOG_FORMAT = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
LOG_DATE_FORMAT = '%b %d %H:%M:%S'
