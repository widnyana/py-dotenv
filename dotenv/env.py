# -*- coding:utf-8 -*-
from __future__ import with_statement
import os

from dotenv.tomlloader import TOMLLoader
from loader import Loader

__all__ = ['Dotenv']


def _locate(ext=''):
    cwd = os.getcwd()
    for f in os.listdir(cwd):
        if f.startswith(".env") and f.endswith(ext):
            path = os.path.join(cwd, f)
            return path


class Dotenv(dict):
    silo = {}

    def __init__(self, filepath=None, ext=""):
        """Init a dotenv

        :param filepath: absolute path to env file. optional.
        :param ext: extension of the env file. it will load ONLY one file
                    which match the extension
                    supported:
                        - plain
                        - toml
        """
        super(Dotenv, self).__init__()

        if filepath is None:
            filepath = _locate(ext)

        if not os.path.exists(filepath):
            raise RuntimeError("Indria: .env file is not found. Please create file at: %s" % filepath)

        #: define file extension
        if not ext:
            _, ext = os.path.splitext(filepath)

        #: available loader.
        _loader = {
            '': Loader,
            'toml': TOMLLoader
        }

        self._filepath = filepath
        try:
            self.loader = _loader[ext.replace(".", "")](filepath)
        except KeyError:
            raise RuntimeError("Indria: sorry the loader for %s file type currently not supported." % (ext,))

    def load(self, immutable=False):
        """load env var from .env,
        default behavior is not overriding any OS' env var

        :param immutable: override env var?
        :type immutable: bool
        :rtype: dict
        """
        self.silo = self.loader.load(immutable=immutable)
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
