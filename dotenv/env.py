# -*- coding:utf-8 -*-
from __future__ import with_statement
import os
from loader import Loader

__all__ = ['Dotenv']


def _get_abs_path():
    path = os.path.join(os.getcwd(), ".env")
    return path


class Dotenv(dict):
    silo = {}

    def __init__(self, filepath=None, overload=False):
        super(Dotenv, self).__init__()

        if filepath is None:
            filepath = _get_abs_path()

        if not os.path.exists(filepath):
            raise RuntimeError(".env file is not found. Please create file at: %s" % filepath)

        self._filepath = filepath
        self.loader = Loader(filepath)
        self._overload = overload

    def load(self):
        """load config with default mutable setting loaded from self._override.

        Default is not overloading env var
        """
        self.silo = self.loader.load(override=self._overload)
        return self.silo

    def override(self):
        """load config and override os environment variable"""
        self.silo = self.loader.load(override=False)
        return self.silo

    def get(self, item, default=None):
        keys = self.silo.keys()

        try:
            if item in keys:
                data = self.silo[item]
            else:
                data = os.environ[item]
        except (KeyError, AttributeError):
            data = default
        return data
