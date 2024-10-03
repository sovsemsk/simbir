import allure

from driver import driver
from utils import write_transactions_csv
from pages import Account, Customer, Login, Transactions

base_url = "https://www.globalsqa.com"

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
        filename = write_transactions_csv(transactions_page.transactions)
        allure.attach.file(filename, name=f"Transactions list", attachment_type=allure.attachment_type.CSV)
        assert len(transactions_page.transactions) == 2
