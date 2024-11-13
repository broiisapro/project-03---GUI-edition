# main.py
import tkinter as tk
from tkinter import messagebox, filedialog
from backend import BudgetTracker
from PIL import Image, ImageTk

class BudgetApp:
    def __init__(self, root, username):
        self.username = username
        self.budget_tracker = BudgetTracker(self.username)

        # Setup the main window
        self.root = root
        self.root.title("Budget Tracker")
        self.root.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Labels and Inputs
        self.amount_label = tk.Label(self.root, text="Amount:")
        self.amount_label.grid(row=0, column=0, padx=10, pady=10)
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.grid(row=1, column=0, padx=10, pady=10)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=1, column=1, padx=10, pady=10)

        self.description_label = tk.Label(self.root, text="Description:")
        self.description_label.grid(row=2, column=0, padx=10, pady=10)
        self.description_entry = tk.Entry(self.root)
        self.description_entry.grid(row=2, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.root, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.view_button = tk.Button(self.root, text="View Summary", command=self.view_summary)
        self.view_button.grid(row=4, column=0, columnspan=2, pady=20)

        self.graph_button = tk.Button(self.root, text="Generate Summary Graph", command=self.generate_graph)
        self.graph_button.grid(row=5, column=0, columnspan=2, pady=20)

        self.export_button = tk.Button(self.root, text="Export Data (CSV/Excel)", command=self.export_data)
        self.export_button.grid(row=6, column=0, columnspan=2, pady=20)

    def add_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            description = self.description_entry.get()
            self.budget_tracker.add_transaction(amount, category, description)
            messagebox.showinfo("Success", "Transaction added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid amount.")

    def view_summary(self):
        summary = self.budget_tracker.generate_summary()
        summary_str = "\n".join([f"{category}: {total}" for category, total in summary.items()])
        messagebox.showinfo("Summary", summary_str)

    def generate_graph(self):
        chart_file = self.budget_tracker.plot_summary()
        self.display_graph(chart_file)

    def display_graph(self, chart_file):
        """Display the generated pie chart in the GUI"""
        img = Image.open(chart_file)
        img = img.resize((400, 400), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        
        chart_label = tk.Label(self.root, image=img)
        chart_label.image = img
        chart_label.grid(row=7, column=0, columnspan=2, pady=20)

    def export_data(self):
        file_type = filedialog.askstring("Export Type", "Enter file type (CSV/Excel):").lower()
        if file_type == "csv":
            filename = self.budget_tracker.export_to_csv(self.budget_tracker.transactions)
            messagebox.showinfo("Export Successful", f"Data exported to {filename}")
        elif file_type == "excel":
            filename = self.budget_tracker.export_to_excel(self.budget_tracker.transactions)
            messagebox.showinfo("Export Successful", f"Data exported to {filename}")
        else:
            messagebox.showerror("Invalid Option", "Please choose either 'CSV' or 'Excel'.")

if __name__ == "__main__":
    # Create Tkinter window and launch app for a specific user
    root = tk.Tk()
    username = "john_doe"  # You can change this or add a login system later
    app = BudgetApp(root, username)
    root.mainloop()
