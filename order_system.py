import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

class OrderItem:
    def __init__(self, product, qty, discount):
        self.product = product
        self.qty = qty
        self.discount = discount
        self.subtotal = self.calculate_subtotal()
    
    def calculate_subtotal(self):
        return self.qty * self.product.price * (1 - self.discount/100)

class OrderProcessingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Order Processing System")
        self.root.geometry("1000x600")
        
        # Initialize database
        self.init_database()
        
        # Load products
        self.products = self.load_products()
        
        # Initialize order items
        self.order_items = []
        
        self.create_widgets()
        
    def init_database(self):
        conn = sqlite3.connect('order_system.db')
        c = conn.cursor()
        
        # Create products table
        c.execute('''CREATE TABLE IF NOT EXISTS products
                    (id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     price REAL NOT NULL)''')
        
        # Insert sample products if none exist
        c.execute("SELECT COUNT(*) FROM products")
        if c.fetchone()[0] == 0:
            sample_products = [
                (1, "BATTERY", 50000),
                (2, "CHARGER", 100000),
            ]
            c.executemany("INSERT INTO products VALUES (?,?,?)", sample_products)
        
        conn.commit()
        conn.close()
    
    def load_products(self):
        conn = sqlite3.connect('order_system.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        products = {row[0]: Product(row[0], row[1], row[2]) for row in c.fetchall()}
        conn.close()
        return products
    
    def create_widgets(self):
        # Order Header Frame
        header_frame = ttk.LabelFrame(self.root, text="Order Information", padding=10)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        # Order Number
        ttk.Label(header_frame, text="Order Number:").grid(row=0, column=0, padx=5, pady=5)
        self.order_number = ttk.Entry(header_frame)
        self.order_number.grid(row=0, column=1, padx=5, pady=5)
        
        # Customer Reference
        ttk.Label(header_frame, text="Customer Ref:").grid(row=0, column=2, padx=5, pady=5)
        self.customer_ref = ttk.Entry(header_frame)
        self.customer_ref.grid(row=0, column=3, padx=5, pady=5)
        
        # Order Date
        ttk.Label(header_frame, text="Order Date:").grid(row=0, column=4, padx=5, pady=5)
        self.order_date = ttk.Entry(header_frame)
        self.order_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.order_date.grid(row=0, column=5, padx=5, pady=5)
        
        # Items Frame
        items_frame = ttk.LabelFrame(self.root, text="Order Items", padding=10)
        items_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview for order items
        columns = ('product', 'qty', 'price', 'discount', 'subtotal')
        self.tree = ttk.Treeview(items_frame, columns=columns, show='headings')
        
        # Set column headings
        self.tree.heading('product', text='Product')
        self.tree.heading('qty', text='Quantity')
        self.tree.heading('price', text='Price')
        self.tree.heading('discount', text='Discount (%)')
        self.tree.heading('subtotal', text='Subtotal')
        
        # Set column widths
        for col in columns:
            self.tree.column(col, width=150)
        
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add Item Frame
        add_item_frame = ttk.Frame(items_frame)
        add_item_frame.pack(fill="x", padx=5, pady=5)
        
        # Product dropdown
        ttk.Label(add_item_frame, text="Product:").grid(row=0, column=0, padx=5, pady=5)
        self.product_var = tk.StringVar()
        product_names = [p.name for p in self.products.values()]
        self.product_dropdown = ttk.Combobox(add_item_frame, textvariable=self.product_var, values=product_names)
        self.product_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        # Quantity entry
        ttk.Label(add_item_frame, text="Quantity:").grid(row=0, column=2, padx=5, pady=5)
        self.qty_var = tk.StringVar(value="1")
        self.qty_entry = ttk.Entry(add_item_frame, textvariable=self.qty_var, width=10)
        self.qty_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Discount entry
        ttk.Label(add_item_frame, text="Discount (%):").grid(row=0, column=4, padx=5, pady=5)
        self.discount_var = tk.StringVar(value="0")
        self.discount_entry = ttk.Entry(add_item_frame, textvariable=self.discount_var, width=10)
        self.discount_entry.grid(row=0, column=5, padx=5, pady=5)
        
        # Add button
        self.add_button = ttk.Button(add_item_frame, text="Add Item", command=self.add_item)
        self.add_button.grid(row=0, column=6, padx=5, pady=5)
        
        # Remove button
        self.remove_button = ttk.Button(add_item_frame, text="Remove Selected", command=self.remove_item)
        self.remove_button.grid(row=0, column=7, padx=5, pady=5)
        
        # Total Frame
        total_frame = ttk.Frame(self.root)
        total_frame.pack(fill="x", padx=10, pady=5)
        
        self.total_label = ttk.Label(total_frame, text="Total: 0.00", font=('Arial', 12, 'bold'))
        self.total_label.pack(side="right", padx=10)
    
    def add_item(self):
        try:
            product_name = self.product_var.get()
            qty = int(self.qty_var.get())
            discount = float(self.discount_var.get())
            
            if not product_name:
                messagebox.showerror("Error", "Please select a product")
                return
            
            if qty <= 0:
                messagebox.showerror("Error", "Quantity must be greater than 0")
                return
            
            if discount < 0 or discount > 100:
                messagebox.showerror("Error", "Discount must be between 0 and 100")
                return
            
            # Find product by name
            product = next((p for p in self.products.values() if p.name == product_name), None)
            
            # Create order item
            order_item = OrderItem(product, qty, discount)
            self.order_items.append(order_item)
            
            # Add to treeview
            self.tree.insert('', 'end', values=(
                product.name,
                qty,
                f"{product.price:.2f}",
                f"{discount:.2f}",
                f"{order_item.subtotal:.2f}"
            ))
            
            # Update total
            self.update_total()
            
            # Clear entries
            self.product_var.set('')
            self.qty_var.set('1')
            self.discount_var.set('0')
            
        except ValueError as e:
            messagebox.showerror("Error", "Please enter valid numbers for quantity and discount")
    
    def remove_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
        
        # Remove from treeview
        for item in selected_item:
            item_idx = self.tree.index(item)
            self.tree.delete(item)
            # Remove from order_items list
            if 0 <= item_idx < len(self.order_items):
                self.order_items.pop(item_idx)
        
        # Update total
        self.update_total()
    
    def update_total(self):
        total = sum(item.subtotal for item in self.order_items)
        self.total_label.config(text=f"Total: {total:,.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderProcessingSystem(root)
    root.mainloop()