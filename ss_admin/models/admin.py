#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti

from __future__ import absolute_import, division, print_function, \
    with_statement

from ss_admin import db


class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column('id', db.Integer, primary_key=True, nullable=False, autoincrement=True)
    email = db.Column('email', db.VARCHAR(128), nullable=True, index=True)
    password = db.Column('password', db.VARCHAR(32), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def get_username(self):
        return self.email