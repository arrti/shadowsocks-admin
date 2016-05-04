#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti

from __future__ import absolute_import, division, print_function, \
    with_statement

from ss_admin import app, db, redis, utils, ss
from ss_admin.models import User
from ss_admin.forms import manage
from flask import render_template, jsonify, request, g
from flask_wtf import Form

import time, math


BYTE_TO_GIGABYTE = 1024 * 1024 * 1024

@app.route('/manage')
def users():
    form = Form() # for csrf
    return render_template("manage.html",
            form = form,
            email = g.user.get_username(),
            environment = app.config.get('ENVIRONMENT'),
            active_user_user = 'active'
            )

@app.route('/user_manage', methods=['POST', 'GET'])
@app.route('/user_manage/<int:page>')
def get_users(page = 1):
    total = 0
    users = None
    if request.method == 'POST':
        port = 0
        email = 0
        if request.form['s'] == '1':
            form = manage.SearchPortForm()
        elif request.form['s'] == '2':
            form = manage.SearchEmailForm()
        elif request.form['s'] == '3':
            form = manage.SearchForm()
        else:
            return jsonify(info='error:Search Keywords can not be empty')
        if form.validate_on_submit():
            if form.port.data:
                port = 1
            if form.email.data:
                email = 2
            port_email = port | email
            if port_email == 1:
                # total = User.query.filter(User.server_port == form.port.data).count()
                users = User.query.filter(User.server_port == form.port.data).all()
            elif port_email == 2:
                # total = User.query.filter(User.email == form.email.data).count()
                users = User.query.filter(User.email == form.email.data).all()
            elif port_email == 3:
                # total = User.query.filter(User.server_port == form.port.data).filter(User.email == form.email.data).count()
                users = User.query.filter(User.server_port == form.port.data).filter(User.email == form.email.data).all()
        else:
            return jsonify(info='error:Search Keywords error')

    elif request.method == 'GET':
        # users status
        now = time.time()
        total = User.query.filter(User.expire_date > now).count()
        users = User.query.filter(User.expire_date > now).paginate(page, app.config.get('TABLE_ITEMS_PER_PAGE'),
                                                                   False).items

    if not users:
        return jsonify(info='error:Not found valid users')

    user_list = []
    for user in users:
        u = {}
        u['id'] = user.id
        u['email'] = user.email
        u['expire'] = utils.format_date(user.expire_date)
        u['transfer'] = round(user.total_transfer / BYTE_TO_GIGABYTE, 2)
        u['usage'] = round((user.upload_transfer + user.download_transfer) / user.total_transfer, 2)
        if user.service_enable == 1 and user.upload_transfer + user.download_transfer < user.total_transfer:
            if redis.connection.sismember('ports_to_stat', user.server_port):
                u['status'] = 'active'
            else:
                u['status'] = 'pending'
        elif user.service_enable == 0 or user.upload_transfer + user.download_transfer >= user.total_transfer:
            u['status'] = 'banned'
        user_list.append(u)

    total_page = int(math.ceil(total / app.config.get('TABLE_ITEMS_PER_PAGE')))
    page = utils.pagination(page, total_page)

    return jsonify(info='success', users=user_list, page=page)

@app.route('/user_edit')
def get_user_with_id():
    id = request.args.get('id', -1, type=int)
    user = User.query.filter_by(id=id).first()
    if not user:
        return None

    u = {}
    u['id'] = user.id
    u['email'] = user.email
    u['expire'] = utils.format_date(user.expire_date)
    u['transfer'] = round(user.total_transfer / BYTE_TO_GIGABYTE, 2)
    u['upload'] = user.upload_transfer
    u['download'] = user.download_transfer
    u['password'] = user.server_pass
    u['port'] = user.server_port
    u['enable'] = user.service_enable

    return jsonify(user=u)

@app.route('/save_user_info', methods=['POST'])
def set_user_info():
    form = manage.UserInfoForm()
    if form.validate_on_submit():
        try:
            db.session.query(User).filter(User.id == form.id.data).update({ User.email: form.email.data,
                                                                            User.total_transfer: int(form.transfer.data) * BYTE_TO_GIGABYTE,
                                                                            User.expire_date: utils.format_date(form.expire.data, True)})
            db.session.commit() # 一定要提交才能生效
            user = db.session.query(User).filter(User.id == form.id.data).first()
            if redis.connection.get('%s_t' % user.server_port):
                redis.connection.set('%s_t' % user.server_port, user.total_transfer) # update total transfer
        except Exception as e:
            return jsonify(info="error:Update database failed %s" % e)
    else:
        return jsonify(info="error:Form validate failed")

    return jsonify(info="success:success")

@app.route('/save_service_setting', methods=['POST'])
def set_service_setting():
    form = manage.ServiceSettingForm()
    if form.validate_on_submit():
        try:
            db.session.query(User).filter(User.id == form.id.data).update({ User.upload_transfer: form.upload.data,
                                                                            User.download_transfer: form.download.data,
                                                                            User.server_port: form.port.data,
                                                                            User.server_pass: form.password.data,
                                                                            User.service_enable: form.enable.data})
            db.session.commit()
            # Todo： update shadowsocks redis
            user = db.session.query(User).filter(User.id == form.id.data).first()
            if ss:
                ss.update_port(user.server_port, user.server_pass)
            #     if not ss.update_port(user.server_port, user.server_pass):
            #         return jsonify(info='info:Service on port[%s] with id %s not start' %(user.server_port, form.id.data))
            # else:
            #     return jsonify(info='error:Can not connect to shadowsocks')

        except Exception as e:
            return jsonify(info="error:Update database failed %s" % e)
    else:
        return jsonify(info="error:Form validate failed")

    return jsonify(info="success:success")

@app.route('/user_disable')
def disable_user_with_id():
    id = request.args.get('id', -1, type=int)

    try:
        db.session.query(User).filter(User.id == id).update({User.service_enable:0})
        db.session.commit()
        user = db.session.query(User).filter(User.id == id).first()
        if ss:
            ss.remove_port(user.server_port)
        #     if not ss.remove_port(user.server_port):
        #         return jsonify(info='error:Failed to remove service on port[%s] with id %s' %(user.server_port, id))
        # else:
        #     return jsonify(info='error:Can not connect to shadowsocks')

    except Exception as e:
        return jsonify(info='error:Disable user with id %s failed' % e)

    return jsonify(info='success:Disable user with id %s success' % id)
