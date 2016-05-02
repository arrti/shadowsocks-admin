#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti

from __future__ import absolute_import, division, print_function, \
    with_statement

from ss_admin import app, db, redis
from ss_admin.models import User
from ss_admin import utils
from flask import render_template, jsonify
from sqlalchemy import func

import time, math


BYTE_TO_GIGABYTE = 1024 * 1024 * 1024

@app.route('/')
@app.route('/dashboard')
def dashboard():


    return render_template("dashboard.html",
            environment = app.config.get('ENVIRONMENT')
            )


@app.route('/dashboard_users_status')
def get_users_status():
    # users status
    now = time.time()
    active_ports = redis.connection.smembers('ports_to_stat')
    active_users = User.query.filter(User.service_enable == 1).\
        filter(User.upload_transfer + User.download_transfer < User.total_transfer).\
        filter(User.expire_date > now).\
        filter(User.server_port.in_(active_ports)).count()
    pending_users = User.query.filter(User.service_enable == 1).\
        filter(User.upload_transfer + User.download_transfer < User.total_transfer).\
        filter(User.expire_date > now).\
        filter(~User.server_port.in_(active_ports)).count()
    banned_users = User.query.filter(User.service_enable == 0).filter(User.expire_date > now).count()

    return jsonify(active=active_users, pending=pending_users, banned=banned_users)

@app.route('/dashboard_transfer_usage')
def get_transfer_usage():
    # transfer usage
    transfer_used = db.session.query(func.sum(User.upload_transfer + User.download_transfer)).scalar()
    transfer_usage= round(transfer_used / app.config.get('SERVER_INIT_TRANSFER') * 100, 1)
    return jsonify(transfer=str(transfer_usage))

@app.route('/dashboard_online_users')
@app.route('/dashboard_online_users/<int:page>')
def get_online_users(page = 1):
    now = time.time()
    expires = now - (app.config.get('ONLINE_LAST_MINUTES') * 60)
    total = User.query.filter(User.service_enable == 1).filter(User.last_active_time > expires).count()
    users = User.query.filter(User.service_enable == 1).filter(User.last_active_time > expires).paginate(page, app.config.get('TABLE_ITEMS_PER_PAGE'), False).items
    online_user = []
    for user in users:
        online_user.append({'id':user.id, 'email':user.email, \
                     'transfer': round(user.total_transfer / BYTE_TO_GIGABYTE, 2), \
                     'usage':round((user.upload_transfer + user.download_transfer) / user.total_transfer, 2)})

    total_page = int(math.ceil(total / app.config.get('TABLE_ITEMS_PER_PAGE')))
    page = utils.pagination(page, total_page)

    return jsonify(online=online_user, number=total, page=page)