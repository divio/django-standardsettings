# -*- coding: utf-8 -*-
from getenv import env
import os

def apply_settings(settings):
    print "APPLYING divio nine cloud settings"
    username = env('USER')  # this is the unix username
    stage = username.split('-')[1]
    server_cfg = {'username': username, 'site': os.environ.get('DEPLOYMENT_SITE', 'main')}
    settings.DATA_ROOT = '/home/%(username)s/upload/' % server_cfg
    settings.MEDIA_ROOT = '/home/%(username)s/upload/media/' % server_cfg
    settings.STATIC_ROOT = '/home/%(username)s/static/' % server_cfg
    settings.LOG_ROOT = '/home/%(username)s/log/'
    settings.SOCKET_ROOT = '/home/%(username)s/tmp/' % server_cfg
    settings.REDIS_SOCKET = '/home/%(username)s/tmp/%(username)s_%(site)s_redis.sock' % server_cfg
    settings.ALLOWED_HOSTS = env("ALLOWED_HOSTS", ['%(username)s.divio.ch' % server_cfg])
    import dj_database_url
    settings.DATABASES = {'default': dj_database_url.config(default='postgres://%(username)s@/%(username)s' % server_cfg)}
    print "configured settings for nine"