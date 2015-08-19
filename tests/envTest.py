# -*- coding:utf-8 -*-
from __future__ import with_statement
import os
import unittest
from tempfile import mkstemp

from dotenv import env, loader


class EnvTest(unittest.TestCase):
    def setUp(self):
        fd, self.filepath = mkstemp()

        with open(self.filepath, "w") as f:
            f.write("FOO=bar\n")
            f.write("BAR=baz\n")
            f.write("baz=1234\n")
            f.write("INDRIA=SMILING\n")
            f.write("amqp=amqp:\\guest:guest@localhost:1234/vhost")

        self.dotenv = env.Dotenv(self.filepath)

    def TestGetAbsPath(self):
        path = env._getAbsPath()
        curpath = os.path.join(os.getcwd(), ".env")
        self.assertEqual(path, curpath)

    def TestParseLine(self):
        k, v = loader._parseline("# omitted")
        self.assertEqual(k, None, "Should return None")

        k, v= loader._parseline("FOO=bar")
        self.assertEqual(v, "bar", "Should return bar, {} found".format(v))

        k, v = loader._parseline("FOO='bar'")
        self.assertEqual(v, "bar", "Should return bar, {} found".format(v))

        k, v = loader._parseline('BAR="baz"')
        self.assertEqual(v, "baz", "Should return 'baz', {} found".format(v))

    def TestLoaderImmutable(self):

        expected = "LAUGHING"  #: existing env var
        os.environ['INDRIA'] = expected
        l = loader.Loader(self.filepath)
        l.load(immutable=True)  #: should not override

        #: got
        got = os.environ["INDRIA"]  #: this should return as same as expected

        self.assertEqual(got, expected,
                         "Loader Should Not override value. %s expected, got %s instead" % (expected, got))

    def TestLoaderMutable(self):
        expected = "SMILING"
        old = "CRYING"
        os.environ['INDRIA'] = old #: existing env var
        l = loader.Loader(self.filepath)
        silo = l.load(immutable=False)   #: this thing should override
        #: got
        got = os.environ["INDRIA"]       #: should return "SMILING"


        self.assertEqual(got, expected,
                         "Loader Should Override Value. %s expected, got %s instead" % (expected, got))

        self.assertEqual(silo['INDRIA'], os.getenv("INDRIA"),
                         "Both object should be equal. got '%s' and '%s'" % (silo.get("INDRIA"), os.getenv("INDRIA")))

    def TestDotEnvMutable(self):
        os.environ["FOO"] = "boom"
        silo = self.dotenv.overload()

        expected = "bar"
        got = os.environ.get("FOO", None)
        self.assertEqual(expected, got)

    def TestDotEnvImmutable(self):
        expected = "bar"

        os.environ["FOO"] = expected
        silo = self.dotenv.load()

        got = silo.get("FOO")
        got2 = os.environ['FOO']
        self.assertEqual(expected, got, "Silo overriding envvar %s != %s" % (expected, got))
        self.assertEqual(got, got2, "envvar and silo doesnt same. %s != %s" % (got, got2))
