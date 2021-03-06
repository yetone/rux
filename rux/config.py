# coding=utf8

"""
    rux.config
    ~~~~~~~~~~

    Configuration manager, rux's configuration is in toml.
"""

from os.path import exists

from . import charset
from .exceptions import ConfigSyntaxError
from .utils import join

import toml


class Config(object):

    filename = 'config.toml'
    filepath = join('.', filename)

    # default configuration
    default = {
        'blog': {
            'name': '',
            'description': '',
            'theme': 'default',
        },
        'author': {
            'name': 'hit9',
            'email': 'nz2324@126.com',
        }
    }

    def parse(self):
        """parse config, return a dict"""

        if exists(self.filepath):
            content = open(self.filepath).read().decode(charset)
        else:
            content = ""

        try:
            config = toml.loads(content)
        except toml.TomlSyntaxError:
            raise ConfigSyntaxError

        return config


config = Config()
