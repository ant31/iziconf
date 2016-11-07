# -*- coding: utf-8 -*-
from __future__ import absolute_import
from iziconf.utils.functional import LazyObject, empty


class LazySettings(LazyObject):
    """A lazy proxy for either global Simpleconf settings or a custom settings object.

    The user can manually configure settings prior to using them. Otherwise,
    iziconf uses the settings module pointed to by ``conffile``.
    """
    def __init__(self, settings_cls, settings_module, *args, **kwargs):
        self.__dict__['_settings_cls'] = settings_cls
        self.__dict__['_settings_module'] = settings_module
        self.__dict__['_args'] = args
        self.__dict__['_kwargs'] = kwargs

        super(LazySettings, self).__init__()

    def _setup(self, name=None):
        """
        Load the settings pointed to by conffile. This is used the first time
        we need any settings at all, if the user has not previously configured
        the settings manually.
        """
        self._wrapped = self._settings_cls(self._settings_module, *self._args, **self._kwargs)

    def __getattr__(self, name):
        if self._wrapped is empty:
            self._setup(name)
        return getattr(self._wrapped, name)

    def configure(self, settings_module):
        """ Called to manually configure the settings.
        The 'default_settings' parameter sets where to retrieve any unspecified values from (its
        argument must support attribute access (__getattr__)).

        :param settings_module: The path to the iziconf.ini configuration file.
 Only options declared in :mod:`iziconf.options.global_settings` will be parsed.


        """
        if self._wrapped is not empty:
            raise RuntimeError('Settings already configured.')
        self._wrapped = self._settings_cls(settings_module, *self._args, **self._kwargs)

    def reconfigure(self, settings_module, **kw_options):
        """
        Called to manually change the options file. It will close all previous
        session, dispose engine and recreate them with the new configuration
        file.
        """
        # Never been configured
        if self._wrapped is not empty:
            if 'dispose_function' in kw_options:
                dispose = kw_options.pop('dispose_function')
                dispose()
            self._wrapped = empty
        self.configure(settings_module, **kw_options)

    @property
    def configured(self):
        """
        Returns ``True`` if the settings have already been configured.
        """
        return self._wrapped is not empty
