#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti

from wtforms import validators, StringField
from flask.ext.wtf import Form


class login(Form):
    email = StringField('email', validators=[
        validators.DataRequired(message='email is required'),
        validators.Length(min=4, message='email is too short'),
        validators.Email(message='email is invalid')
    ])

    password = StringField('password', validators=[
        validators.DataRequired(message='password is required'),
        validators.Length(min=6, max=32, message='password is required 6~32 characters')
    ])

    vcode = StringField('vcode', validators=[
        validators.DataRequired(message='verification code is required')
    ])