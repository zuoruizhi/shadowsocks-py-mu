#!/usr/bin/python
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

import logging
import cymysql
import time
import socket
import config
import json


class DbTransfer(object):

    instance = None

    def __init__(self):
        self.last_get_transfer = {}

    @staticmethod
    def get_instance():
        if DbTransfer.instance is None:
            DbTransfer.instance = DbTransfer()
        return DbTransfer.instance

    @staticmethod
    def send_command(cmd):
        data = ''
        try:
            cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            cli.settimeout(1)
            cli.sendto(cmd, ('%s' % config.MANAGE_BIND_IP, config.MANAGE_PORT))
            data, addr = cli.recvfrom(1500)
            cli.close()
            # TODO: bad way solve timed out
            time.sleep(0.05)
        except:
            logging.warn('send_command response')
        return data

    @staticmethod
    def get_servers_transfer():
        dt_transfer = {}
        cli = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        cli.settimeout(2)
        cli.sendto('transfer: {}', (config.MANAGE_BIND_IP, config.MANAGE_PORT))
        while True:
            data, addr = cli.recvfrom(1500)
            if data == 'e':
                break
            data = json.loads(data)
            # print data
            dt_transfer.update(data)
        cli.close()
        return dt_transfer

    def push_db_all_user(self):
        import urllib2, urllib
        import time
        dt_transfer = self.get_servers_transfer()

        if config.PANEL_VERSION == 'V2':
            query_head = 'UPDATE `user`'
            query_sub_when = ''
            query_sub_when2 = ''
            query_sub_in = None
            last_time = time.time()
            for id in dt_transfer.keys():
                query_sub_when += ' WHEN %s THEN `u`+%s' % (id, 0)  # all in d
                query_sub_when2 += ' WHEN %s THEN `d`+%s' % (id, dt_transfer[id])
                if query_sub_in is not None:
                    query_sub_in += ',%s' % id
                else:
                    query_sub_in = '%s' % id
            if query_sub_when == '':
                return
            query_sql = query_head + ' SET u = CASE port' + query_sub_when + \
                        ' END, d = CASE port' + query_sub_when2 + \
                        ' END, t = ' + str(int(last_time)) + \
                        ' WHERE port IN (%s)' % query_sub_in
            # print query_sql
            conn = cymysql.connect(host=config.MYSQL_HOST, port=config.MYSQL_PORT, user=config.MYSQL_USER,
                                   passwd=config.MYSQL_PASS, db=config.MYSQL_DB, charset='utf8')
            cur = conn.cursor()
            cur.execute(query_sql)
            cur.close()
            conn.commit()
            conn.close()
            if config.SS_VERBOSE:
                logging.info('db upload')
        else:
            if config.PANEL_VERSION == 'V3':
                i = 0
                for id in dt_transfer.keys():
                    string = ' WHERE `port` = %s' % id
                    conn = cymysql.connect(host=config.MYSQL_HOST, port=config.MYSQL_PORT, user=config.MYSQL_USER,
                                           passwd=config.MYSQL_PASS, db=config.MYSQL_DB, charset='utf8')
                    cur = conn.cursor()
                    cur.execute('SELECT id FROM %s%s '
                                % (config.MYSQL_USER_TABLE, string))
                    rows = []
                    for r in cur.fetchall():
                        rows.append(list(r))
                    cur.close()
                    conn.close()
                    if config.SS_VERBOSE:
                        logging.info('port:%s ----> id:%s' % (id, rows[0][0]))
                    tran = str(dt_transfer[id])
                    data = {'d': tran, 'node_id': config.NODE_ID, 'u': '0'}
                    url = config.API_URL + '/users/' + str(rows[0][0]) + '/traffic?key=' + config.API_PASS
                    data = urllib.urlencode(data)
                    req = urllib2.Request(url, data)
                    response = urllib2.urlopen(req)
                    the_page = response.read()
                    if config.SS_VERBOSE:
                        logging.info('%s - %s - %s' % (url, data, the_page))
                    i += 1
                # online user count
                data = {'count': i}
                url = config.API_URL + '/nodes/' + config.NODE_ID + '/online_count?key=' + config.API_PASS
                data = urllib.urlencode(data)
                req = urllib2.Request(url, data)
                response = urllib2.urlopen(req)
                the_page = response.read()
                if config.SS_VERBOSE:
                    logging.info('%s - %s - %s' % (url, data, the_page))

                # load info
                url = config.API_URL + '/nodes/' + config.NODE_ID + '/info?key=' + config.API_PASS
                f = open("/proc/loadavg")
                load = f.read().split()
                f.close()
                loadavg = load[0]+' '+load[1]+' '+load[2]+' '+load[3]+' '+load[4]
                f = open("/proc/uptime")
                time = f.read().split()
                uptime = time[0]
                f.close()
                data = {'load': loadavg, 'uptime': uptime}
                data = urllib.urlencode(data)
                req = urllib2.Request(url, data)
                response = urllib2.urlopen(req)
                the_page = response.read()
                if config.SS_VERBOSE:
                    logging.info('%s - %s - %s' % (url, data, the_page))
            else:
                if config.SS_VERBOSE:
                    logging.warn('Not support panel version: %s' % config.PANEL_VERSION)
                return


    @staticmethod
    def del_server_out_of_bound_safe(rows):
        for row in rows:
            server = json.loads(DbTransfer.get_instance().send_command(
                'stat: {"server_port":%s}' % row[0]))
            if server['stat'] != 'ko':
                if row[5] == 0 or row[6] == 0:
                    # stop disabled or switched-off user
                    logging.info(
                        'db stop server at port [%d] reason: disable' % row[0])
                    DbTransfer.send_command(
                        'remove: {"server_port":%d}' % row[0])
                elif row[1] + row[2] >= row[3]:
                    # stop user that exceeds bandwidth limit
                    logging.info(
                        'db stop server at port [%d] reason: out bandwidth' % row[0])
                    DbTransfer.send_command(
                        'remove: {"server_port":%d}' % row[0])
                elif server['password'] != row[4]:
                    # password changed
                    logging.info(
                        'db stop server at port [%d] reason: password changed' % row[0])
                    DbTransfer.send_command(
                        'remove: {"server_port":%d}' % row[0])
                else:
                    if not config.CUSTOM_METHOD:
                        row[7] = config.SS_METHOD
                    if server['method'] != row[7] :
                        # encryption method changed
                        logging.info(
                            'db stop server at port [%d] reason: encryption method changed' % row[0])
                        DbTransfer.send_command(
                            'remove: {"server_port":%d}' % row[0])
            else:
                if row[5] == 1 and row[6] == 1 and row[1] + row[2] < row[3]:
                    if config.MANAGE_BIND_IP != '127.0.0.1':
                        logging.info(
                            'db start server at port [%s] with password [%s] and method [%s]' % (row[0], row[4], row[7]))
                    if not config.CUSTOM_METHOD:
                        row[7] = config.SS_METHOD
                    DbTransfer.send_command(
                        'add: {"server_port": %d, "password":"%s", "method":"%s", "email":"%s"}' % (row[0], row[4], row[7], row[8]))

    @staticmethod
    def thread_db():
        socket.setdefaulttimeout(config.MYSQL_TIMEOUT)
        while True:
            try:
                rows = DbTransfer.pull_db_all_user()
                DbTransfer.del_server_out_of_bound_safe(rows)
            except Exception as e:
                if config.SS_VERBOSE:
                    import traceback
                    traceback.print_exc()
                logging.error('db thread except:%s' % e)
            finally:
                time.sleep(config.CHECKTIME)

    @staticmethod
    def thread_push():
        socket.setdefaulttimeout(config.MYSQL_TIMEOUT)
        while True:
            try:
                DbTransfer.get_instance().push_db_all_user()
            except Exception as e:
                import traceback
                if config.SS_VERBOSE:
                    traceback.print_exc()
                logging.warn('db thread except:%s' % e)
            finally:
                time.sleep(config.SYNCTIME)

    @staticmethod
    def pull_db_all_user():
        string = ''
        for index in range(len(config.SS_SKIP_PORTS)):
            port = config.SS_SKIP_PORTS[index]
            if config.SS_VERBOSE:
                logging.info('db skipped port %s' % port)
            if index == 0:
                string = ' WHERE `port`<>%s' % port
            else:
                string = '%s AND `port`<>%s' % (string, port)
        conn = cymysql.connect(host=config.MYSQL_HOST, port=config.MYSQL_PORT, user=config.MYSQL_USER,
                               passwd=config.MYSQL_PASS, db=config.MYSQL_DB, charset='utf8')
        cur = conn.cursor()
        cur.execute('SELECT port, u, d, transfer_enable, passwd, switch, enable, method, email FROM %s%s ORDER BY `port` ASC'
                    % (config.MYSQL_USER_TABLE, string))
        rows = []
        for r in cur.fetchall():
            rows.append(list(r))
        # Release resources
        cur.close()
        conn.close()
        if config.SS_VERBOSE:
            logging.info('db downloaded')
        return rows
