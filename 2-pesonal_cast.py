# bale -> parsaeghbali 
# address bot -> @python_learnbot

import csv
import os
from datetime import datetime


class ExpenseManager:

    FILE_NAME = "transactions.csv"

    def __init__(self):
        self.create_file()

    def create_file(self):
        if not os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "w", newline="") as file:
                writer = csv.writer(file)

                writer.writerow([
                    "date",
                    "type",
                    "category",
                    "amount"
                ])

    def add_income(self):

        category = input("Income Category: ")
        amount = float(input("Amount: "))

        self.save_transaction(
            "income",
            category,
            amount
        )

        print("✅ Income added successfully.")

    def add_expense(self):

        category = input("Expense Category: ")
        amount = float(input("Amount: "))

        self.save_transaction(
            "expense",
            category,
            amount
        )

        print("✅ Expense added successfully.")

    def save_transaction(self,
                         trans_type,
                         category,
                         amount):

        with open(self.FILE_NAME,
                  "a",
                  newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d"),
                trans_type,
                category,
                amount
            ])

    def show_balance(self):

        income = 0
        expense = 0

        with open(self.FILE_NAME,
                  "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                amount = float(row["amount"])

                if row["type"] == "income":
                    income += amount
                else:
                    expense += amount

        balance = income - expense

        print("\n===== Balance =====")
        print(f"Total Income : {income}")
        print(f"Total Expense: {expense}")
        print(f"Balance      : {balance}")

    def monthly_report(self):

        current_month = datetime.now().strftime("%Y-%m")

        expenses = {}

        total_income = 0
        total_expense = 0

        with open(self.FILE_NAME,
                  "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                if row["date"].startswith(current_month):

                    amount = float(row["amount"])

                    if row["type"] == "income":
                        total_income += amount

                    else:

                        total_expense += amount

                        category = row["category"]

                        expenses[category] = (
                            expenses.get(category, 0)
                            + amount
                        )

        print("\n===== Monthly Report =====")

        print(f"Month: {current_month}")
        print(f"Income : {total_income}")
        print(f"Expense: {total_expense}")
        print(
            f"Balance: {total_income - total_expense}"
        )

        print("\nExpense Categories:")

        for category, amount in expenses.items():

            print(
                f"{category:<15} : {amount}"
            )

    def show_all_transactions(self):

        print("\n===== Transactions =====")

        with open(self.FILE_NAME,
                  "r") as file:

            reader = csv.DictReader(file)

            for row in reader:

                print(
                    f"{row['date']} | "
                    f"{row['type']} | "
                    f"{row['category']} | "
                    f"{row['amount']}"
                )


def main():

    manager = ExpenseManager()

    while True:

        print("\n===== Expense Tracker =====")

        print("1. Add Income")
        print("2. Add Expense")
        print("3. Show Balance")
        print("4. Monthly Report")
        print("5. Show Transactions")
        print("6. Exit")

        choice = input("Choose: ")

        if choice == "1":
            manager.add_income()

        elif choice == "2":
            manager.add_expense()

        elif choice == "3":
            manager.show_balance()

        elif choice == "4":
            manager.monthly_report()

        elif choice == "5":
            manager.show_all_transactions()

        elif choice == "6":
            print("Goodbye 👋")
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    main()