#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti

from __future__ import absolute_import, division, print_function, \
    with_statement

from ss_admin import app, db, utils, ss, mail
from ss_admin.models import User
from ss_admin.forms import manage
from flask import render_template, jsonify, request, g
from flask.ext.wtf import Form
from flask.ext.login import login_required
from flask.ext.mail import Message

import random

BYTE_TO_GIGABYTE = 1024 * 1024 * 1024

@app.route('/user_add', methods=['POST', 'GET'])
@login_required
def user_add():
    if request.method == 'POST':
        form = manage.AddUserForm()
        if form.validate_on_submit():
            if add_new_user(form):
                try:
                    ss.add_port(form.port.data, form.password.data)
                except:
                    import traceback
                    traceback.print_exc()
                    return jsonify(info='error:Add service on port[%s] failed' % form.port.data)
                return jsonify(info='success', service={'port': form.port.data, 'password': form.password.data})
            else:
                return jsonify(info='error:Add new user failed')
        else:
            return jsonify(info='error:Form validate failed')

    elif request.method == 'GET':
        form = Form()
        return render_template("add.html",
                form=form,
                email=g.user.get_username(),
                host=app.config.get('HOST_URL'),
                port = get_valid_port(),
                password = utils.generate_password(),
                transfer = app.config.get('USER_INIT_TRANSFER') // BYTE_TO_GIGABYTE,
                environment = app.config.get('ENVIRONMENT'),
                active_user_new = 'active'
                )

def add_new_user(form):
    try:
        u = {}
        u['email'] = form.email.data
        u['port'] = form.port.data
        u['passwd'] = form.password.data
        u['t'] = int(form.transfer.data) * BYTE_TO_GIGABYTE
        u['d'] = form.download.data
        u['u'] = form.upload.data
        u['effective_date'] = utils.format_date(form.effective.data, True)
        u['expire_date'] = utils.format_date(form.expire.data, True)
        u['enable'] = form.enable.data

        user = User(u)
        db.session.add(user)
        db.session.commit()
    except:
        import traceback
        traceback.print_exc()
        return False

    return True

def get_valid_port():
    used_ports = db.session.query(User.server_port).all()
    original_ports = set(range(app.config.get('MIN_SERVICE_PORT'), app.config.get('MAX_SERVICE_PORT')))
    if used_ports:
        used_ports = set(p[0] for p in used_ports)
        return random.choice(list(original_ports.difference(used_ports)))
    else:
        return random.choice(list(original_ports))
