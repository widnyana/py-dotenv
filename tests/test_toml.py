# -*- Coding: utf-8 -*-
import unittest
from tempfile import mkstemp

import os

from dotenv import env, tomlloader


class TOMLTest(unittest.TestCase):
    def setUp(self):
        fd, self.filepath = mkstemp(".toml", prefix=".env")

        with open(self.filepath, "w") as f:
            f.writelines("""
# This is a TOML document.

INDRIA = "LAUGHING"

[owner]
name = "Tom Preston-Werner"
dob = 1979-05-27T07:32:00-08:00 # First class dates

[database]
server = "192.168.1.1"
ports = [ 8001, 8001, 8002 ]
connection_max = 5000
enabled = true

[servers]

# Indentation (tabs and/or spaces) is allowed but not required
[servers.alpha]
ip = "10.0.0.1"
dc = "eqdc10"

[servers.beta]
ip = "10.0.0.2"
dc = "eqdc10"

[clients]
data = [ ["gamma", "delta"], [1, 2] ]
            """)

        os.chdir(os.path.dirname(self.filepath))
        self.dotenv = env.Dotenv(self.filepath)

    def tearDown(self):
        os.unlink(self.filepath)

    def testLocateEnvFile(self):

        path = env._locate(".toml")
        self.assertEqual(path, self.filepath)

    def TestLoaderImmutable(self):

        expected = "LAUGHING"  #: existing env var
        os.environ['INDRIA'] = expected
        l = tomlloader.TOMLLoader(self.filepath)
        l.load(immutable=True)  #: should not override

        #: got
        got = os.environ["INDRIA"]  #: this should return as same as expected

        self.assertEqual(got, expected,
                         "Loader Should Not override value. %s expected, got %s instead" % (expected, got))