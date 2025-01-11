import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkinter import ttk
from backend import BudgetTracker
from PIL import Image, ImageTk
import datetime
import tkinter.simpledialog as simpledialog

# Hardcoded users for the demo (username: password)
USER_CREDENTIALS = {
    "root": "root",
    "user1": "user1"
}

class BudgetApp:
    def __init__(self, root, username):
        self.username = username
        self.budget_tracker = BudgetTracker(self.username)

        # Setup the main window
        self.root = root
        self.root.title(f"{self.username}'s Budget Tracker")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.input_frame = ctk.CTkFrame(self.root)
        self.input_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        #Input Fields
        self.amount_label = self.create_label("Amount:")
        self.amount_entry = self.create_entry()

        self.category_label = self.create_label("Category:")
        self.category_combobox = self.create_combobox(self.budget_tracker.categories)

        self.description_label = self.create_label("Description:")
        self.description_entry = self.create_entry()

        self.date_label = self.create_label("Date:")
        self.date_entry = ctk.CTkEntry(self.input_frame, font=("Arial", 12), width=250)
        self.date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

        #layout
        self.amount_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        self.category_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.category_combobox.grid(row=1, column=1, padx=10, pady=10)

        self.description_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.description_entry.grid(row=2, column=1, padx=10, pady=10)

        self.date_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)
        self.date_entry.grid(row=3, column=1, padx=10, pady=10)

        #buttons
        self.add_button = self.create_button("Add Transaction", self.add_transaction)
        self.view_button = self.create_button("View Summary", self.view_summary)
        self.graph_button = self.create_button("Generate Graph", self.generate_graph)
        self.export_button = self.create_button("Export Data", self.export_data)
        self.reset_button = self.create_button("Reset Fields", self.reset_fields)
        self.logout_button = self.create_button("Logout", self.logout)
        self.view_transactions_button = self.create_button("View Transactions", self.view_transactions)

        self.add_button.grid(row=4, column=0, columnspan=2, pady=20)
        self.view_button.grid(row=5, column=0, columnspan=2, pady=20)
        self.graph_button.grid(row=6, column=0, columnspan=2, pady=20)
        self.export_button.grid(row=7, column=0, columnspan=2, pady=20)
        self.reset_button.grid(row=8, column=0, columnspan=2, pady=20)
        self.view_transactions_button.grid(row=9, column=0, columnspan=2, pady=20)
        self.logout_button.grid(row=10, column=0, columnspan=2, pady=20)

        # Add placeholder for pie chart display
        self.chart_label = ctk.CTkLabel(self.root, text="", width=200, height=200)
        self.chart_label.grid(row=11, column=0, columnspan=2, pady=20)

    def create_label(self, text):
        return ctk.CTkLabel(self.input_frame, text=text, font=("Arial", 12, "bold"))

    def create_entry(self):
        entry = ctk.CTkEntry(self.input_frame, font=("Arial", 12), width=250)
        return entry

    def create_combobox(self, values):
        combobox = ctk.CTkComboBox(self.input_frame, values=values, font=("Arial", 12), width=250)
        combobox.set(values[0])  # Set the default value
        return combobox

    def create_button(self, text, command):
        return ctk.CTkButton(self.root, text=text, command=command, font=("Arial", 12, "bold"), width=20, height=2, fg_color="#4CAF50", hover_color="#902bf5")

    def add_transaction(self):
        #add the transaction
        try:
            amount = self.amount_entry.get()
            amount = float(amount)

            category = self.category_combobox.get()
            description = self.description_entry.get()
            date = self.date_entry.get()

            #all fields are filled
            if not amount or not category or not description or not date:
                messagebox.showerror("Error", "Please fill in all fields.")
                return

            self.budget_tracker.add_transaction(amount, category, description, date)
            messagebox.showinfo("Success", "Transaction added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")

    def view_summary(self):
        #summary of transactions
        summary = self.budget_tracker.generate_summary()
        summary_str = "\n".join([f"{category}: ${total:.2f}" for category, total in summary.items()])
        messagebox.showinfo("Summary", summary_str)

    def generate_graph(self):
        #cook up the pie
        chart_file = self.budget_tracker.plot_summary()
        self.display_graph(chart_file)

    def display_graph(self, chart_file):
        #pie chart tasty image
        img = Image.open(chart_file)
        img = img.resize((400, 400), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        
        self.chart_label.config(image=img)
        self.chart_label.image = img

    def export_data(self):
        self.export_window = ctk.CTkToplevel(self.root)
        self.export_window.title("Export Data")
        self.export_window.geometry("400x300")
        self.export_window.configure(bg="#f0f0f0")

        #label for file type input
        self.label = ctk.CTkLabel(self.export_window, text="Enter file type (CSV/Excel):", font=("Arial", 12))
        self.label.pack(pady=20)

        #entry field
        self.file_type_entry = ctk.CTkEntry(self.export_window, font=("Arial", 12), width=250)
        self.file_type_entry.pack(pady=10)

        #confirm button
        self.export_button = ctk.CTkButton(self.export_window, text="Export", command=self.confirm_export, font=("Arial", 12, "bold"), width=20, height=2, fg_color="#4CAF50", hover_color="#45a049")
        self.export_button.pack(pady=20)

        #cancel button
        self.cancel_button = ctk.CTkButton(self.export_window, text="Cancel", command=self.export_window.destroy, font=("Arial", 12, "bold"), width=20, height=2, fg_color="#FF6347", hover_color="#FF4500")
        self.cancel_button.pack(pady=10)

    def confirm_export(self):
        #confirming the export file type
        file_type = self.file_type_entry.get().lower()

        if file_type == "csv":
            filename = self.budget_tracker.export_to_csv(self.budget_tracker.transactions)
            messagebox.showinfo("Export Successful", f"Data exported to {filename}")
        elif file_type == "excel":
            filename = self.budget_tracker.export_to_excel(self.budget_tracker.transactions)
            messagebox.showinfo("Export Successful", f"Data exported to {filename}")
        else:
            messagebox.showerror("Invalid Option", "Please choose either 'CSV' or 'Excel'.")

        self.export_window.destroy()

    def reset_fields(self):
        #Clear input fields
        self.amount_entry.delete(0, ctk.END)
        self.category_combobox.set(self.budget_tracker.categories[0])
        self.description_entry.delete(0, ctk.END)
        self.date_entry.delete(0, ctk.END)
        self.date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

    def logout(self):
        #self explanitory
        self.root.destroy()
        self.open_login_screen()

    def view_transactions(self):
        #display all transactions
        transactions = self.budget_tracker.get_all_transactions()
        if not transactions:
            messagebox.showinfo("No Transactions", "No transactions available.")
            return
        transactions_str = "\n".join([f"Amount: {t['amount']} | {t['category']} | {t['date']} | {t['description']}" for t in transactions])
        messagebox.showinfo("Transactions", transactions_str)

    def open_login_screen(self):
        #open login screen
        login_root = ctk.CTk()
        login_screen = LoginScreen(login_root)
        login_root.mainloop()


class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Budget Tracker")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        self.create_widgets()

    def create_widgets(self):
        #Create login screen stuff
        self.label_username = ctk.CTkLabel(self.root, text="Username:", font=("Arial", 12))
        self.label_password = ctk.CTkLabel(self.root, text="Password:", font=("Arial", 12))

        self.entry_username = ctk.CTkEntry(self.root, font=("Arial", 12), width=250)
        self.entry_password = ctk.CTkEntry(self.root, font=("Arial", 12), width=250, show="*")

        self.button_login = ctk.CTkButton(self.root, text="Login", command=self.login, font=("Arial", 12, "bold"), width=20, height=2, fg_color="#4CAF50", hover_color="#45a049")

        self.label_username.grid(row=0, column=0, padx=10, pady=10)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)

        self.label_password.grid(row=1, column=0, padx=10, pady=10)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        self.button_login.grid(row=2, column=0, columnspan=2, pady=20)

    def login(self):
        #validate login credentials
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            self.root.destroy()
            self.open_budget_tracker(username)
        else:
            messagebox.showerror("Error", "Invalid username or password. Please try again.")

    def open_budget_tracker(self, username):
        #Opens the main window
        root = ctk.CTk()
        app = BudgetApp(root, username)
        root.mainloop()


if __name__ == "__main__":
    # Create login window
    root = ctk.CTk()
    login_screen = LoginScreen(root)
    root.mainloop()
