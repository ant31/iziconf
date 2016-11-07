from __future__ import absolute_import, division, print_function

import yaml
from iziconf.utils.dict import deep_merge


class YamlSettings(object):
    def __init__(self, config_path, defaults, callback=None):
        """
        Configure iziconf.

        Get global settings (defaults) and override them with ini-file-defined
        custom settings.
        """
        self._config = {}
        try:
            with open(config_path, "rb") as f:
                self._config = yaml.load(f.read())
        except IOError:
            pass
        print(defaults)
        deep_merge(defaults, self._config)
        self._config = defaults
        print(self._config)
        # Read config
        self.configure('logger', 'log', self._config)

        if callback:
            callback(self)

    def configure(self, section, attr=None, conf=None):
        """Configure all settings from a given section."""
        if attr is None:
            attr = section

        if not conf:
            conf = self._config
        settings = conf[section]

        setattr(self, attr, settings)
