# -*- coding:utf-8 -*-
import os


class Loader(object):
    __author__ = 'Widnyana <me@widnyana.web.id>'

    silo = {}

    def __init__(self, filepath):
        self._filepath = filepath
        self._immutable = False

    def load(self, immutable=False):
        """Load .env as Config"""
        self._immutable = immutable
        self._ensureReadable()

        self._createConf()
        self._setEnvVar()

        return self.silo

    def _createConf(self):
        with open(self._filepath, "r") as f:
            for line in f.readlines():
                k, v = _parseline(line)
                if self._immutable and os.environ.get(k, None) is not None:
                    v = os.environ.get(k, None)

                conf = dict((x, y) for x, y in ((k,v),))
                self.silo.update(conf)

    def _ensureReadable(self):
        if not os.access(self._filepath, os.R_OK) or not os.path.exists(self._filepath):
            raise IOError('Indria: Environment file .env not found or not readable. '
                          'Create file with your environment settings at %s' % self._filepath)

    def _setEnvVar(self):
        """Overide Environtment Variable"""
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
