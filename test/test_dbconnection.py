"""
The local config sqlite database retrieves a mysql connection url
"""
import os
import re
import unittest
from unittest import TestCase

from  models.dbconnection import Keys

class TestDbConnection(TestCase):
    def test_KeysGetSaConn(self):
        '''
        Tests that we get a value from the sqlite db and it begins w a pymysql SqlAlchemy protocol
        '''
        uri = Keys.getSAConn()
        self.assertIsNotNone(uri)
        self.assertTrue(uri.startswith('mysql+pymysql://'))

if __name__ == '__main__':
    tbc = TestDbConnection()
    tbc.test_KeysGetSaConn()

