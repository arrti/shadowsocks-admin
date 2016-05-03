#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2012 F2E.im
# Do have a faith in what you're doing.
# Make your life a story worth telling.

import re
from jinja2 import evalcontextfilter, Markup, escape


class Filters():
    def __init__(self, jinja2_env):
        self.jinja2 = jinja2_env

    def register(self):
        self.jinja2.filters["dump_errors"] = self.dump_errors
        self.jinja2.filters["pagination"] = self.pagination
        self.jinja2.filters["progress_bar"] = self.progress_bar
        self.jinja2.filters["progress_label"] = self.progress_label
        self.jinja2.filters["nl2br"] = self.nl2br
        self.jinja2.filters["build_uri"] = self.build_uri
        self.jinja2.filters["pretty_date"] = self.pretty_date
        self.jinja2.filters["email_mosaic"] = self.email_mosaic
        return self.jinja2

    def dump_errors(self, errors):
        t = self.jinja2.from_string("""
            {% if errors %}
            <ul class="alert-error">
                {% for error in errors %}
                    <li>{{ ','.join(errors[error]) }}</li>
                {% endfor %}
            </ul>
            {% endif %}
            """)

        return t.render(errors = errors)

    def build_uri(uri, param, value):
        regx = re.compile("[\?&](%s=[^\?&]*)" % param)
        find = regx.search(uri)
        split = "&" if re.search(r"\?", uri) else "?"
        if not find: return "%s%s%s=%s" % (uri, split, param, value)
        return re.sub(find.group(1), "%s=%s" % (param, value), uri)

    def pagination(self, page, uri, list_rows = 10):
        def gen_page_list(current_page = 1, total_page = 1, list_rows = 10):
            if(total_page <= list_rows):
                return range(1, total_page + 1)

            if(current_page + list_rows > total_page):
                return range(total_page - list_rows + 1, total_page + 1)
            else:
                return range(current_page, list_rows + current_page)

        t = self.jinja2.from_string("""
            {% if page and not page.pages == 1 %}
                <ul>
                    <li {% if page.current == page.prev %}class="disabled"{% endif %}><a href="{{ uri|build_uri('p', page.prev) }}">«</a></li>
                    {% for p in gen_page_list(page.current, page.pages, list_rows) %}
                        <li {% if page.current == p %}class="active"{% endif %}>
                            {% if not page.current == p %}
                                <a href="{{ uri|build_uri('p', p) }}">{{ p }}</a>
                            {% else %}
                                <a href="javascript:;">{{ p }}</a>
                            {% endif %}
                        </li>
                    {% endfor %}
                    <li {% if page.current == page.next %}class="disabled"{% endif %}><a href="{{ uri|build_uri('p', page.next) }}">»</a></li>
                </ul>
            {% endif %}
            """)

        return t.render(page = page, uri = uri, gen_page_list = gen_page_list, list_rows = list_rows)

    def progress_bar(self, usage):
        if usage <= 0.5:
            bar = "progress-bar-success"
        elif usage > 0.5 and usage <= 0.7:
            bar = "progress-bar-primary"
        elif usage >= 0.7 and usage < 0.95:
            bar = "progress-bar-yellow"
        else:
            bar = "progress-bar-danger"

        t = self.jinja2.from_string("""
            <div class="progress progress-xs">
              <div class="progress-bar {{ bar }}" style="width: {{ usage }}"></div>
            </div>
        """)

        return t.render(bar = bar, usage = usage)

    def progress_label(self, usage):
        if usage <= 0.5:
            label = "bg-green"
        elif usage > 0.5 and usage <= 0.7:
            label = "bg-light-blue"
        elif usage >= 0.7 and usage < 0.95:
            label = "bg-yellow"
        else:
            label = "bg-red"

        t = self.jinja2.from_string("""
            <span class="badge {{ label }}">{{ usage }}</span>
        """)

        return t.render(label = label, usage = usage)

    @evalcontextfilter
    def nl2br(self, eval_ctx, value):
        _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
        result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n') for p in _paragraph_re.split(escape(value)))
        if eval_ctx.autoescape:
            result = Markup(result)
        return result

    def pretty_date(self, time = False):
        """
        Get a datetime object or a int() Epoch timestamp and return a
        pretty string like 'an hour ago', 'Yesterday', '3 months ago',
        'just now', etc
        """
        if time == None:
            return time

        from datetime import datetime
        now = datetime.now()
        if type(time) is str or type(time) is unicode:
            time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        elif type(time) is int:
            diff = now - datetime.fromtimestamp(time)
        elif isinstance(time, datetime):
            diff = now - time 
        elif not time:
            diff = now - now
        second_diff = diff.seconds
        day_diff = diff.days

        if day_diff < 0:
            return ''

        if day_diff == 0:
            if second_diff < 10:
                return "刚刚"
            if second_diff < 60:
                return str(second_diff) + " 秒前"
            if second_diff < 120:
                return  "1 分钟前"
            if second_diff < 3600:
                return str(second_diff / 60) + " 分钟前"
            if second_diff < 7200:
                return "1 小时前"
            if second_diff < 86400:
                return str(second_diff / 3600) + " 小时前"
        if day_diff == 1:
            return "昨天"
        if day_diff < 7:
            return str(day_diff) + " 天前"
        if day_diff < 31:
            return str(day_diff / 7) + " 周前"
        if day_diff < 365:
            return str(day_diff / 30) + " 月前"
        return str(day_diff / 365) + " 天前"

    def email_mosaic(self, email):
        if not email:
            return ""

        email_name = re.findall(r'^([^@]+)@', email)[0]

        if len(email_name) < 5:
            email_name = email_name + '***'
            email = re.sub(r'^([^@]+)@', '%s@' % email_name, email)
        else:
            email = re.sub(r'[^@]{3}@', '***@', email)

        return email


