import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from backend import BudgetTracker
from PIL import Image, ImageTk

# Hardcoded users for the demo (username: password)
USER_CREDENTIALS = {
    "root": "root",  # Example username: password
    "user1": "user1"   # Another user for demo purposes
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

        self.create_widgets()

    def create_widgets(self):
        # Frame for input fields and buttons
        self.input_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.input_frame.grid(row=0, column=0, padx=20, pady=20)

        # Labels and Inputs with better styling
        self.amount_label = self.create_label("Amount:")
        self.amount_entry = self.create_entry()

        self.category_label = self.create_label("Category:")
        self.category_combobox = self.create_combobox(self.budget_tracker.categories)

        self.description_label = self.create_label("Description:")
        self.description_entry = self.create_entry()

        # Layout the entries and labels
        self.amount_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=10)

        self.category_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.category_combobox.grid(row=1, column=1, padx=10, pady=10)

        self.description_label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        self.description_entry.grid(row=2, column=1, padx=10, pady=10)

        # Buttons with improved layout and style
        self.add_button = self.create_button("Add Transaction", self.add_transaction)
        self.view_button = self.create_button("View Summary", self.view_summary)
        self.graph_button = self.create_button("Generate Graph", self.generate_graph)
        self.export_button = self.create_button("Export Data", self.export_data)

        # Button grid arrangement
        self.add_button.grid(row=3, column=0, columnspan=2, pady=20)
        self.view_button.grid(row=4, column=0, columnspan=2, pady=20)
        self.graph_button.grid(row=5, column=0, columnspan=2, pady=20)
        self.export_button.grid(row=6, column=0, columnspan=2, pady=20)

        # Add placeholder for pie chart display
        self.chart_label = tk.Label(self.root, bg="#f0f0f0")
        self.chart_label.grid(row=7, column=0, columnspan=2, pady=20)

    def create_label(self, text):
        """Helper function to create a label with consistent styling."""
        return tk.Label(self.input_frame, text=text, font=("Arial", 12, "bold"), bg="#f0f0f0")

    def create_entry(self):
        """Helper function to create an entry field with consistent styling."""
        entry = tk.Entry(self.input_frame, font=("Arial", 12), bd=2, relief="solid", width=30)
        entry.config(highlightbackground="#D3D3D3", highlightcolor="#a3a3a3")
        return entry

    def create_combobox(self, values):
        """Helper function to create a combobox (dropdown) with predefined values."""
        combobox = ttk.Combobox(self.input_frame, values=values, font=("Arial", 12), state="readonly", width=28)
        combobox.set(values[0])  # Set the default value to the first category
        return combobox

    def create_button(self, text, command):
        """Helper function to create a styled button."""
        return tk.Button(self.root, text=text, command=command, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                         relief="solid", height=2, width=20)

    def add_transaction(self):
        """Adds a new transaction."""
        try:
            amount = float(self.amount_entry.get())
            category = self.category_combobox.get()  # Get the selected category from the combobox
            description = self.description_entry.get()
            self.budget_tracker.add_transaction(amount, category, description)
            messagebox.showinfo("Success", "Transaction added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid amount.")

    def view_summary(self):
        """View the summary of transactions."""
        summary = self.budget_tracker.generate_summary()
        summary_str = "\n".join([f"{category}: ${total:.2f}" for category, total in summary.items()])
        messagebox.showinfo("Summary", summary_str)

    def generate_graph(self):
        """Generates and displays the pie chart."""
        chart_file = self.budget_tracker.plot_summary()
        self.display_graph(chart_file)

    def display_graph(self, chart_file):
        """Displays the generated pie chart in the GUI."""
        img = Image.open(chart_file)
        img = img.resize((400, 400), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        
        self.chart_label.config(image=img)
        self.chart_label.image = img  # Keep a reference to avoid garbage collection

    def export_data(self):
        """Exports data to CSV or Excel."""
        file_type = filedialog.askstring("Export Type", "Enter file type (CSV/Excel):").lower()
        if file_type == "csv":
            filename = self.budget_tracker.export_to_csv(self.budget_tracker.transactions)
            messagebox.showinfo("Export Successful", f"Data exported to {filename}")
        elif file_type == "excel":
            filename = self.budget_tracker.export_to_excel(self.budget_tracker.transactions)
            messagebox.showinfo("Export Successful", f"Data exported to {filename}")
        else:
            messagebox.showerror("Invalid Option", "Please choose either 'CSV' or 'Excel'.")

# Login screen
class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Budget Tracker")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        self.create_widgets()

    def create_widgets(self):
        """Create widgets for the login screen."""
        self.label_username = tk.Label(self.root, text="Username:", font=("Arial", 12), bg="#f0f0f0")
        self.label_password = tk.Label(self.root, text="Password:", font=("Arial", 12), bg="#f0f0f0")

        self.entry_username = tk.Entry(self.root, font=("Arial", 12), bd=2, relief="solid", width=30)
        self.entry_password = tk.Entry(self.root, font=("Arial", 12), bd=2, relief="solid", width=30, show="*")

        self.button_login = tk.Button(self.root, text="Login", command=self.login, bg="#4CAF50", fg="white",
                                      font=("Arial", 12, "bold"), relief="solid", height=2, width=20)

        self.label_username.grid(row=0, column=0, padx=10, pady=10)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)

        self.label_password.grid(row=1, column=0, padx=10, pady=10)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        self.button_login.grid(row=2, column=0, columnspan=2, pady=20)

    def login(self):
        """Validate the login credentials."""
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            self.root.destroy()  # Close the login window
            self.open_budget_tracker(username)
        else:
            messagebox.showerror("Error", "Invalid username or password. Please try again.")

    def open_budget_tracker(self, username):
        """Open the main Budget Tracker window."""
        root = tk.Tk()
        app = BudgetApp(root, username)
        root.mainloop()


if __name__ == "__main__":
    # Create login window
    root = tk.Tk()
    login_screen = LoginScreen(root)
    root.mainloop()
