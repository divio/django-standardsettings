# -*- coding: utf-8 -*-
from getenv import env
import os

def apply_settings(settings):
    s = settings
    s.DATA_ROOT = os.path.abspath(env("DATA_ROOT", os.path.join(s.PROJECT_ROOT, 'tmp')))
    s.MEDIA_ROOT = env("MEDIA_ROOT", os.path.join(s.DATA_ROOT, 'media'))
    s.STATIC_ROOT = env("STATIC_ROOT", os.path.join(s.DATA_ROOT, 'static_collected'))
    s.LOG_ROOT = env("LOG_ROOT", os.path.join(s.DATA_ROOT, 'logs'))
    s.SOCKET_ROOT = env("SOCKET_ROOT", s.DATA_ROOT)
    s.REDIS_SOCKET = env("REDIS_SOCKET", os.path.join(s.SOCKET_ROOT, 'redis.sock'))
    s.ALLOWED_HOSTS = env("ALLOWED_HOSTS", ['127.0.0.1', 'localhost',])
    import dj_database_url
    s.DATABASES = {'default': dj_database_url.config(default='sqlite:///%s' % os.path.join(s.DATA_ROOT, 'db.sqlite3'))}