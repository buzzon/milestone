import os
from configparser import ConfigParser


class ParametersContainer:
    """
    Class-proxy for config parser
    Loads the parameters from the file, the path to which is specified in the $CONFIG_PATH env var
    If $CONFIG_PATH not set, use default location
    """
    DEFAULT_CONFIG_FILENAME = 'settings/config.ini'

    def __init__(self, base_dir=None):
        self._base_dir = base_dir

        if self._base_dir:
            self._default_config_path = os.path.join(self._base_dir, self.DEFAULT_CONFIG_FILENAME)

        self._parameters = ConfigParser()
        config_path = os.getenv('CONFIG_PATH', self._default_config_path)
        assert os.path.exists(config_path), \
            'Configuration file not exists: {}'.format(config_path)

        self._parameters.read(
            os.getenv('CONFIG_PATH', self._default_config_path)
        )

    def get(self, *args, **kwargs):
        return self._parameters.get(*args, **kwargs)

    def getboolean(self, *args, **kwargs):
        return self._parameters.getboolean(*args, **kwargs)

    def getint(self, *args, **kwargs):
        return self._parameters.getint(*args, **kwargs)

    def getfloat(self, *args, **kwargs):
        return self._parameters.getfloat(*args, **kwargs)