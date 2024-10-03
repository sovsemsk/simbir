import csv
# import locale
from datetime import datetime
from dateutil.parser import parse

def fib(n):
    a, b = 0, 1
    for __ in range(n):
        a, b = b, a + b
    return a

def write_transactions_csv(transactions):
    # Не очень понятно, в тз написано ДД Месяц ГГГГ ЧЧ:ММ:СС, если дата нужна на русском то нужно сетнуть локаль
    # locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
    transaction_types = ("Credit", "Debit")
    filename = f"csv/transations_list_{datetime.now()}.csv"

    with open(filename, "w") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow(("Date", "Amount", "Type"))

        for transaction in transactions:
            writer.writerow((
                parse(transaction.date).strftime("%d %B %Y %H:%M:%S"),
                int(transaction.amount),
                transaction.type if transaction.type in transaction_types else "Unknown transaction type"
            ))

    # locale.setlocale(locale.LC_ALL, "")
    return filename
