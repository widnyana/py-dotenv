# -*- Coding: utf-8 -*-
import os
import pytoml

from dotenv.baseloader import BaseLoader


class TOMLLoader(BaseLoader):

    def __init__(self, filepath):
        self._filepath = filepath

    def load(self, immutable=False):
        """Load .env as Config
        :param immutable: if set to true, will override OS's env var
        :type immutable: bool
        """
        self._immutable = immutable
        self._ensure_readable()

        self._create_conf()
        self._set_envar()

        return self.silo

    def _create_conf(self):
        with open(self._filepath, "r") as f:
            obj = pytoml.load(f)

            for k, v in obj.iteritems():
                if not k or not v:
                    #: ignore empty data
                    continue

                if self._immutable and os.environ.get(k, None) is not None:
                    v = os.environ.get(k, None)

                conf = dict((x, y) for x, y in ((k,v),))
                self.silo.update(conf)

    def _set_envar(self):
        """Add setting from .env to OS' Environment Variable"""
        if not isinstance(self.silo, dict):
            return

        for key in self.silo.keys():
            if self._immutable and os.environ.get(key, None) is not None:
                continue
            else:
                os.environ[key] = self.silo[key]
