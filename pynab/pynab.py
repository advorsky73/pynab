#!/usr/bin/env python3

"""
This module provides classes for easy handling of the YNAB API.
"""

import sys
import json
import requests
import urllib
from collections import namedtuple


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
        :param json_string:
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

    def _internal_get_stuff(self, url, key1, key2, check_for_404=False):
        """
        get information from YNAB the generic way
        :return: (list of) object(s) with information about requested data
        :throws: if an error occurs an exception is raised
        """
        # get the response from YNAB
        r = self.session.get(self.base_url + url)

        # check for success
        if r.status_code == 200:
            result = json.dumps(json.loads(r.text)[key1][key2])
            return self._build_json_object(result)

        # check for an empty account
        if check_for_404 and r.status_code == 404:
            return None

        # build error information and raise an exception
        raise Exception(self._build_exception_string(json.loads(r.text)))

    def get_user(self):
        """
        gets user information from YNAB
        :return: object with user information
        :throws: if an error occurs an exception is raised
        """

        # get the response from YNAB
        r = self.session.get(self.base_url + "user")

        # check for success
        if r.status_code == 200:
            user = json.dumps(json.loads(r.text)["data"]["user"])
            return self._build_json_object(user)

        # build error information and raise an exception
        raise Exception(self._build_exception_string(json.loads(r.text)))

    def get_budgets(self, budget_id=None, last_knowledge_of_server=None):
        """
        get budget(s) information from YNAB
        :return: (list of) object(s) with information about budget(s)
        :throws: if an error occurs an exception is raised
        """
        url = "budgets"
        # get the response from YNAB
        if budget_id is None:
            return self._internal_get_stuff(url, 'data', 'budgets', True)
        else:
            if last_knowledge_of_server is None:
                return self._internal_get_stuff(url + "/" + budget_id, 'data', 'budget', True)
            else:
                url = url + "/" + budget_id + \
                      "?last_knowledge_of_server =" + last_knowledge_of_server
                return self._internal_get_stuff(url, 'data', 'budget', True)

    def get_accounts(self, budget_id, account_id=None):
        """
        get account(s) information from YNAB
        :return: (list of) object(s) with information about account(s)
        :throws: if an error occurs an exception is raised
        """
        url = "budgets/" + budget_id + "/accounts"
        # get the response from YNAB
        if account_id is None:
            return self._internal_get_stuff(url, 'data', 'accounts', True)
        else:
            return self._internal_get_stuff(url + "/" + account_id, 'data', 'account', True)

    def get_categories(self, budget_id, category_id=None):
        """
        get categorie(s) information from YNAB
        :return: (list of) object(s) with information about categorie(s)
        :throws: if an error occurs an exception is raised
        """
        url = "budgets/" + budget_id + "/categories"
        # get the response from YNAB
        if category_id is None:
            return self._internal_get_stuff(url, 'data', 'category_groups', True)
        else:
            return self._internal_get_stuff(url + "/" + category_id, 'data', 'category', True)

    def get_payees(self, budget_id, payee_id=None):
        """
        get payee(s) information from YNAB
        :return: (list of) object(s) with information about payee(s)
        :throws: if an error occurs an exception is raised
        """
        url = "budgets/" + budget_id + "/payees"
        # get the response from YNAB
        if payee_id is None:
            return self._internal_get_stuff(url, 'data', 'payees', True)
        else:
            return self._internal_get_stuff(url + "/" + payee_id, 'data', 'payee', True)

    def get_months(self, budget_id, month_id=None):
        """
        get month(s) information from YNAB
        :return: (list of) object(s) with information about month(s)
        :throws: if an error occurs an exception is raised
        """
        url = "budgets/" + budget_id + "/months"
        # get the response from YNAB
        if month_id is None:
            return self._internal_get_stuff(url, 'data', 'months', True)
        else:
            return self._internal_get_stuff(url + "/" + month_id, 'data', 'month', True)

    def get_transactions(self,
                         budget_id,
                         account_id=None,
                         categories_id=None,
                         payees_id=None,
                         transaction_id=None,
                         since_date=None,
                         ttype=None):
        """
        get transaction(s) information from YNAB
        :return: (list of) object(s) with information about transaction(s)
        :throws: if an error occurs an exception is raised
        """
        url = "budgets/" + budget_id + "/transactions"
        # get the response from YNAB
        if transaction_id is None:
            if account_id is not None:
                assert(categories_id is None and payees_id is None)
                url = "budgets/" + budget_id + "/accounts/" + account_id + "/transactions"
            if categories_id is not None:
                assert(account_id is None and payees_id is None)
                url = "budgets/" + budget_id + "/categories/" + categories_id + "/transactions"
            if payees_id is not None:
                assert(account_id is None and categories_id is None)
                url = "budgets/" + budget_id + "/payees/" + payees_id + "/transactions"
            url_vars = {}
            if since_date is not None:
                url_vars.update({'since_date': since_date})
            if ttype is not None:
                assert(account_id is None and
                       categories_id is None and
                       payees_id is None)
                url_vars.update({'type': ttype})
            return self._internal_get_stuff(url + urllib.parse.urlencode(url_vars),
                                            'data', 'transactions', True)
        else:
            assert(since_date is None and
                   ttype is None and
                   account_id is None and
                   payees_id is None and
                   categories_id is None)
            return self._internal_get_stuff(url + "/" + transaction_id, 'data', 'transaction', True)


if __name__ == '__main__':
    #y = YNABSession(sys.argv[1])
    #b = y.get_budgets()
    #print(b)
    #bt = y.get_budgets(b[0].id)
    #print(bt)
    #a = y.get_accounts(b[0].id)
    #for aa in a:
    #    print(aa)
    #c = y.get_categories(b[0].id)
    #for cc in c:
    #    print(cc)
    #p = y.get_payees(b[0].id)
    #for pp in p:
    #    print(pp)
    #m = y.get_months(b[0].id)
    #for mm in m:
    #    print(mm)
    #t = y.get_transactions(b[0].id)
    #for tt in t:
    #    print(tt)
    print("Module not ment to run on its own...")

