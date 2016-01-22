# -*- coding:utf-8 -*-
import os
from dotenv.baseloader import BaseLoader


class Loader(BaseLoader):
    __author__ = 'Widnyana <me@widnyana.web.id>'

    silo = {}

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
            for line in f.readlines():
                k, v = _parseline(line)

                if not k or not v:
                    #: ignore blank line
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


def _parseline(line):
    """Parse Line to dict"""
    if line.startswith("#"):
        return None, None

    line = line.replace("\n","")

    if line.strip():
        quote_delimit = max(line.find('\'', line.find('\'') + 1),
                            line.find('"', line.rfind('"')) + 1)  # find first comment mark after second quote mark

        if quote_delimit == 0:
            key, value = line.split("=")

        else:
            comment_delimit = line.find('#', quote_delimit)
            line = line[:comment_delimit]
            key, value = map(lambda x: x.strip().strip('\'').strip('"'),
                             line.split('=', 1))
        return key, value

    else:
        return None, None
