#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti

from wtforms import validators, StringField
from flask.ext.wtf import Form


class login(Form):
    email = StringField('email', validators=[
        validators.DataRequired(),
        validators.Length(min=4),
        validators.Email()
    ])

    password = StringField('password', validators=[
        validators.DataRequired(),
        validators.Length(min=6, max=32)
    ])