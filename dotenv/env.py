# -*- coding:utf-8 -*-
from __future__ import with_statement
import os
from loader import Loader

__all__ = ['Dotenv']


def _getAbsPath():
    path = os.path.join(os.getcwd(), ".env")
    return path


class Dotenv(dict):
    silo = {}

    def __init__(self, filepath=None, immutable=False):
        super(Dotenv, self).__init__()

        if filepath is None:
            filepath = _getAbsPath()

        if not os.path.exists(filepath):
            raise RuntimeError(".env file is not found. Please create file at: %s" % filepath)

        self._filepath = filepath
        self.loader = Loader(filepath)

    def load(self):
        """load config without overriding os environment variable"""
        self.silo = self.loader.load(immutable=True)
        return self.silo

    def overload(self):
        """load config and override os environment variable"""
        self.silo = self.loader.load(immutable=False)
        return self.silo

    def __getitem__(self, item):
        keys = self.silo.keys()
        if item in keys:
            return self.silo[item]

        return os.environ[item]
