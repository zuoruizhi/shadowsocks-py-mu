#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 mengskysama
# Copyright 2016 Howard Liu
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys
import os
import logging
import time
# Check whether the config is correctly renamed
try:
    import config
except ImportError:
    print('[ERROR] Please rename `config.example.py` to `config.py` first!')
    sys.exit('config not found')
# For those system do not have thread (or _thread in Python 3)
try:
    import thread
except ImportError:
    import _dummy_thread as thread

# Output log at stdout as well as the log file
logging.basicConfig(format=config.LOG_FORMAT,
                    datefmt=config.LOG_DATE_FORMAT, stream=sys.stdout, level=config.LOG_LEVEL)
if config.LOG_ENABLE:
    logger = logging.getLogger()
    fileLogger = logging.FileHandler(config.LOG_FILE)
    fileLogger.setFormatter(logging.Formatter(config.LOG_FORMAT, datefmt=config.LOG_DATE_FORMAT))
    fileLogger.setLevel(config.LOG_LEVEL)
    logger.addHandler(fileLogger)

# Check whether the versions of config files match
try:
    import config_example
    if not hasattr(config, 'CONFIG_VERSION') or config.CONFIG_VERSION != config_example.CONFIG_VERSION:
        logging.error('Your configuration file is out-dated. Please update `config.py` according to `config.example.py`.')
        sys.exit('config out-dated')
except ImportError:
    logging.error('DO NOT delete the example configuration! Please re-upload it or use `git reset` to recover the file!')
    sys.exit('example config file missing')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
import manager
from dbtransfer import DbTransfer

if os.path.isdir('../.git'):
    import subprocess
    VERSION = subprocess.check_output(["git", "describe"])
else:
    VERSION = '3.0.1'


def main():
    configer = {
        'server': config.SS_BIND_IP,
        'local_port': 1081,
        'port_password': {},
        'method': config.SS_METHOD,
        'manager_address': '%s:%s' % (config.MANAGE_BIND_IP, config.MANAGE_PORT),
        'timeout': config.SS_TIMEOUT,
        'fast_open': config.SS_FASTOPEN,
        'verbose': config.SS_VERBOSE,
        'one_time_auth': config.SS_OTA,
        'forbidden_ip': config.SS_FORBIDDEN_IP,
        'banned_ports': config.SS_BAN_PORTS
    }
    logging.info('-----------------------------------------')
    logging.info('Multi-User Shadowsocks Server Starting...')
    logging.info('Current Server Version: %s' % VERSION)
    if config.PANEL_VERSION != 'V3':
        logging.warn('Not support ss-panel version: %s' % config.PANEL_VERSION)
        logging.warn('Please upgrade your ss-panel to V3 to enable all features.')
    thread.start_new_thread(manager.run, (configer,))
    time.sleep(1)
    thread.start_new_thread(DbTransfer.thread_db, ())
    time.sleep(1)
    thread.start_new_thread(DbTransfer.thread_push, ())
    
    while True:
        time.sleep(100)


if __name__ == '__main__':
    main()
