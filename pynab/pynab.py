#!/usr/bin/env python3

"""
This module provides classes for easy handling of the YNAB API.
"""

from .ynap_api import YNABSession

class YNAB(YNABSession):
    """
    This class is a convenience layer to the direct YNAB API implementation.
    """

    # pylint: disable-msg=too-many-arguments
    def build_transaction_json(self,
                               account_id,
                               date,
                               amount,
                               payee_id,
                               payee_name,
                               category_id,
                               memo,
                               cleared,
                               approved,
                               flag_color,
                               import_id):
        """
        This creates an object to be used with put_transaction or post_transaction commands
        :param account_id:  string
        :param date:        string
        :param amount:      number
        :param payee_id:    string|null
        :param payee_name:  string|null
        :param category_id: string|null
        :param memo:        string|null
        :param cleared:     string 'cleared'
        :param approved:    boolean
        :param flag_color:  string|null
        :param import_id:   string|null
        :return: a json object filled with given data
        """
        result = {
            "transaction": {
                "account_id": account_id,
                "date": date,
                "amount": amount,
                "payee_id": payee_id,
                "payee_name": payee_name,
                "category_id": category_id,
                "memo": memo,
                "cleared": cleared,
                "approved": approved,
                "flag_color": flag_color,
                "import_id": import_id
            }
        }
        return result
    # pylint: enable-msg=too-many-arguments

    def get_budget_id(self, budget_name):
        """
        retrieves the budget id from budget name
        :param budget_name: the budget name to search for
        :return: budget id if the budget was found; None if not
        :throws: does not catch exceptions from get_budgets()
        """
        # get the budgets from ynab
        budgets = self.get_budgets()
        results = [budget.id for budget in budgets if budget.name == budget_name]
        if not results:
            return None
        return results[0]

    def get_account_id(self, budget_id, account_name):
        """
        retrieves the account id from acoount name and budget id
        :param budget_id: budget id the account belongs to
        :param account_name: the account name to look for
        :return: account id if the account was found; None if not
        :throws: does not catch exceptions from get_accounts()
        """
        # get the accounts from YNAb
        accounts = self.get_accounts(budget_id)
        results = [account.id for account in accounts if account.name == account_name]
        if not results:
            return None
        return results[0]

    def get_payee_id(self, budget_id, payee_name):
        """
        retrieves the payee id from payee name
        :param payee_name: the payee name to search for
        :return: payee id if the payee was found; None if not
        :throws: does not catch exceptions from get_payees()
        """
        # get the payees from ynab
        payees = self.get_payees(budget_id)
        results = [payee.id for payee in payees if payee.name == payee_name]
        if not results:
            return None
        return results[0]

    def get_category_id(self, budget_id, category_name):
        """
        retrieves the category id from category name
        :param category_name: the category name to search for
        :return: category id if the category was found; None if not
        :throws: does not catch exceptions from get_categories()
        """
        # get the categories from ynab
        category_groups = self.get_categories(budget_id)
        results = [category.id
                   for category_group in category_groups
                   for category in category_group.categories
                   if category.name == category_name]
        if not results:
            return None
        return results[0]

    def import_csv(self, budget_id, account_id, csv_filename):
        """
        imports a csv like the website does. requires same csv format as apps.youneedabudget.com
        :param budget_id: the budget the transactions should be imported to
        :param account_id: the account the transactions should be imported to
        :param csv_filename: filename of the csv file containing the transactions
        :return: 2 values are returned: amount_imported, amount_skipped
        :throws: if an error occurs an exception is raised
        """
        raise Exception("NOT YET IMPLEMENTED")



if __name__ == '__main__':
    print("Module not ment to run on its own...")
