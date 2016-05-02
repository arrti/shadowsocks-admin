#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://ss" \
                           ":" \
                           "shadowsocks" \
                           "@" \
                           "localhost/" \
                           "shadowsocks" \
                           "?charset=utf8"

# redis config
REDIS_URL = 'redis://:shadowsocks@localhost:6379/0'

SECRET_KEY = '\xf7\xf7\x9c~\x81|:\x95~0DOX~ZZ\xc0\x16\x9e\xbbh\xa3\xb7\xf9' # os.urandom(24)

ONLINE_LAST_MINUTES = 60
TABLE_ITEMS_PER_PAGE = 10

# net.ipv4.ip_local_port_range 32768,61000
MIN_SERVICE_PORT = 61000
MAX_SERVICE_PORT = 65000

HOST_URL = '127.0.0.1' # 'http://www.ixmwd.com'

# init transfer
USER_INIT_TRANSFER = 10 * 1024 * 1024 * 1024
SERVER_INIT_TRANSFER = 1000 * 1024 * 1024 * 1024

# mail config
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'smtp@gmail.com'
MAIL_PASSWORD = 'smtp'

ENVIRONMENT = 'Debug' # 生产模式为'Production'