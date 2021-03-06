#!/usr/bin/env python3

"""
This module provides a class for direct handling of the YNAB API.
"""

from urllib.parse import urlencode
from collections import namedtuple
import json
import requests


class YNABSession(object):
    """
    This class holds and handles a YNAB (requests) session including authentication.
    """

    def __init__(self, ynab_access_token):
        """
        Constructor
        """
        # create the header with the Bearer token for YNAB
        self.requests_header = {"accept": "application/json",
                                "Authorization": "Bearer " + ynab_access_token}
        # create the requests session with the custom header fields
        self.session = requests.Session()
        self.session.headers.update(self.requests_header)
        # base url for all api calls
        self.base_url = "https://api.youneedabudget.com/v1/"

    def __del__(self):
        """
        Destructor
        """
        # close and destroy requests session
        self.session.close()
        del self.session

    @staticmethod
    def _build_json_object(json_string):
        """
        creates an object with attributes from json attributes
        :param json_string: json string representation
        :return: python object
        """
        return json.loads(json_string, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    @staticmethod
    def _build_exception_string(json_data):
        """
        internal helper to build the exception string from a json object
        :param json_data: the json object
        :return:  the exception text built from the json object
        """
        return json_data["error"]["id"] + " : " + \
               json_data["error"]["name"] + " (" + \
               json_data["error"]["detail"] + ")"

    def _internal_get_stuff(self, url, key1, key2, key2alt=None):
        """
        get information from YNAB the generic way
        :param url: url part for the request appended to base_url member
        :param key1: first key to access json dictionary after retrieval
        :param key2: second key to access json dictionary after retrieval
        :param key2alt: alternative second key to access json dictionary after retrieval
        :return: (list of) object(s) with information about requested data
                 if key2alt is set, then a second object is returned representing it
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        result = self.session.get(self.base_url + url)
        # check for success
        if result.status_code == 200:
            resultkey = json.dumps(json.loads(result.text)[key1][key2])
            if key2alt is None:
                return self._build_json_object(resultkey)
            resultkey2 = json.dumps(json.loads(result.text)[key1][key2alt])
            return self._build_json_object(resultkey), self._build_json_object(resultkey2)
        # check for an empty account
        if result.status_code == 404:
            return None
        # build error information and raise an exception
        raise Exception(self._build_exception_string(json.loads(result.text)))

    def _internal_put_stuff(self, url, json_data):
        """
        work in progress...
        :param url:
        :param data:
        :return:
        """
        raise Exception("NOT YET IMPLEMENTED")

    def _internal_post_stuff(self, url, json_data, key1, key2):
        """
        posts data to ynab URL the generic way
        :param url: url part for the request appended to base_url member
        :param json_data: json data to be posted to ynab
        :param key1: first key to access json dictionary after retrieval
        :param key2: second key to access json dictionary after retrieval
        :return: object with created transaction if successful, None if import_id already existed
        :throws: if an error occurs an exception is raised
        """
        # post the data to YNAB
        result = self.session.post(self.base_url + url, json=json_data)
        if result.status_code == 201:
            return self._build_json_object(json.dumps(json.loads(result.text)[key1][key2]))
        # check for 422 (A transaction with the same import_id already exists)
        if result.status_code == 422:
            return None
        # build error information and raise an exception
        raise Exception(self._build_exception_string(json.loads(result.text)))

    def get_user(self):
        """
        API call
        gets user information from YNAB
        :return: object with user information
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        result = self.session.get(self.base_url + "user")
        # check for success
        if result.status_code == 200:
            user = json.dumps(json.loads(result.text)["data"]["user"])
            return self._build_json_object(user)
        # build error information and raise an exception
        raise Exception(self._build_exception_string(json.loads(result.text)))

    def get_budgets(self, budget_id=None, last_knowledge_of_server=None):
        """
        API call
        get budget(s) information from YNAB
        :param budget_id: optional; id of the budget to be received. If not set all budgets
                will be retrieved
        :param last_knowledge_of_server: optional; The starting server knowledge. If provided,
                only entities that have changed since last_knowledge_of_server will be included.
        :return: (list of) object(s) with information about budget(s)
                 if budget_id is presented a second return value stands for server_knowledge
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        url = "budgets"
        if budget_id is None:
            return self._internal_get_stuff(url, 'data', 'budgets')
        if last_knowledge_of_server is None:
            return self._internal_get_stuff(url + "/" + budget_id,
                                            'data',
                                            'budget',
                                            'server_knowledge')
        return self._internal_get_stuff(url, 'data', 'budget')

    def get_accounts(self, budget_id, account_id=None):
        """
        API call
        get account(s) information from YNAB
        :param budget_id:  id of the budget to get the account data from
        :param account_id: optional; id of the account to be received. If not set all accounts will
                be retrieved
        :return: (list of) object(s) with information about account(s)
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        url = "budgets/" + budget_id + "/accounts"
        if account_id is None:
            return self._internal_get_stuff(url, 'data', 'accounts')
        return self._internal_get_stuff(url + "/" + account_id, 'data', 'account')

    def get_categories(self, budget_id, category_id=None):
        """
        API call
        get categorie(s) information from YNAB
        :param budget_id:  id of the budget to get the account data from
        :param category_id: optional; id of the category to be received. If not set all categories
                will be retrieved
        :return: (list of) object(s) with information about categorie(s)
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        url = "budgets/" + budget_id + "/categories"
        if category_id is None:
            return self._internal_get_stuff(url, 'data', 'category_groups')
        return self._internal_get_stuff(url + "/" + category_id, 'data', 'category')

    def get_payees(self, budget_id, payee_id=None):
        """
        API call
        get payee(s) information from YNAB
        :param budget_id:  id of the budget to get the account data from
        :param payee_id: optional; id of the payee to be received. If not set all payees will be
                retrieved
        :return: (list of) object(s) with information about payee(s)
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        url = "budgets/" + budget_id + "/payees"
        if payee_id is None:
            return self._internal_get_stuff(url, 'data', 'payees')
        return self._internal_get_stuff(url + "/" + payee_id, 'data', 'payee')

    def get_payee_locations(self, budget_id, payee_location_id=None):
        """
        API call
        get get_payee_location(s) information from YNAB
        :param budget_id:  id of the budget to get the account data from
        :param payee_location_id: optional; id of the payee_location to be received.
                If not set all payee_locations will be retrieved
        :return: (list of) object(s) with information about payee_location(s)
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        url = "budgets/" + budget_id + "/payee_locations"
        if payee_location_id is None:
            return self._internal_get_stuff(url, 'data', 'payee_locations')
        return self._internal_get_stuff(url + "/" + payee_location_id, 'data', 'payee_location')

    def get_payee_locations_for_payee(self, budget_id, payee_id):
        """
        API call
        get get_payee_location(s) information from YNAB
        :param budget_id: id of the budget to get the account data from
        :param payee_id:  id of the payee for which all payee_locations are to be received.
        :return: list of objects with information about payee_locations
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        url = "budgets/" + budget_id + "/payee" + payee_id + "/payee_locations"
        return self._internal_get_stuff(url, 'data', 'payee_locations')

    def get_months(self, budget_id, month_id=None):
        """
        API call
        get month(s) information from YNAB
        :param budget_id:  id of the budget to get the account data from
        :param month_id: optional; id of the month to be received. If not set all months will be
                retrieved
        :return: (list of) object(s) with information about month(s)
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        url = "budgets/" + budget_id + "/months"
        if month_id is None:
            return self._internal_get_stuff(url, 'data', 'months')
        return self._internal_get_stuff(url + "/" + month_id, 'data', 'month')

    def get_transactions(self, budget_id, transaction_id=None, since_date=None, ttype=None):
        """
        API call
        get transaction(s) information from YNAB
        :param budget_id:       all transactions for this budget will be retrieved if set alone
        :param transaction_id:  optional; only one specific transaction will be retrieved
        :param since_date:      optional; limit the retrieved data to transactions since this date
        :param ttype:           optional; limit the retrieved data to transactions matching the type
        :return: (list of) object(s) with information about transaction(s)
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        url = "budgets/" + budget_id + "/transactions"
        url_vars = {}
        if transaction_id is None:
            if since_date is not None:
                url_vars.update({'since_date': since_date})
            if ttype is not None:
                url_vars.update({'type': ttype})
            return self._internal_get_stuff(url + urlencode(url_vars), 'data', 'transactions')
        return self._internal_get_stuff(url + "/" + transaction_id, 'data', 'transaction')

    def get_transactions_for_account(self, budget_id, account_id, since_date=None):
        """
        API call
        get transaction(s) information from YNAB
        :param budget_id:  all transactions for this budget will be retrieved if set alone
        :param account_id: all transactions for this account will be retrieved
        :param since_date: optional; limit the retrieved data to transactions since this date
        :return: (list of) object(s) with information about transaction(s)
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        url_vars = {}
        url = "budgets/" + budget_id + "/accounts/" + account_id + "/transactions"
        if since_date is not None:
            url_vars.update({'since_date': since_date})
        return self._internal_get_stuff(url + urlencode(url_vars), 'data', 'transactions')

    def get_transactions_for_category(self, budget_id, category_id, since_date=None):
        """
        API call
        get transaction(s) information from YNAB
        :param budget_id:   all transactions for this budget will be retrieved if set alone
        :param category_id: all transactions for this category will be retrieved
        :param since_date:  optional; limit the retrieved data to transactions since this date
        :return: (list of) object(s) with information about transaction(s)
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        url_vars = {}
        url = "budgets/" + budget_id + "/categories/" + category_id + "/transactions"
        if since_date is not None:
            url_vars.update({'since_date': since_date})
        return self._internal_get_stuff(url + urlencode(url_vars), 'data', 'transactions')

    def get_transactions_for_payee(self, budget_id, payees_id, since_date=None):
        """
        API call
        get transaction(s) information from YNAB
        :param budget_id:  all transactions for this budget will be retrieved if set alone
        :param payees_id:  all transactions for this payee will be retrieved
        :param since_date: optional; limit the retrieved data to transactions since this date
        :return: (list of) object(s) with information about transaction(s)
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        url_vars = {}
        url = "budgets/" + budget_id + "/payees/" + payees_id + "/transactions"
        if since_date is not None:
            url_vars.update({'since_date': since_date})
        return self._internal_get_stuff(url + urlencode(url_vars), 'data', 'transactions')

    def get_scheduled_transactions(self, budget_id, scheduled_transaction_id=None):
        """
        API call
        get scheduled transaction(s) information from YNAB
        :param budget_id: all transactions for this budget will be retrieved if set alone
        :param scheduled_transaction_id: optional; only one specific transaction will be retrieved
        :return: (list of) object(s) with information about transaction(s)
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        url = "budgets/" + budget_id + "/scheduled_transactions"
        if scheduled_transaction_id is None:
            return self._internal_get_stuff(url, 'data', 'scheduled_transactions')
        return self._internal_get_stuff(url + "/" + scheduled_transaction_id,
                                        'data',
                                        'scheduled_transaction')

    def post_transaction(self, budget_id, transaction):
        """
        API call
        posts a single transaction to YNAB
        :param budget_id: the budget id which this transaction is for
        :param transaction: object containing the transaction data from build_transaction
        :return: True if a transaction has been created; False if it had been skipped
        :throws: if an error occurs an exception is raised
        """
        url = "budgets/" + budget_id + "/transactions"
        return self._internal_post_stuff(url, transaction, 'data', 'transaction')

    def post_transaction_bulk(self, budget_id, transactions):
        """
        API call
        posts transactions as bulk to YNAB
        :param budget_id: the budget id which these transactions are for
        :param transactions: array of json objects containing the transaction data
        :return: json object with bulk import information
        :throws: if an error occurs an exception is raised
        """
        url = "budgets/" + budget_id + "/transactions/bulk"
        return self._internal_post_stuff(url, transactions, 'data', 'bulk')

    def put_transaction(self, budget_id, transaction_id, transaction):
        """
        API call
        puts an update of an existing transaction to YNAB
        :param budget_id: the budget id which this transaction is for
        :param transaction_id: the id of the transaction to be updated
        :param transaction: json object containing the transaction data
        :return: True if a transaction has been created
        :throws: if an error occurs an exception is raised
        """
        url = "budgets/" + budget_id + "/transactions/" + transaction_id
        return self._internal_put_stuff(url, transaction)


if __name__ == '__main__':
    print("Module not ment to run on its own...")
