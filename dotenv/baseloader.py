# -*- Coding: utf-8 -*-
import os


class BaseLoader(object):
    __author__ = 'Widnyana <me@widnyana.web.id>'

    silo = {}
    _filepath = None
    _immutable = False

    def _ensure_readable(self):
        if not os.access(self._filepath, os.R_OK) or not os.path.exists(self._filepath):
            raise IOError('Indria: Environment file .env not found or not readable. '
                          'Create file with your environment settings at %s' % self._filepath)
