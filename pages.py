import time
from datetime import datetime

from pypom import Page, Region
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from utils import fib


class Login(Page):
    URL_TEMPLATE = "/angularJs-protractor/BankingProject/#/login"

    _login_button_locator = (By.XPATH, ".//button[@ng-click='customer()']")

    @property
    def loaded(self):
        return self.find_element(*self._login_button_locator).is_displayed()

    def click_login_button(self):
        self.find_element(*self._login_button_locator).click()
        return self


class Customer(Page):
    URL_TEMPLATE = "/angularJs-protractor/BankingProject/#/customer"

    _user_form_locator = (By.XPATH, ".//form[@ng-submit='showAccount()']")
    _user_select_locator = (By.XPATH, ".//select[@ng-model='custId']")

    @property
    def loaded(self):
        return self.find_element(*self._user_select_locator).is_displayed()

    def change_user_select(self):
        user_select = self.find_element(*self._user_select_locator)
        Select(user_select).select_by_visible_text("Harry Potter")
        return self

    def submit_user_form(self):
        self.find_element(*self._user_form_locator).submit()
        return self


class Account(Page):
    URL_TEMPLATE = "/angularJs-protractor/BankingProject/#/account"

    # Индексы идут с 0 поэтому инкремент на 1 делать не нужно
    _fib_by_date = fib(datetime.now().day)

    _amount_input_locator = (By.XPATH, ".//input[@ng-model='amount']")
    _balance_span_locator = (By.XPATH, ".//strong[@class='ng-binding'][2]")
    _deposit_button_locator = (By.XPATH, ".//button[@ng-click='deposit()']")
    _deposit_form_locator = (By.XPATH, ".//form[@ng-submit='deposit()']")
    _transactions_button_locator = (By.XPATH, ".//button[@ng-click='transactions()']")
    _withdrawl_button_locator = (By.XPATH, ".//button[@ng-click='withdrawl()']")
    _withdrawl_form_locator = (By.XPATH, ".//form[@ng-submit='withdrawl()']")

    @property
    def loaded(self):
        return self.find_element(*self._deposit_button_locator).is_displayed()

    @property
    def balance(self):
        return self.find_element(*self._balance_span_locator).text

    def click_deposit_button(self):
        self.find_element(*self._deposit_button_locator).click()
        return self

    def change_deposit_amount_input(self):
        self.find_element(*self._deposit_form_locator).find_element(*self._amount_input_locator).send_keys(self._fib_by_date)
        return self

    def submit_deposit_form(self):
        self.find_element(*self._deposit_form_locator).submit()
        time.sleep(1)
        return self

    def click_withdrawl_button(self):
        self.find_element(*self._withdrawl_button_locator).click()
        return self

    def change_withdrawl_amount_input(self):
        self.find_element(*self._withdrawl_form_locator).find_element(*self._amount_input_locator).send_keys(self._fib_by_date)
        return self

    def submit_withdrawl_form(self):
        self.find_element(*self._withdrawl_form_locator).submit()
        time.sleep(1)
        return self


class Transactions(Page):
    URL_TEMPLATE = "/angularJs-protractor/BankingProject/#/listTx"

    _transaction_table_locator = (By.XPATH, ".//table")
    _transaction_tr_locator = (By.XPATH, ".//tbody//tr")

    @property
    def loaded(self):
        return self.find_element(*self._transaction_table_locator).is_displayed()

    @property
    def transactions(self):
        return [self.Transaction(self, el) for el in self.find_elements(*self._transaction_tr_locator)]

    class Transaction(Region):
        _amount_td_locator = (By.XPATH, ".//td[2]")
        _date_td_locator = (By.XPATH, ".//td[1]")
        _type_td_locator = (By.XPATH, ".//td[3]")

        @property
        def amount(self):
            return self.find_element(*self._amount_td_locator).text

        @property
        def date(self):
            return self.find_element(*self._date_td_locator).text

        @property
        def type(self):
            return self.find_element(*self._type_td_locator).text
