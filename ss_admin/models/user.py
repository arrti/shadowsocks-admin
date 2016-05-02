#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti

from __future__ import absolute_import, division, print_function, \
    with_statement

from ss_admin import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column('id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = db.Column('email', db.VARCHAR(128), nullable=False, index=True)
    login_pass = db.Column('user_pass', db.VARCHAR(32), nullable=True)
    server_port = db.Column('port', db.Integer, nullable=False, index=True)
    server_pass = db.Column('passwd', db.VARCHAR(32), nullable=False)
    total_transfer = db.Column('t', db.Integer, nullable=False)
    download_transfer = db.Column('d', db.Integer, nullable=False)
    upload_transfer = db.Column('u', db.Integer, nullable=False)
    service_enable = db.Column('enable', db.Integer, nullable=False)
    effective_date = db.Column('effective_date', db.Integer, nullable=False)
    expire_date = db.Column('expire_date', db.Integer, nullable=False)
    last_active_time = db.Column('last_active_time', db.Integer, nullable=True)

    def __init__(self, user):
        self.email = user['email']
        self.login_pass = user.get('user_pass', '')
        self.server_port = user['port']
        self.server_pass = user['passwd']
        self.total_transfer = user['t']
        self.download_transfer = user['d']
        self.upload_transfer = user['u']
        self.service_enable = user['enable']
        self.effective_date = user['effective_date']
        self.expire_date = user['expire_date']
        self.last_active_time = user.get('last_active_date', '')


if __name__ == '__main__':
    pass