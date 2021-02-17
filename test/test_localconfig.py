"""
Test the reference in local config is proper
"""
import os
import re
import unittest
from unittest import TestCase

from  localconfig import sqlitedb

class TestLocalconfig(TestCase):
    def test_localconfig(self):
        '''
        Test that the string sqlitedb is a proper SQLAlchemy url and that
        the file exists already
        '''
        fn = re.search(r'sqlite:///(.*)', sqlitedb)
        self.assertIsNotNone(fn)
        fn = fn.group(1)
        self.assertTrue(os.path.exists(fn))
        # self.assertTrue(os.path.exists(sqlitedb))

if __name__ == '__main__':
    tlc = TestLocalconfig()
    tlc.test_localconfig()

