#!/usr/bin/env python3

"""
This module tests the pynab module
"""

import os
import unittest
import uuid
from pynab.pynab import YNAB


class TestYNABModule(unittest.TestCase):
    """
    Test class for pynab.py
    """

    def setUp(self):
        self.api_token = os.environ['YNAB_API_TOKEN']
        self.ynab_session = YNAB(self.api_token)

    def tearDown(self):
        del self.ynab_session

    def _verify_budget(self, budget):
        """
        Verifies the budget json node and its children
        :param budget: object representing a budget
        :return: nothing
        """
        self.assertIsNotNone(budget)
        self.assertIsNotNone(budget.id)
        self.assertIsNotNone(budget.name)
        if hasattr(budget, 'last_modified_on'):
            self.assertIsNotNone(budget.last_modified_on)
        self.assertIsNotNone(budget.date_format)
        self.assertIsNotNone(budget.date_format.format)
        self.assertIsNotNone(budget.currency_format)
        self.assertIsNotNone(budget.currency_format.iso_code)
        self.assertIsNotNone(budget.currency_format.example_format)
        self.assertIsNotNone(budget.currency_format.decimal_digits)
        self.assertIsNotNone(budget.currency_format.decimal_separator)
        self.assertIsNotNone(budget.currency_format.symbol_first)
        self.assertIsNotNone(budget.currency_format.group_separator)
        self.assertIsNotNone(budget.currency_format.currency_symbol)
        self.assertIsNotNone(budget.currency_format.display_symbol)

    def _verify_account(self, account):
        """
        Verifies the account json node and its children
        :param account: object representing an account
        :return: nothing
        """
        self.assertIsNotNone(account)
        self.assertIsNotNone(account.id)
        self.assertIsNotNone(account.name)
        self.assertIsNotNone(account.type)
        self.assertIsNotNone(account.on_budget)
        self.assertIsNotNone(account.closed)
        self.assertTrue(hasattr(account, 'note'))
        self.assertIsNotNone(account.balance)
        self.assertIsNotNone(account.cleared_balance)
        self.assertIsNotNone(account.uncleared_balance)

    def _verify_payee(self, payee):
        """
        Verifies the payee json node and its children
        :param payee: object representing a payee
        :return: nothing
        """
        self.assertIsNotNone(payee)
        self.assertIsNotNone(payee.id)
        self.assertIsNotNone(payee.name)
        self.assertTrue(hasattr(payee, 'transfer_account_id'))

    def _verify_payee_location(self, payee_location):
        """
        Verifies the payee_location json node and its children
        :param payee_location: object representing a payee_location
        :return: nothing
        """
        self.assertIsNotNone(payee_location)
        self.assertIsNotNone(payee_location.id)
        self.assertIsNotNone(payee_location.payee_id)
        self.assertTrue(hasattr(payee_location, 'latitude'))
        self.assertTrue(hasattr(payee_location, 'longitude'))

    def _verify_category_group(self, category_group):
        """
        Verifies the category_group json node and its children
        :param category_group: object representing a category_group
        :return: nothing
        """
        self.assertIsNotNone(category_group)
        self.assertIsNotNone(category_group.id)
        self.assertIsNotNone(category_group.name)
        self.assertIsNotNone(category_group.hidden)

    def _verify_category(self, category):
        """
        Verifies the category json node and its children
        :param category: object representing a category
        :return: nothing
        """
        self.assertIsNotNone(category)
        self.assertIsNotNone(category.id)
        self.assertIsNotNone(category.category_group_id)
        self.assertIsNotNone(category.name)
        self.assertIsNotNone(category.hidden)
        self.assertIsNotNone(category.name)
        self.assertTrue(hasattr(category, 'note'))
        self.assertIsNotNone(category.budgeted)
        self.assertIsNotNone(category.activity)
        self.assertIsNotNone(category.balance)

    def _verify_month(self, month):
        """
        Verifies the month json node and its children
        :param month: object representing a month
        :return: nothing
        """
        self.assertIsNotNone(month)
        self.assertIsNotNone(month.month)
        self.assertTrue(hasattr(month, 'note'))
        self.assertIsNotNone(month.to_be_budgeted)
        self.assertTrue(hasattr(month, 'age_of_money'))

    def _verify_transaction(self, transaction):
        """
        Verifies the transaction json node and its children
        :param transaction: object representing a transaction
        :return: nothing
        """
        self.assertIsNotNone(transaction)
        self.assertIsNotNone(transaction.id)
        self.assertIsNotNone(transaction.date)
        self.assertIsNotNone(transaction.amount)
        self.assertTrue(hasattr(transaction, 'memo'))
        self.assertIsNotNone(transaction.cleared)
        self.assertIsNotNone(transaction.approved)
        self.assertTrue(hasattr(transaction, 'flag_color'))
        self.assertIsNotNone(transaction.account_id)
        self.assertTrue(hasattr(transaction, 'payee_id'))
        self.assertTrue(hasattr(transaction, 'category_id'))
        self.assertTrue(hasattr(transaction, 'transfer_account_id'))
        self.assertTrue(hasattr(transaction, 'import_id'))

    def _verify_subtransactions(self, subtransaction):
        """
        Verifies the subtransactions json node and its children
        :param subtransaction: object representing a subtransactions
        :return: nothing
        """
        self.assertIsNotNone(subtransaction)
        self.assertIsNotNone(subtransaction.transaction_id)
        self.assertIsNotNone(subtransaction.amount)
        self.assertTrue(hasattr(subtransaction, 'memo'))
        self.assertTrue(hasattr(subtransaction, 'payee_id'))
        self.assertTrue(hasattr(subtransaction, 'category_id'))
        self.assertTrue(hasattr(subtransaction, 'transfer_account_id'))

    def _verify_scheduled_transactions(self, scheduled_transaction):
        """
        Verifies the scheduled_transactions json node and its children
        :param scheduled_transaction: object representing a scheduled_transactions
        :return: nothing
        """
        self.assertIsNotNone(scheduled_transaction)
        self.assertIsNotNone(scheduled_transaction.id)
        self.assertIsNotNone(scheduled_transaction.date_first)
        self.assertIsNotNone(scheduled_transaction.date_next)
        self.assertIsNotNone(scheduled_transaction.frequency)
        self.assertIsNotNone(scheduled_transaction.amount)
        self.assertTrue(hasattr(scheduled_transaction, 'memo'))
        self.assertTrue(hasattr(scheduled_transaction, 'flag_color'))
        self.assertIsNotNone(scheduled_transaction.account_id)
        self.assertTrue(hasattr(scheduled_transaction, 'payee_id'))
        self.assertTrue(hasattr(scheduled_transaction, 'category_id'))
        self.assertTrue(hasattr(scheduled_transaction, 'transfer_account_id'))

    def _verify_scheduled_subtransactions(self, scheduled_subtransaction):
        """
        Verifies the scheduled_subtransactions json node and its children
        :param scheduled_subtransaction: object representing a scheduled_subtransactions
        :return: nothing
        """
        self.assertIsNotNone(scheduled_subtransaction)
        self.assertIsNotNone(scheduled_subtransaction.scheduled_transaction_id)
        self.assertIsNotNone(scheduled_subtransaction.amount)
        self.assertTrue(hasattr(scheduled_subtransaction, 'memo'))
        self.assertTrue(hasattr(scheduled_subtransaction, 'payee_id'))
        self.assertTrue(hasattr(scheduled_subtransaction, 'category_id'))
        self.assertTrue(hasattr(scheduled_subtransaction, 'transfer_account_id'))

    def test_get_user(self):
        """
        This tests the get_user() from class YNABSession
        :return: nothing
        """
        user = self.ynab_session.get_user()
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.id)

    def test_get_budgets(self):
        """
        This tests the get_budgets() from class YNABSession without parameter budget_id
        :return: nothing
        """
        budgets = self.ynab_session.get_budgets()
        for budget in budgets:
            self._verify_budget(budget)

    def test_get_budgets_with_budget_id(self):
        """
        This tests the get_budgets() from class YNABSession with parameter budget_id
        :return: nothing
        """
        budgets = self.ynab_session.get_budgets()
        budget, server_knowledge = self.ynab_session.get_budgets(budgets[0].id)
        self._verify_budget(budget)
        for account in budget.accounts:
            self._verify_account(account)
        for payee in budget.payees:
            self._verify_payee(payee)
        for payee_location in budget.payee_locations:
            self._verify_payee_location(payee_location)
        for category_group in budget.category_groups:
            self._verify_category_group(category_group)
        for category in budget.categories:
            self._verify_category(category)
        for month in budget.months:
            self._verify_month(month)
            for category in month.categories:
                self._verify_category(category)
        for transaction in budget.transactions:
            self._verify_transaction(transaction)
        for subtransaction in budget.subtransactions:
            self._verify_subtransactions(subtransaction)
        for scheduled_transaction in budget.scheduled_transactions:
            self._verify_scheduled_transactions(scheduled_transaction)
        for scheduled_subtransaction in budget.scheduled_subtransactions:
            self._verify_scheduled_subtransactions(scheduled_subtransaction)
        self.assertIsNotNone(server_knowledge)

    # pylint: disable-msg=too-many-locals
    def test_pos_transaction(self):
        """
        This test will create a transaction without import_id to avoid reimporting error 422.
        If not already existing a payee named 'Testpayee' will be created.
        Prerequisites:
            A budget named 'Testing'
            An account named 'Bank'
            A category named 'Rent/Mortgage'
        :return: nothing
        """
        date = '2018-03-31'
        amount = 11000
        payee_id = None
        payee_name = 'Testpayee'
        memo = None
        cleared = 'uncleared'
        approved = False
        flag_color = None
        import_id = None
        budget_id = self.ynab_session.get_budget_id("Testing")
        self.assertIsNotNone(budget_id)
        account_name = 'Bank'
        account_id = self.ynab_session.get_account_id(budget_id, account_name)
        self.assertIsNotNone(account_id)
        category_name = 'Rent/Mortgage'
        category_id = self.ynab_session.get_category_id(budget_id, category_name)
        self.assertIsNotNone(category_id)
        transaction = self.ynab_session.build_transaction_json(account_id,   #account it
                                                               date,         #date
                                                               amount,       #amount
                                                               payee_id,     #payee id
                                                               payee_name,   #payee name
                                                               category_id,  #category id
                                                               memo,         #memo
                                                               cleared,      #cleared
                                                               approved,     #approved
                                                               flag_color,   #flag_color
                                                               import_id)    #import id
        result = self.ynab_session.post_transaction(budget_id, transaction)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.id)
        self.assertEqual(result.date, date, 'Date is different')
        self.assertEqual(result.amount, amount, 'Amount is different')
        self.assertEqual(result.memo, memo, 'Memo name is different')
        self.assertEqual(result.cleared, cleared, 'Cleared is different')
        self.assertEqual(result.approved, approved, 'Approved is different')
        self.assertEqual(result.flag_color, flag_color, 'Flag_color is different')
        self.assertEqual(result.account_id, account_id, 'Account_id is different')
        self.assertIsNotNone(result.payee_id)   # most likely unknown before the test
        self.assertEqual(result.category_id, category_id, 'Category_id is different')
        self.assertIsNone(result.transfer_account_id)
        self.assertEqual(result.import_id, import_id, 'Import_id is different')
        self.assertEqual(result.account_name, account_name, 'Account_name is different')
        self.assertEqual(result.payee_name, payee_name, 'Payee_name is different')
        self.assertEqual(result.category_name, category_name, 'Category_name is different')
        self.assertIsNotNone(result.subtransactions)
    # pylint: enable-msg=too-many-locals

    def test_post_transaction_bulk(self):
        """
        This test will create 2 transactions without import_id to avoid reimporting error 422.
        If not already existing a payee named 'Testpayee' and 'Testpayee2' will be created.
        Prerequisites:
            A budget named 'Testing'
            An account named 'Bank'
            A category named 'Rent/Mortgage'
        :return: nothing
        """
        budget_id = self.ynab_session.get_budget_id("Testing")
        self.assertIsNotNone(budget_id)
        account_name = 'Bank'
        account_id = self.ynab_session.get_account_id(budget_id, account_name)
        self.assertIsNotNone(account_id)
        category_name = 'Rent/Mortgage'
        category_id = self.ynab_session.get_category_id(budget_id, category_name)
        self.assertIsNotNone(category_id)
        transactions = [self.ynab_session.build_transaction_json(account_id,    # account id
                                                                 '2018-03-31',  # date
                                                                 123000,        # amount
                                                                 None,          # payee id
                                                                 'Testpayee',   # payee name
                                                                 category_id,   # category id
                                                                 None,          # memo
                                                                 'uncleared',   # cleared
                                                                 False,         # approved
                                                                 None,          # flag_color
                                                                 None),         # import id
                        self.ynab_session.build_transaction_json(account_id,    # account it
                                                                 '2018-04-01',  # date
                                                                 222000,        # amount
                                                                 None,          # payee id
                                                                 'Testpayee2',  # payee name
                                                                 category_id,   # category id
                                                                 None,          # memo
                                                                 'uncleared',   # cleared
                                                                 False,         # approved
                                                                 None,          # flag_color
                                                                 None)]         # import id
        real_transactions = self.ynab_session.build_transactions_json(transactions)
        result = self.ynab_session.post_transaction_bulk(budget_id, real_transactions)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.transaction_ids)
        self.assertIsNotNone(result.duplicate_import_ids)
        self.assertEqual(len(result.transaction_ids), 2)
        self.assertEqual(len(result.duplicate_import_ids), 0)

    def test_post_transaction_bulk_2(self):
        """
        This test will create 2 transactions with import_id to test reimporting prevention.
        To do this it will post transaction bulk 2 times with the same data
        If not already existing a payee named 'Testpayee' and 'Testpayee2' will be created.
        Prerequisites:
            A budget named 'Testing'
            An account named 'Bank'
            A category named 'Rent/Mortgage'
        :return: nothing
        """
        budget_id = self.ynab_session.get_budget_id("Testing")
        self.assertIsNotNone(budget_id)
        account_name = 'Bank'
        account_id = self.ynab_session.get_account_id(budget_id, account_name)
        self.assertIsNotNone(account_id)
        category_name = 'Rent/Mortgage'
        category_id = self.ynab_session.get_category_id(budget_id, category_name)
        self.assertIsNotNone(category_id)
        import_id1 = str(uuid.uuid4())
        import_id2 = str(uuid.uuid4())
        transactions = [self.ynab_session.build_transaction_json(account_id,    # account id
                                                                 '2018-03-31',  # date
                                                                 123000,        # amount
                                                                 None,          # payee id
                                                                 'Testpayee',   # payee name
                                                                 category_id,   # category id
                                                                 None,          # memo
                                                                 'uncleared',   # cleared
                                                                 False,         # approved
                                                                 None,          # flag_color
                                                                 import_id1),   # import id
                        self.ynab_session.build_transaction_json(account_id,    # account id
                                                                 '2018-04-01',  # date
                                                                 321000,        # amount
                                                                 None,          # payee id
                                                                 'Testpayee2',  # payee name
                                                                 category_id,   # category id
                                                                 None,          # memo
                                                                 'uncleared',   # cleared
                                                                 False,         # approved
                                                                 None,          # flag_color
                                                                 import_id2)]   # import id
        real_transactions = self.ynab_session.build_transactions_json(transactions)
        result = self.ynab_session.post_transaction_bulk(budget_id, real_transactions)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.transaction_ids)
        self.assertIsNotNone(result.duplicate_import_ids)
        self.assertEqual(len(result.transaction_ids), 2)
        self.assertEqual(len(result.duplicate_import_ids), 0)
        result = self.ynab_session.post_transaction_bulk(budget_id, real_transactions)
        self.assertIsNotNone(result)
        self.assertIsNotNone(result.transaction_ids)
        self.assertIsNotNone(result.duplicate_import_ids)
        self.assertEqual(len(result.transaction_ids), 0)
        self.assertEqual(len(result.duplicate_import_ids), 2)


if __name__ == '__main__':
    unittest.main()
