import os
import json
import csv
import pandas as pd
from datetime import datetime, timedelta
from getpass import getpass
import shutil

class BudgetTracker:
    def __init__(self, username):
        self.username = username
        self.transactions = []
        self.categories = ['Food', 'Rent', 'Entertainment', 'Utilities', 'Transportation', 'Miscellaneous']
        self.file_name = f'{self.username}_transactions.json'
        self.load_transactions()
        self.recurring_transactions = []  # List to store recurring transactions

    def load_transactions(self):
        """Load transaction data from the file if it exists."""
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, 'r') as file:
                    data = json.load(file)
                    self.transactions = [Transaction(**item) for item in data]
            except json.JSONDecodeError:
                print("Error loading transaction data. The file may be corrupted.")
        else:
            print(f"No previous transaction data found for user {self.username}. Starting fresh.")

    def save_transactions(self):
        """Save transaction data to a file."""
        try:
            with open(self.file_name, 'w') as file:
                json.dump([transaction.to_dict() for transaction in self.transactions], file)
        except IOError:
            print("Error saving transactions to file.")

    def add_transaction(self, amount, category, description, date=None):
        """Add a transaction to the tracker."""
        if category not in self.categories:
            print("Invalid category. Please choose from the following: ", self.categories)
            return
        if not date:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction = Transaction(amount, category, description, date)
        self.transactions.append(transaction)
        print(f"Transaction added: {transaction}")
        self.save_transactions()

    def add_recurring_transaction(self, amount, category, description, interval_days, start_date=None):
        """Add a recurring transaction to the tracker."""
        if category not in self.categories:
            print("Invalid category. Please choose from the following: ", self.categories)
            return
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        recurring_transaction = RecurringTransaction(amount, category, description, start_date, interval_days)
        self.recurring_transactions.append(recurring_transaction)
        print(f"Recurring transaction added: {recurring_transaction}")

    def generate_summary(self):
        """Generate a summary of transactions by category."""
        print("\nSummary of Transactions by Category:")
        summary = {category: 0 for category in self.categories}
        for transaction in self.transactions:
            summary[transaction.category] += transaction.amount
        
        for category, total in summary.items():
            print(f"{category}: {total}")
        
        # Call the graphing function here
        self.plot_spending_by_category(summary)

    def plot_spending_by_category(self, summary):
        """Plot spending distribution by category using a pie chart."""
        import matplotlib.pyplot as plt
        categories = list(summary.keys())
        totals = list(summary.values())
        plt.figure(figsize=(8, 8))
        plt.pie(totals, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title("Spending by Category")
        plt.show()

    def process_recurring_transactions(self):
        """Automatically add recurring transactions to the tracker."""
        today = datetime.now()
        for recurring in self.recurring_transactions:
            last_added_date = datetime.strptime(recurring.last_added, "%Y-%m-%d %H:%M:%S")
            if today - last_added_date >= timedelta(days=recurring.interval_days):
                self.add_transaction(recurring.amount, recurring.category, recurring.description)
                recurring.last_added = today.strftime("%Y-%m-%d %H:%M:%S")
                self.save_transactions()

    def view_expenses_vs_income(self):
        """View income vs expenses."""
        income = sum(t.amount for t in self.transactions if t.amount > 0)
        expenses = sum(t.amount for t in self.transactions if t.amount < 0)
        print(f"Income: {income}\nExpenses: {expenses}")
        print(f"Net Balance: {income + expenses}")

    def generate_report(self, start_date, end_date):
        """Generate a report for a specific time period."""
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        filtered_transactions = [
            t for t in self.transactions if start_date <= datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S") <= end_date
        ]
        
        print(f"\nTransactions from {start_date.date()} to {end_date.date()}:")
        for transaction in filtered_transactions:
            print(transaction)
        
        total = sum(t.amount for t in filtered_transactions)
        print(f"\nTotal for this period: {total}")
        
        return filtered_transactions

    def export_to_csv(self, transactions):
        """Export transactions to a CSV file."""
        csv_file = f'{self.username}_transactions.csv'
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Description', 'Amount'])
            for transaction in transactions:
                writer.writerow([transaction.date, transaction.category, transaction.description, transaction.amount])
        print(f"Transactions exported to {csv_file}")

    def export_to_excel(self, transactions):
        """Export transactions to an Excel file."""
        df = pd.DataFrame([t.to_dict() for t in transactions])
        excel_file = f'{self.username}_transactions.xlsx'
        df.to_excel(excel_file, index=False)
        print(f"Transactions exported to {excel_file}")

    def backup_data(self):
        """Backup transaction data to a separate file."""
        backup_file = f'{self.username}_backup.json'
        shutil.copy(self.file_name, backup_file)
        print(f"Backup completed: {backup_file}")

    def restore_data(self):
        """Restore transaction data from a backup file."""
        backup_file = f'{self.username}_backup.json'
        if os.path.exists(backup_file):
            shutil.copy(backup_file, self.file_name)
            print(f"Data restored from backup.")
            self.load_transactions()
        else:
            print("Backup file not found.")


class Transaction:
    def __init__(self, amount, category, description, date):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    def __str__(self):
        return f"{self.date} | {self.category} | {self.description} | {'+' if self.amount > 0 else ''}{self.amount}"

    def to_dict(self):
        """Convert transaction to dictionary for saving."""
        return {
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'date': self.date
        }


class RecurringTransaction:
    def __init__(self, amount, category, description, start_date, interval_days):
        self.amount = amount
        self.category = category
        self.description = description
        self.start_date = start_date
        self.interval_days = interval_days
        self.last_added = start_date

    def __str__(self):
        return f"{self.description} | {self.amount} | every {self.interval_days} days"

    def to_dict(self):
        """Convert recurring transaction to dictionary for saving."""
        return {
            'amount': self.amount,
            'category': self.category,
            'description': self.description,
            'start_date': self.start_date,
            'interval_days': self.interval_days,
            'last_added': self.last_added
        }


def display_menu():
    """Display the main menu options."""
    print("\n-- Budget Tracker --")
    print("1. Add Transaction")
    print("2. Add Recurring Transaction")
    print("3. View Summary")
    print("4. View Expenses vs Income")
    print("5. Generate Report (Custom Time Period)")
    print("6. Export to CSV")
    print("7. Export to Excel")
    print("8. Backup Data")
    print("9. Restore Data from Backup")
    print("10. Exit")


def get_user_input():
    """Prompt for user input to choose an option."""
    try:
        choice = int(input("Choose an option: "))
        return choice
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


def handle_add_transaction(budget_tracker):
    """Handle adding a transaction."""
    try:
        amount = float(input("Enter amount (positive for income, negative for expense): "))
        category = input(f"Enter category ({', '.join(budget_tracker.categories)}): ")
        description = input("Enter description: ")
        budget_tracker.add_transaction(amount, category, description)
    except ValueError:
        print("Invalid input for amount. Please enter a valid number.")


def handle_add_recurring_transaction(budget_tracker):
    """Handle adding a recurring transaction."""
    try:
        amount = float(input("Enter amount (positive for income, negative for expense): "))
        category = input(f"Enter category ({', '.join(budget_tracker.categories)}): ")
        description = input("Enter description: ")
        interval_days = int(input("Enter the interval in days for recurrence: "))
        budget_tracker.add_recurring_transaction(amount, category, description, interval_days)
    except ValueError:
        print("Invalid input. Please enter a valid number.")


def handle_generate_report(budget_tracker):
    """Handle report generation for a custom time period."""
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    budget_tracker.generate_report(start_date, end_date)


def handle_export_to_csv(budget_tracker):
    """Handle exporting transactions to CSV."""
    budget_tracker.export_to_csv(budget_tracker.transactions)


def handle_export_to_excel(budget_tracker):
    """Handle exporting transactions to Excel."""
    budget_tracker.export_to_excel(budget_tracker.transactions)


def main():
    """Main function to run the Budget Tracker."""
    print("Welcome to Budget Tracker!")

    # User Authentication (simplified)
    username = input("Enter your username: ")
    budget_tracker = BudgetTracker(username)

    while True:
        display_menu()
        choice = get_user_input()

        if choice == 1:
            handle_add_transaction(budget_tracker)
        elif choice == 2:
            handle_add_recurring_transaction(budget_tracker)
        elif choice == 3:
            budget_tracker.generate_summary()
        elif choice == 4:
            budget_tracker.view_expenses_vs_income()
        elif choice == 5:
            handle_generate_report(budget_tracker)
        elif choice == 6:
            handle_export_to_csv(budget_tracker)
        elif choice == 7:
            handle_export_to_excel(budget_tracker)
        elif choice == 8:
            budget_tracker.backup_data()
        elif choice == 9:
            budget_tracker.restore_data()
        elif choice == 10:
            print("Exiting the Budget Tracker.")
            break
        else:
            print("Invalid option, please choose again.")


if __name__ == "__main__":
    main()
