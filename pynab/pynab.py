#!/usr/bin/env python3

"""
This module provides classes for easy handling of the YNAB API.
"""

import sys
import json
import requests
from collections import namedtuple


class YNABUser(object):
    """
    Data class for YNAB user
    """

    def __init__(self, json_data):
        """
        Constructor
        """
        self.json_data = json_data

    def get_id(self):
        """
        :return: the id for the user
        """
        return self.json_data["data"]["user"]["id"]


class YNABCurrencyFormat(object):
    """
    Data class for YNAB currency format
    """

    def __init__(self, json_data):
        """
        Constructor
        """
        self.json_data = json_data

    def get_iso_code(self):
        return self.json_data["iso_code"]

    def get_example_format(self):
        return self.json_data["example_format"]

    def get_decimal_digits(self):
        return self.json_data["decimal_digits"]

    def get_symbol_first(self):
        return self.json_data["symbol_first"]

    def get_group_separator(self):
        return self.json_data["group_separator"]



class YNABBudget(object):
    """
    Data class for one YNAB budget returned by /budgets
    json data starts at data/budgets/.
    """

    def __init__(self, json_data):
        """
        Constructor
        """
        self.json_data = json_data

    def get_id(self):
        """
        :return: id of the budget
        """
        return self.json_data["id"]

    def get_name(self):
        return self.json_data["name"]

    def get_last_modified_on(self):
        return self.json_data["last_modified_on"]

    def get_date_format(self):
        return self.json_data["date_format"]["format"]

    def get_currency_format(self):
        return YNABCurrencyFormat(self.json_data["currency_format"])



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
        # destroy requets session
        del self.session

    def _build_json_object(self, json_string):
        """
        creates an object with attributes from json attributes
        :param json_string:
        :return: python object
        """
        return json.loads(json_string, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

    def _build_exception_string(self, j):
        """
        internal helper to build the exception string from a json object
        :param j: the json object
        :return:  the exception text built from the json object
        """
        return j["error"]["id"] + " : " + j["error"]["name"] + " : " + j["error"]["detail"]

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

    def get_budgets(self, budget_id=None):
        """
        get budget(s) information from YNAB
        :return: (list of) object(s) with information about budget(s)
        :throws: if an error occurs an exception is raised
        """

        # get the response from YNAB
        if budget_id is None:
            r = self.session.get(self.base_url + "budgets")
        else:
            r = self.session.get(self.base_url + "budgets/" + budget_id)

        # check for success
        if r.status_code == 200:
            if budget_id is None:
                result = json.dumps(json.loads(r.text)["data"]["budgets"])
            else:
                result = json.dumps(json.loads(r.text)["data"]["budget"])
            return self._build_json_object(result)

        # check for an empty account
        if r.status_code == 404:
            if budget_id is None:
                return []
            else:
                return None

        # build error information and raise an exception
        raise Exception(self._build_exception_string(json.loads(r.text)))

    def get_accounts(self, budget_id, account_id=None):
        """
        get account(s) information from YNAB
        :return: (list of) object(s) with information about account(s)
        :throws: if an error occurs an exception is raised
        """

        # get the response from YNAB
        if account_id is None:
            r = self.session.get(self.base_url + "budgets/" + budget_id + "/accounts")
        else:
            r = self.session.get(self.base_url + "budgets/" + budget_id + "/accounts/" + account_id)

        # check for success
        if r.status_code == 200:
            if account_id is None:
                result = json.dumps(json.loads(r.text)["data"]["accounts"])
            else:
                result = json.dumps(json.loads(r.text)["data"]["account"])
            return self._build_json_object(result)

        # check for an empty account
        if r.status_code == 404:
            if account_id is None:
                return []
            else:
                return None

            # build error information and raise an exception
        raise Exception(self._build_exception_string(json.loads(r.text)))

    def get_categories(self, budget_id, category_id=None):
        """
        get categorie(s) information from YNAB
        :return: (list of) object(s) with information about categorie(s)
        :throws: if an error occurs an exception is raised
        """

        # get the response from YNAB
        if category_id is None:
            r = self.session.get(self.base_url + "budgets/" + budget_id + "/categories")
        else:
            r = self.session.get(self.base_url + "budgets/" + budget_id + "/categories/" + category_id)

        # check for success
        if r.status_code == 200:
            if category_id is None:
                result = json.dumps(json.loads(r.text)["data"]["category_groups"])
            else:
                result = json.dumps(json.loads(r.text)["data"]["category"])
            return self._build_json_object(result)

        # check for an empty account
        if r.status_code == 404:
            if category_id is None:
                return []
            else:
                return None

            # build error information and raise an exception
        raise Exception(self._build_exception_string(json.loads(r.text)))

    def get_payees(self, budget_id, payee_id=None):
        """
        get payee(s) information from YNAB
        :return: (list of) object(s) with information about payee(s)
        :throws: if an error occurs an exception is raised
        """

        # get the response from YNAB
        if payee_id is None:
            r = self.session.get(self.base_url + "budgets/" + budget_id + "/payees")
        else:
            r = self.session.get(self.base_url + "budgets/" + budget_id + "/payees/" + payee_id)

        # check for success
        if r.status_code == 200:
            if payee_id is None:
                result = json.dumps(json.loads(r.text)["data"]["payees"])
            else:
                result = json.dumps(json.loads(r.text)["data"]["payee"])
            return self._build_json_object(result)

        # check for an empty account
        if r.status_code == 404:
            if payee_id is None:
                return []
            else:
                return None

            # build error information and raise an exception
        raise Exception(self._build_exception_string(json.loads(r.text)))




y = YNABSession(sys.argv[1])
#u = y.get_user()
#print(u)
#print(u.id)
b = y.get_budgets()
#for bs in b:
#    print(bs)
#bt = y.get_budgets("c0a28ec7-4d43-4b3f-acaf-15b4425cd9bd")
#print(bt)
#a = y.get_accounts(b[0].id)
#for aa in a:
#    print(aa)
#c = y.get_categories(b[0].id)
#for cc in c:
#    print(cc)
p = y.get_payees(b[0].id)
for pp in p:
    print(pp)
