About shadowsocks-python manyuser
=================================
This is a multi-user version of shadowsocks-python. Requires a mysql database.

Install
-------
1. install MySQL 5.x.x
2. install cymysql library by `pip install cymysql`
3. create a database named `shadowsocks`
4. import `shadowsocks.sql` into `shadowsocks`
5. copy `config_example.py` to `config.py` and edit it following the notes inside (but DO NOT delete the example file)
6. TestRun `cd shadowsocks && python servers.py` (not server.py)

if no exception the server will startup. By default logging is enabled.
You should be able to see this kind of thing in `shadowsocks.log`(default log file name)
```
May 25 23:03:16 INFO Multi-User Shadowsocks Server Starting...
May 25 23:03:17 INFO Current Server Version: 2.8.3-83-gf8dd2f8

May 25 23:03:18 INFO db skipped port 443
May 25 23:03:19 INFO db downloaded
May 25 23:03:19 INFO Server Added:   P[XXXX], M[aes-256-cfb], E[XXX@XXX.XXX]
```

Explanation of the log output
-----------------------------
When adding server:

`P[XXX]` client port (assigned by database)

`M[XXX]` client encryption method

`E[XXX]` client email address

When data connection being established/blocked

`U[XXX]` client port (assigned by database)

`RP[XXX]` remote port (the port the client wants to connect)

`A[XXX-->XXX]` from the client address to the remote address

Database user table column
--------------------------
`passwd` server pass

`port` server port

`t` last connecting time

`u` upload transfer

`d` download transfer

`method` encryption method

`transfer_enable` if u + d > transfer_enable this server will be stop (method del_server_out_of_bound_safe in dbtransfer.py)

Compatibility with other frontend UIs
-------------------------------------
It is compatible with [ss-panel](https://github.com/orvice/ss-panel).

Open source license
-------------------
This program is licensed under [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)