__version__ = '0.0.3'


def apply_settings(setting_module_name):
    """
    pass in the settings module here and standardsettings will set stuff on it.
    """
    import sys
    settings = sys.modules[setting_module_name]
    from . import helpers
    helpers.apply_all_settings(settings)