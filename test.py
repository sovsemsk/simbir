import csv
import time
# import locale
from datetime import datetime

import allure
import pytest
from dateutil.parser import parse
from selenium import webdriver

from page import Account, Customer, Login, Transactions

base_url = "https://www.globalsqa.com"

options = webdriver.ChromeOptions()
options.set_capability("selenoid:options", {
    "enableVNC": True,
    "screenResolution": "1280x1024x24",
    "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru", "LC_ALL=ru_RU.UTF-8"]
})

@pytest.fixture(scope="session")
def driver():
    # driver = webdriver.Remote(command_executor="http://9bea7b5c.portrate.io/wd/hub", options=options)
    driver = webdriver.Remote(command_executor="http://185.93.109.120:4444/wd/hub", options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def write_transactions(transactions):
    # Не очень понятно, в тз написано ДД Месяц ГГГГ ЧЧ:ММ:СС, если дата нужна на русском то нужно сетнуть локаль
    # locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
    transaction_types = ("Credit", "Debit")
    filename = f"csv/transations_list_{datetime.now()}.csv"

    with open(filename, "w") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(("Date", "Balance", "Type"))

        for transaction in transactions:
            writer.writerow((
                parse(transaction.date).strftime("%d %B %Y %H:%M:%S"),
                int(transaction.amount),
                transaction.type if transaction.type in transaction_types else "Unknown transaction type"
            ))

    # locale.setlocale(locale.LC_ALL, "")
    return filename

@allure.suite("Banking test")
@allure.story("Checking the users balance and the count of transactions after depositing and withdrawing")
@allure.title("Test balance and transactions as Harry Potter")
def test_balance_and_transactions(driver):
    with allure.step("Login as Harry Potter"):
        login_page = Login(driver, base_url)
        (
            login_page
            .open()
            .click_login_button()
        )

        customer_page = Customer(driver, base_url)
        (
            customer_page
            .open()
            .change_user_select()
            .submit_user_form()
        )

    with allure.step("Checking the Harry Potter balance after depositing and withdrawing"):
        account_page = Account(driver, base_url)
        (
            account_page
            .open()
            .click_deposit_button()
            .change_deposit_amount_input()
            .submit_deposit_form()
            .click_withdrawl_button()
            .change_withdrawl_amount_input()
            .submit_withdrawl_form()
        )

        assert int(account_page.balance) == 0

    with allure.step("Checking the Harry Potter transactions count after depositing and withdrawing"):
        transactions_page = Transactions(driver, base_url).open()
        filename = write_transactions(transactions_page.transactions)
        allure.attach.file(filename, name=f"CSV Transactions list ({filename})", attachment_type=allure.attachment_type.CSV)
        assert len(transactions_page.transactions) == 2
