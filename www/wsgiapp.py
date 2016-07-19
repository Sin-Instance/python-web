#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

'''
A WSGI application entry.
'''

import logging; logging.basicConfig(level=logging.INFO)

import os

from transwarp import db
from transwarp.web import WSGIApplication, Jinja2TemplateEngine

from config import configs

def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'A minute ago'
    if delta < 3600:
        return u'%s minute ago' % (delta // 60)
    if delta < 86400:
        return u'%s hour ago' % (delta // 3600)
    if delta < 604800:
        return u'%s day age' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
	return u'%s - %s - %s' % (dt.year, dt.month, dt.day)

# init db:
db.create_engine(**configs.db)

# init wsgi app:
wsgi = WSGIApplication(os.path.dirname(os.path.abspath(__file__)))

template_engine = Jinja2TemplateEngine(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
template_engine.add_filter('datetime', datetime_filter)

wsgi.template_engine = template_engine

import urls

wsgi.add_module(urls)

if __name__ == '__main__':
	wsgi.run(9000)