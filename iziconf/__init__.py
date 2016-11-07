# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from os.path import isfile

from iziconf.lazy_settings import LazySettings
from iziconf.base_settings import YamlSettings
from iziconf.global_settings import global_settings
from iziconf.utils.singleton import Singleton


class Simpleconf(object):
    __metaclass__ = Singleton
    _default_conf = {"envvar_name": "SIMPLECONF_SETTINGS_FILE",
                     "settings_file": "/etc/SIMPLECONF/iziconf.yaml",
                     "callback": None}

    def _settings_file(self, conf=None):
        if not conf:
            conf = self._default_conf
        try:
            conffile = os.environ[conf['envvar_name']]
            if not isfile(conffile):
                raise KeyError
            return conffile
        except KeyError:
            # USE DEFAULT PATH
            return conf['settings_file']

    def __init__(self, conf=_default_conf):
        conffile = self._settings_file(conf)
        self.settings = LazySettings(YamlSettings, conffile,
                                     global_settings, callback=conf['callback'])
