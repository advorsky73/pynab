#!/usr/bin/env python3

"""
This module tests the pynab module
"""

import unittest
from pynab.pynab import YNABSession


class TestYNABModule(unittest.TestCase):
    """
    Test class for pynab.py
    """
    def setUp(self):
        self.api_token = ""
        self.ynab_session = YNABSession(self.api_token)

    def tearDown(self):
        del self.ynab_session

    def test_get_user(self):
        u = self.ynab_session.get_user()
        print(u)
        print(u.id)

    def test_get_budgets(self):
        b = self.ynab_session.get_budgets()
        for bs in b:
           print(bs)

    def test_get_budgets_with_parameter(self):
        b = self.ynab_session.get_budgets()
        bb = self.ynab_session.get_budgets(b[0].id)
        for bs in bb:
           print(bs)



if __name__ == '__main__':
    unittest.main()
