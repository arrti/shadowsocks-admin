#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti

# from __future__ import absolute_import, division, print_function, \
#     with_statement

from ss_admin import app, login_manager
from ss_admin.models import Admin
from ss_admin.forms import admin
from ss_admin.lib import verification_code

from flask import render_template, request, session, redirect, url_for, g, flash
from flask.ext.wtf import Form
from flask.ext.login import login_required, login_user, logout_user, current_user
import StringIO, hashlib

@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        form = Form()
        return render_template('login.html',
                               form=form
                               )
    elif request.method == 'POST':
        form = admin.login()
        if form.validate_on_submit():
            user = Admin.query.filter_by(password=form.password.data).first()
            if user:
                login_user(user, remember=False)
                return redirect(request.args.get('next') or url_for('index'))

        flash(u'email or password not correct', 'error')
        return redirect('login')

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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/index')
@login_required
def index():
    return redirect(url_for('dashboard'))

@login_manager.user_loader
def load_user(id):
    return Admin.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

