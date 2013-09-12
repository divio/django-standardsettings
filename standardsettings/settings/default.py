# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from getenv import env
import os


def apply_pre_environment_settings(settings):
    s = settings
    print "APPLYING default settings"
    s.DEBUG = env('DEBUG', False)
    s.TEMPLATE_DEBUG = env('TEMPLATE_DEBUG', s.DEBUG)
    s.SRC_ROOT = env('SRC_ROOT', os.path.dirname(__file__))
    s.PROJECT_ROOT = env('PROJECT_ROOT', os.path.abspath(os.path.join(s.SRC_ROOT, '..')))
    s.SECRET_KEY = env('SECRET_KEY')
    if not s.SECRET_KEY:
        raise ImproperlyConfigured("you must set SECRET_KEY in your environment")

    s.SITE_ID = env('SITE_ID', 1)
    s.ROOT_URLCONF = 'urls'
    configure_media_and_static(settings)
    configure_templates(settings)
    configure_locale_and_time(settings)
    configure_debug_toolbar(settings)


def apply_post_environment_settings(settings):
    s = settings
    print "APPLYING default settings"
    # make sure all directories exist
    for path in (s.DATA_ROOT, s.MEDIA_ROOT, s.LOG_ROOT, s.SOCKET_ROOT):
        try:
            os.makedirs(path)
        except OSError:
            pass

    configure_celery(settings)
    configure_email(settings)
    configure_sessions(settings)
    configure_cache(settings)
    configure_sentry(settings)
    configure_logging(settings)


def configure_media_and_static(settings):
    s = settings
    s.MEDIA_URL = '/media/'
    s.STATIC_URL = '/static/'
    s.ADMIN_MEDIA_PREFIX = ''.join([s.STATIC_URL, 'admin/'])
    s.STATICFILES_DIRS = [os.path.join(s.PROJECT_ROOT, 'static')]
    s.STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'core.staticfiles_finders.AppDirectoriesFinderAsMedia',
        'compressor.finders.CompressorFinder',
    ]


def configure_templates(settings):
    s = settings
    s.TEMPLATE_DIRS = [os.path.join(s.PROJECT_ROOT, 'templates')]
    s.SEKIZAI_IGNORE_VALIDATION = True  # Silence the whining!
    s.TEMPLATE_LOADERS = [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]


def configure_locale_and_time(settings):
    s = settings
    s.LOCALE_PATHS = [
        os.path.join(s.PROJECT_ROOT, 'locale'),
    ]
    s.TIME_ZONE = env('TIME_ZONE', 'Europe/Zurich')
    s.USE_TZ = True
    s.LANGUAGE_CODE = env('LANGUAGE_CODE', 'en')
    s.USE_I18N = True
    s.USE_L10N = True
    s.DATE_FORMAT = 'd.m.Y'
    s.DATETIME_FORMAT = 'd.m.Y H:i'
    s.TIME_FORMAT = 'H:i'
    s.YEAR_MONTH_FORMAT = 'F Y'
    s.MONTH_DAY_FORMAT = 'j. F'


def configure_celery(settings):
    s = settings
    s.BROKER_TRANSPORT = 'celery_redis_unixsocket.broker.Transport'
    s.BROKER_HOST = s.REDIS_SOCKET
    s.BROKER_VHOST = 0
    s.CELERY_RESULT_BACKEND = 'redisunixsocket'
    s.CELERY_REDIS_HOST = s.BROKER_HOST
    s.CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
    import celery_redis_unixsocket  # makes it work with sockets
    if env("ENABLE_CELERY_AUTORELOADER", s.DEBUG):  # TODO: check if this really works
        s.CELERYD_AUTORELOADER = env("CELERYD_AUTORELOADER", "celery.worker.autoreload.Autoreloader")


def configure_email(settings):
    s = settings
    import dj_email_url
    email_config = dj_email_url.config()
    if email_config:
        s.EMAIL_FILE_PATH = email_config['EMAIL_FILE_PATH']
        s.EMAIL_HOST_USER = email_config['EMAIL_HOST_USER']
        s.EMAIL_HOST_PASSWORD = email_config['EMAIL_HOST_PASSWORD']
        s.EMAIL_HOST = email_config['EMAIL_HOST']
        s.EMAIL_PORT = email_config['EMAIL_PORT']
        s.EMAIL_BACKEND = email_config['EMAIL_BACKEND']
        s.EMAIL_USE_TLS = email_config['EMAIL_USE_TLS']
    else:
        s.EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    s.SERVER_EMAIL = env('SERVER_EMAIL', 'django@%s' % os.uname()[1])
    s.DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', 'norepy@divio.ch')


def configure_sessions(settings):
    s = settings
    s.SESSION_ENGINE = 'redis_sessions.session'
    s.SESSION_REDIS_UNIX_DOMAIN_SOCKET_PATH = s.REDIS_SOCKET
    s.SESSION_REDIS_DB = 1
    s.SESSION_REDIS_PREFIX = 'session'


def configure_cache(settings):
    s = settings
    s.CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': s.REDIS_SOCKET,
            'OPTIONS': {
                'DB': 2,
                'PASSWORD': '',
                'PARSER_CLASS': 'redis.connection.HiredisParser'
            },
        },
    }
    s.DJANGO_REDIS_IGNORE_EXCEPTIONS = True  # don't go down if cache fails


def configure_debug_toolbar(settings):
    s = settings
    if env("ENABLE_DEBUG_TOOLBAR", False):
        s.INSTALLED_APPS.extend([
           'debug_toolbar',
        ])
        s.MIDDLEWARE_CLASSES.extend([
           'debug_toolbar.middleware.DebugToolbarMiddleware',
        ])
        s.DEBUG_TOOLBAR_CONFIG = env("DEBUG_TOOLBAR_CONFIG", {'INTERCEPT_REDIRECTS': False,})


def configure_sentry(settings):
    s = settings
    s.RAVEN_CONFIG = env("RAVEN_CONFIG", {})
    if s.RAVEN_CONFIG:
        s.INSTALLED_APPS.append('raven.contrib.django.raven_compat')


def configure_logging(settings):
    """
    configure_sentry should run before this!
    """
    s = settings
    s.LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
            },
            'null': {
                'class': 'logging.NullHandler',
            },
            # we don't need this, we use sentry
            # 'mail_admins': {
            #     'level': 'ERROR',
            #     'filters': ['require_debug_false'],
            #     'class': 'django.utils.log.AdminEmailHandler'
            # },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
            },
            # 'django.request': {
            #     'handlers': ['mail_admins'],
            #     'level': 'ERROR',
            #     'propagate': False,
            # },
            # 'django.security': {
            #     'handlers': ['mail_admins'],
            #     'level': 'ERROR',
            #     'propagate': False,
            # },
            'py.warnings': {
                'handlers': ['console'],
            },
        }
    }


def configure_sentry(settings):
    s = settings
    s.RAVEN_CONFIG = env("RAVEN_CONFIG", {})
    if s.RAVEN_CONFIG:
        s.INSTALLED_APPS.append('raven.contrib.django.raven_compat')


