#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti

from wtforms import validators, StringField, IntegerField
from flask.ext.wtf import Form


class UserInfoForm(Form):
    id = IntegerField('id')

    email = StringField('email', validators=[
        validators.DataRequired(),
        validators.Length(min=4),
        validators.Email()
    ])

    transfer = StringField('transfer', validators=[
        validators.DataRequired(),
        validators.Regexp('^(?:[1-9]\d*|0)$')
    ])

    expire = StringField('expire', validators=[
        validators.DataRequired()
    ])

class ServiceSettingForm(Form):
    id = IntegerField('id')

    upload = StringField('upload', validators=[
        validators.DataRequired(),
        validators.Regexp('^(?:[1-9]\d*|0)$')
    ])

    download = StringField('download', validators=[
        validators.DataRequired(),
        validators.Regexp('^(?:[1-9]\d*|0)$')
    ])

    password = StringField('password', validators=[
        validators.DataRequired(),
        validators.Length(min=6, max=64)
    ])

    port = IntegerField('port', validators=[
        validators.DataRequired()
    ])

    enable = StringField('enable', validators=[
        validators.DataRequired(),
        validators.Regexp("^[1|0]$")
    ])

class AddUserForm(Form):
    email = StringField('email', validators=[
        validators.DataRequired(),
        validators.Length(min=4),
        validators.Email()
    ])

    transfer = StringField('transfer', validators=[
        validators.DataRequired(),
        validators.Regexp('^(?:[1-9]\d*|0)$')
    ])

    upload = StringField('upload', validators=[
        validators.DataRequired(),
        validators.Regexp('^(?:[1-9]\d*|0)$')
    ])

    download = StringField('download', validators=[
        validators.DataRequired(),
        validators.Regexp('^(?:[1-9]\d*|0)$')
    ])

    effective = StringField('effective', validators=[
        validators.DataRequired()
    ])

    expire = StringField('expire', validators=[
        validators.DataRequired()
    ])

    password = StringField('password', validators=[
        validators.DataRequired(),
        validators.Length(min=6, max=64)
    ])

    port = IntegerField('port', validators=[
        validators.DataRequired()
    ])

    enable = StringField('enable', validators=[
        validators.DataRequired(),
        validators.Regexp("^[1|0]$")
    ])

class SearchForm(Form):
    port = IntegerField('port', validators=[
        validators.DataRequired()
    ])
    email = StringField('email', validators=[
        validators.DataRequired(),
        validators.Length(min=4),
        validators.Email()
    ])

class SearchPortForm(Form):
    port = IntegerField('port')
    email = StringField('email')

class SearchEmailForm(Form):
    port = StringField('port')
    email = StringField('email', validators=[
        validators.DataRequired(),
        validators.Length(min=4),
        validators.Email()
    ])


