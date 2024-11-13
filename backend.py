import os
import json
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

class BudgetTracker:
    def __init__(self, username):
        self.username = username
        self.transactions = []
        self.categories = ['Food', 'Rent', 'Entertainment', 'Utilities', 'Transportation', 'Miscellaneous']
        self.file_name = f'{self.username}_transactions.json'
        self.load_transactions()

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
        self.save_transactions()

    def generate_summary(self):
        """Generate a summary of transactions by category."""
        summary = {category: 0 for category in self.categories}
        for transaction in self.transactions:
            summary[transaction.category] += transaction.amount
        return summary

    def generate_report(self, start_date, end_date):
        """Generate a report for a specific time period."""
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        filtered_transactions = [
            t for t in self.transactions if start_date <= datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S") <= end_date
        ]
        total = sum(t.amount for t in filtered_transactions)
        return filtered_transactions, total

    def export_to_csv(self, transactions):
        """Export transactions to a CSV file."""
        csv_file = f'{self.username}_transactions.csv'
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Description', 'Amount'])  # Write header
            for transaction in transactions:
                # Convert each transaction to a dictionary and extract the relevant values
                writer.writerow([transaction.date, transaction.category, transaction.description, transaction.amount])
        return csv_file

    def export_to_excel(self, transactions):
        """Export transactions to an Excel file."""
        # Convert the transactions to a list of dictionaries (or use the Transaction's `to_dict()` method)
        data = [transaction.to_dict() for transaction in transactions]
        
        # Create a DataFrame from the data
        df = pd.DataFrame(data)
        
        # Define the Excel file name
        excel_file = f'{self.username}_transactions.xlsx'
        
        # Export the DataFrame to an Excel file
        df.to_excel(excel_file, index=False)
        return excel_file

    def plot_summary(self):
        """Generate a pie chart for the summary."""
        summary = self.generate_summary()
        categories = list(summary.keys())
        amounts = list(summary.values())

        fig, ax = plt.subplots()
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

        chart_file = f'charts/{self.username}_summary.png'
        plt.savefig(chart_file)
        plt.close()

        return chart_file


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
