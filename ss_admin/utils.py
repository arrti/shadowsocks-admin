#!/usr/bin/python
# -*- coding: utf-8 -*-
# author arrti

import os, random, hashlib, string, time

def pagination(current_page, total_page, list_rows = 10):
    if total_page <= 0:
            return None

    def gen_page_list(current_page = 1, total_page = 1, list_rows = 10):
        if(total_page <= list_rows):
            return range(1, total_page + 1)

        if(current_page + list_rows > total_page):
            return range(total_page - list_rows + 1, total_page + 1)
        else:
            return range(current_page, list_rows + current_page)

    prev = current_page - 1
    if prev == 0:
        prev = current_page
    next = current_page + 1
    if next > total_page:
        next = total_page

    page = {'page': current_page, 'pages': total_page, 'prev':prev, 'next': next, \
            'page_list': gen_page_list(current_page, total_page, list_rows)}

    return page

def format_date(time_stamp, to_unix=False):
    if not to_unix:
        format = time.strftime("%Y-%m-%d", time.localtime(time_stamp))
    else:
        format = int(time.mktime(time.strptime(time_stamp, '%Y-%m-%d')))

    return format

def generate_password(length = 16):
    chars= string.letters + string.digits*3 + '^@!$%&=?+#-_|'
    return ''.join([random.choice(chars) for i in range(length)])
