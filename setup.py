#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from setuptools import setup

try:  # fix nose error
    import multiprocessing
except ImportError:
    pass

setup(
    name='dotenv',
    version=__import__('dotenv').__version__,
    description='Handle .env files',
    author='widnyana putra',
    author_email='wid@widnyana.web.id',
    url='https://github.com/widnyana/py-dotenv',
    test_suite='nose.collector',
    packages=['dotenv'],
    tests_require=['nose']
)
