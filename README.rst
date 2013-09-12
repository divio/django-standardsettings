=======================
Django Standardsettings
=======================

Django standardsettings encapsulates using dotenv and getenv to produce a "standard"
(opinionated) set of settings for the basic configuration needed in most projects.

It defines what things should be exposed to be configurable (e.g ``DEBUG=True``)
over environment variables and simplifies them (e.g setting
``ENABLE_DEBUG_TOOLBAR=True`` will add it to ``INSTALLED_APPS`` and to ``MIDDDLEWARES``).

It also does some autosetup for specific deployment environments based on a single environment variable.
Setting ``AUTOSETUP="local"`` will use our opinionated defaults for local development.
Setting ``AUTOSETUP="divio-nine-cloud"`` will configure all the basic settings for deployment on our server at nine.

Of course you can still override all these settings by defining variables in the corresponding ``.env`` file.

Deployment specific things are:

* ``MEDIA_ROOT`` / ``STATIC_ROOT``
* Database
* Cache
* Celery
* Sessions

Standardsettings also adds some other opinionated settings that should be the same over most projects:

* ...