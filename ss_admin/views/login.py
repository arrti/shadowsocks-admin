#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti

from __future__ import absolute_import, division, print_function, \
    with_statement

from ss_admin import app
from ss_admin.models import Admin
from ss_admin.forms import admin
from ss_admin.lib import verification_code

from flask import render_template, request, session, jsonify
from flask.ext.wtf import Form
import os, StringIO


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        form = Form()
        # session['verification_code'], path = gen_code()
        # gen_code()
        return render_template('login.html',
                               form=form
                               )

@app.route('/v_code')
def code():
    vc = verification_code.VerificationCode()
    session['verification_code'], image = vc.generate()
    buf = StringIO.StringIO()
    image.save(buf, 'JPEG', quality=70)
    buf_str = buf.getvalue()
    response = app.make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    return response

