# -*- coding: utf-8 -*-
from getenv import env

def apply_all_settings(settings):
    # TODO: make this configurable
    from .settings import default as defaults_mod
    defaults_mod.apply_pre_environment_settings(settings)

    # TODO: environment should be dynamically imported with AUTOSETUP
    autoconfig = env('AUTOSETUP', 'standardsettings.environments.local')
    if autoconfig == 'standardsettings.environments.local':
        from .environments import local as env_mod
    elif autoconfig == 'standardsettings.environments.divio_nine_cloud':
        from .environments import divio_nine_cloud as env_mod
    else:
        raise Exception("must define autoconfig")
    env_mod.apply_settings(settings)

    defaults_mod.apply_post_environment_settings(settings)