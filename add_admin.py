#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti

from __future__ import absolute_import, division, print_function, \
    with_statement

import hashlib
import getopt
import sys
import pymysql.cursors


class Config_DB(object):
    #mysql
    mysql_host = '127.0.0.1'
    mysql_user = 'ss'
    mysql_pass = 'shadowsocks'
    mysql_db   = 'shadowsocks'


class Mysql_DB(object):

    instance = None

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        if Mysql_DB.instance is None:
            Mysql_DB.instance = Mysql_DB()
        return Mysql_DB.instance

    def _create_conn(self):
        connection = pymysql.connect(
            host=Config_DB.mysql_host,
            user=Config_DB.mysql_user,
            password=Config_DB.mysql_pass,
            db=Config_DB.mysql_db,
            charset='utf8'
            )
        return connection

    def add_user(self, email, password):
        connection = self._create_conn()

        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `admin` (`email`, `password`) VALUES (%s, %s)"
                cursor.execute(sql, (email, password))
                connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close()

        print('success')

def print_help():
    print('''usage: python add_admin.py [OPTION]...
A tools to generate shadowsocks-admin's administrator secured password.

options:
    -u, --user             administrator's email to login
    -p, --password         administrator's password to login

Project address: <http://git.oschina.net/arrti/shadowsocks-admin/tree/dev>
''')

def main(argv):

    shortopts = 'hu:p:'
    longopts = ['help','user=', 'password=']
    email = None
    password = None
    
    try:
        optlist, args = getopt.getopt(argv[1:], shortopts, longopts)
        for key, value in optlist:
            if key in ('-u', '--user'):
                email = value

            if key in ('-p', '--password'):
                password = value

            if key in ('-h', '--help'):
                print_help()
                sys.exit(0)
    except getopt.GetoptError as e:
        print(e)
        print_help()
        sys.exit(1)

    if email is None or password is None:
        print('email or password not specified')
        print_help()
        sys.exit(2)

    # generate secured password
    secure_password = hashlib.sha1(email + password).hexdigest()
    secure_password_md5 = hashlib.md5(secure_password).hexdigest()

    # insert into database
    m = Mysql_DB.get_instance()
    m.add_user(email, secure_password_md5)

if __name__ == '__main__':
    main(sys.argv)