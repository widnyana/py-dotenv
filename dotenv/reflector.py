# -*- coding: utf-8 -*-


class Reflector(object):

    def __init__(self, data=None):
        """

        :param data: data to be checked
        :type data: str, basetring
        :return:
        """
        if data:
            self._data = data.strip()

    @property
    def data(self):
        """
        :return: data
        :rtype: str
        """
        return self._data

    @data.setter
    def data(self, data):
        data = data.strip()
        self._data = data

    def _guess(self):
        data = self.data

        if data.isdigit():
            data = long(data)

        elif isfloat(data):
            data = float(data)

        elif data in ['True', 'true', 'False', 'false', 'no', 'yes']:
            data = data.lower()
            data = True if data in ['true', 'yes'] else False

        return data

    def getval(self):

        data = self._guess()
        return data


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

