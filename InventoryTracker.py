import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox


class InventoryDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Tracking Dashboard")

        # Database Initialization
        self.conn = sqlite3.connect('inventory.db')
        self.cursor = self.conn.cursor()
        self.setup_database()

        # Widgets
        self.add_inventory_frame()
        self.display_inventory_frame()
        self.load_inventory_from_db()

    def setup_database(self):
        """Initialize the database and tables."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS inventory
                               (item_name TEXT PRIMARY KEY, quantity INTEGER)''')
        self.conn.commit()

    def add_inventory_frame(self):
        frame = ttk.LabelFrame(self.root, text="Add Inventory", padding=(10, 5))
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Labels
        ttk.Label(frame, text="Item Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Entries
        self.item_name = tk.StringVar()
        self.item_qty = tk.StringVar()
        ttk.Entry(frame, textvariable=self.item_name).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Entry(frame, textvariable=self.item_qty).grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Add Button
        ttk.Button(frame, text="Add", command=self.add_to_inventory).grid(row=2, column=0, columnspan=2, pady=10)

    def display_inventory_frame(self):
        frame = ttk.LabelFrame(self.root, text="Current Inventory", padding=(10, 5))
        frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Listbox to display inventory items
        self.listbox = tk.Listbox(frame)
        self.listbox.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        # Delete Button to remove items
        ttk.Button(frame, text="Delete", command=self.delete_from_inventory).grid(row=1, column=0, pady=10)

        # Clear All Button to remove all items
        ttk.Button(frame, text="Clear All", command=self.clear_all_inventory).grid(row=2, column=0, pady=10)

    def add_to_inventory(self):
        item = self.item_name.get()
        qty = int(self.item_qty.get())

        if item and qty:
            self.cursor.execute("INSERT OR REPLACE INTO inventory (item_name, quantity) VALUES (?, ?)", (item, qty))
            self.conn.commit()
            self.load_inventory_from_db()

        self.item_name.set("")
        self.item_qty.set("")

    def load_inventory_from_db(self):
        self.listbox.delete(0, tk.END)
        for row in self.cursor.execute("SELECT item_name, quantity FROM inventory"):
            item, qty = row
            self.listbox.insert(tk.END, f"{item}: {qty}")

    def delete_from_inventory(self):
        selected_item = self.listbox.get(tk.ACTIVE)
        if selected_item:  # Check if an item is selected
            item_name = selected_item.split(":")[0].strip()  # Extract the item name from the listbox entry

            # Delete the item from the SQLite database
            self.cursor.execute("DELETE FROM inventory WHERE item_name=?", (item_name,))
            self.conn.commit()

            # Reload the listbox to reflect the changes
            self.load_inventory_from_db()

    def clear_all_inventory(self):
        # Ask the user for confirmation before deleting all items
        answer = tk.messagebox.askyesno("Confirmation", "Are you sure you want to delete all items from the inventory?")
        if answer:
            # Delete all items from the SQLite database
            self.cursor.execute("DELETE FROM inventory")
            self.conn.commit()

            # Clear the listbox
            self.listbox.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryDashboard(root)
    root.mainloop()
