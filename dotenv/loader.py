# -*- coding:utf-8 -*-
import os
from .reflector import Reflector


class Loader(object):
    __author__ = 'Widnyana <me@widnyana.web.id>'

    silo = {}

    def __init__(self, filepath):
        self._filepath = filepath
        self._override = False

    def load(self, override=False):
        """Load .env as Config
        :param override: set to True to avoid overriding os' env var
        """
        self._override = override
        self._ensure_readable()

        self._create_conf()
        self._set_env_var()

        return self.silo

    def _create_conf(self):
        with open(self._filepath, "r") as f:
            r = Reflector()
            for line in f.readlines():
                k, v = _parseline(line)

                if not k or not v:
                    #: ignore blank line
                    continue

                if self._override and os.environ.get(k, None) is not None:
                    v = os.environ.get(k, None)

                r.data = v

                conf = dict((x, y) for x, y in ((k, r.getval()),))
                self.silo.update(conf)

    def _ensure_readable(self):
        if not os.access(self._filepath, os.R_OK) or not os.path.exists(self._filepath):
            raise IOError('Indria: Environment file .env not found or not readable. '
                          'Create file with your environment settings at %s' % self._filepath)

    def _set_env_var(self):
        """Overide Environtment Variable"""
        if not isinstance(self.silo, dict):
            return

        for key in self.silo.keys():
            if self._override and os.environ.get(key, None) is not None:
                data = os.environ.get(key)
            else:
                data = self.silo[key]

            self.silo.update({
                key: data
            })

            try:
                os.environ[key] = str(data)
            except Exception, e:
                raise e


def _parseline(line):
    """Parse Line to dict"""
    if line.startswith("#"):
        return None, None

    line = line.replace("\n","")

    if line.strip():
        quote_delimiter = max(
            line.find('\'', line.find('\'') + 1),
            line.find('"', line.rfind('"')) + 1     #: find first comment mark after second quote mark
        )

        if quote_delimiter == 0:
            key, value = line.split("=")

        else:
            comment_delimiter = line.find('#', quote_delimiter)
            line = line[:comment_delimiter]

            key, value = map(lambda x: x.strip().strip('\'').strip('"'),
                             line.split('=', 1))

        key = key.strip()
        value = value.strip()
        return key, value

    else:
        return None, None
