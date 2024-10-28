import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class ProductManagement:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Product Management")
        self.window.geometry("600x400")
        
        # Create frames
        self.create_widgets()
        self.load_products()
        
    def create_widgets(self):
        # Product List Frame
        list_frame = ttk.LabelFrame(self.window, text="Product List", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview for products
        columns = ('id', 'name', 'price')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Set column headings
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Product Name')
        self.tree.heading('price', text='Price')
        
        # Set column widths
        self.tree.column('id', width=50)
        self.tree.column('name', width=200)
        self.tree.column('price', width=100)
        
        self.tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Add Product Frame
        add_frame = ttk.LabelFrame(self.window, text="Add New Product", padding=10)
        add_frame.pack(fill="x", padx=10, pady=5)
        
        # Product Name
        ttk.Label(add_frame, text="Product Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(add_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Product Price
        ttk.Label(add_frame, text="Price:").grid(row=0, column=2, padx=5, pady=5)
        self.price_var = tk.StringVar()
        self.price_entry = ttk.Entry(add_frame, textvariable=self.price_var)
        self.price_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Add Button
        self.add_button = ttk.Button(add_frame, text="Add Product", command=self.add_product)
        self.add_button.grid(row=0, column=4, padx=5, pady=5)
        
        # Refresh Button
        self.refresh_button = ttk.Button(add_frame, text="Refresh List", command=self.load_products)
        self.refresh_button.grid(row=0, column=5, padx=5, pady=5)
    
    def load_products(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load products from database
        conn = sqlite3.connect('order_system.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        for row in c.fetchall():
            self.tree.insert('', 'end', values=row)
        conn.close()
    
    def add_product(self):
        try:
            name = self.name_var.get()
            price = float(self.price_var.get())
            
            if not name:
                messagebox.showerror("Error", "Product name is required")
                return
            
            if price <= 0:
                messagebox.showerror("Error", "Price must be greater than 0")
                return
            
            # Add to database
            conn = sqlite3.connect('order_system.db')
            c = conn.cursor()
            c.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
            conn.commit()
            conn.close()
            
            # Clear entries
            self.name_var.set('')
            self.price_var.set('')
            
            # Refresh product list
            self.load_products()
            messagebox.showinfo("Success", "Product added successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid price")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))


class ViewOrders:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("View Orders")
        self.window.geometry("800x600")
        
        self.create_widgets()
        self.load_orders()
        
    def create_widgets(self):
        # Orders List Frame
        list_frame = ttk.LabelFrame(self.window, text="Orders List", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview for orders
        columns = ('order_number', 'customer_ref', 'order_date', 'total_amount')
        self.orders_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Set column headings
        self.orders_tree.heading('order_number', text='Order Number')
        self.orders_tree.heading('customer_ref', text='Customer Ref')
        self.orders_tree.heading('order_date', text='Order Date')
        self.orders_tree.heading('total_amount', text='Total Amount')
        
        # Set column widths
        self.orders_tree.column('order_number', width=150)
        self.orders_tree.column('customer_ref', width=150)
        self.orders_tree.column('order_date', width=100)
        self.orders_tree.column('total_amount', width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.orders_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        # Order Details Frame
        details_frame = ttk.LabelFrame(self.window, text="Order Details", padding=10)
        details_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Treeview for order details
        columns = ('product', 'quantity', 'price', 'discount', 'subtotal')
        self.details_tree = ttk.Treeview(details_frame, columns=columns, show='headings')
        
        # Set column headings
        self.details_tree.heading('product', text='Product')
        self.details_tree.heading('quantity', text='Quantity')
        self.details_tree.heading('price', text='Price')
        self.details_tree.heading('discount', text='Discount (%)')
        self.details_tree.heading('subtotal', text='Subtotal')
        
        # Set column widths
        for col in columns:
            self.details_tree.column(col, width=150)
        
        # Add scrollbar for details
        details_scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=self.details_tree.yview)
        self.details_tree.configure(yscrollcommand=details_scrollbar.set)
        
        # Pack the details treeview and scrollbar
        self.details_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        details_scrollbar.pack(side="right", fill="y", pady=5)
        
        # Bind select event
        self.orders_tree.bind('<<TreeviewSelect>>', self.show_order_details)
        
        # Refresh button
        refresh_button = ttk.Button(self.window, text="Refresh", command=self.load_orders)
        refresh_button.pack(pady=5)
    
    def load_orders(self):
        # Clear existing items
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        try:
            conn = sqlite3.connect('order_system.db')
            c = conn.cursor()
            c.execute("""
                SELECT order_number, customer_ref, order_date, total_amount 
                FROM order_header 
                ORDER BY order_date DESC
            """)
            
            for row in c.fetchall():
                formatted_total = f"{row[3]:,.2f}"
                self.orders_tree.insert('', 'end', values=(row[0], row[1], row[2], formatted_total))
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
    
    def show_order_details(self, event):
        # Clear existing details
        for item in self.details_tree.get_children():
            self.details_tree.delete(item)
        
        # Get selected order
        selected_item = self.orders_tree.selection()
        if not selected_item:
            return
        
        order_number = self.orders_tree.item(selected_item)['values'][0]
        
        try:
            conn = sqlite3.connect('order_system.db')
            c = conn.cursor()
            
            # Updated query to use correct column names
            c.execute("""
                SELECT products.name, od.quantity, od.price, od.discount, od.subtotal
                FROM order_detail od
                JOIN products ON od.product_id = products.id
                JOIN order_header oh ON od.order_id = oh.order_id
                WHERE oh.order_number = ?
            """, (order_number,))
            
            for row in c.fetchall():
                formatted_price = f"{row[2]:,.2f}"
                formatted_subtotal = f"{row[4]:,.2f}"
                self.details_tree.insert('', 'end', values=(
                    row[0],          # Product name
                    row[1],          # Quantity
                    formatted_price, # Price
                    row[3],          # Discount
                    formatted_subtotal # Subtotal
                ))
            
            conn.close()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))

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
        
        # Drop existing tables to ensure clean schema
        c.execute("DROP TABLE IF EXISTS order_detail")
        c.execute("DROP TABLE IF EXISTS order_header")
        c.execute("DROP TABLE IF EXISTS products")
        
        # Create products table with correct column name
        c.execute('''CREATE TABLE IF NOT EXISTS products
                    (id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     price REAL NOT NULL)''')
        
        # Create order_header table
        c.execute('''CREATE TABLE IF NOT EXISTS order_header
                    (order_id INTEGER PRIMARY KEY,
                     order_number TEXT NOT NULL,
                     customer_ref TEXT,
                     order_date DATE,
                     total_amount REAL)''')
        
        # Create order_detail table with correct foreign key reference
        c.execute('''CREATE TABLE IF NOT EXISTS order_detail
                    (detail_id INTEGER PRIMARY KEY,
                     order_id INTEGER,
                     product_id INTEGER,
                     quantity INTEGER,
                     price REAL,
                     discount REAL,
                     subtotal REAL,
                     FOREIGN KEY (order_id) REFERENCES order_header (order_id),
                     FOREIGN KEY (product_id) REFERENCES products (id))''')
        
        # Insert sample products if none exist
        c.execute("SELECT COUNT(*) FROM products")
        if c.fetchone()[0] == 0:
            sample_products = [
                (1, "BATTERY", 50000),
                (2, "CHARGER", 100000),
            ]
            c.executemany("INSERT INTO products (id, name, price) VALUES (?,?,?)", sample_products)
        
        conn.commit()
        conn.close()

    
    def load_products(self):
        conn = sqlite3.connect('order_system.db')
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        products = {row[0]: {"id": row[0], "name": row[1], "price": row[2]} for row in c.fetchall()}
        conn.close()
        return products
    
    def refresh_products(self):
        self.products = self.load_products()
        product_names = [p["name"] for p in self.products.values()]
        self.product_dropdown['values'] = product_names
    
    def create_widgets(self):
        # Menu Bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Product Menu
        product_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Products", menu=product_menu)
        product_menu.add_command(label="Manage Products", command=self.open_product_management)
        product_menu.add_command(label="Refresh Product List", command=self.refresh_products)
        
        # Orders Menu
        orders_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Orders", menu=orders_menu)
        orders_menu.add_command(label="View Orders", command=self.open_view_orders)
        
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
        product_names = [p["name"] for p in self.products.values()]
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
        
        # Buttons Frame
        buttons_frame = ttk.Frame(items_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)
        
        # Add button
        self.add_button = ttk.Button(buttons_frame, text="Add Item", command=self.add_item)
        self.add_button.pack(side="left", padx=5)
        
        # Remove button
        self.remove_button = ttk.Button(buttons_frame, text="Remove Selected", command=self.remove_item)
        self.remove_button.pack(side="left", padx=5)
        
        # Save Order button
        self.save_button = ttk.Button(buttons_frame, text="Save Order", command=self.save_order)
        self.save_button.pack(side="left", padx=5)
        
        # Clear Order button
        self.clear_button = ttk.Button(buttons_frame, text="Clear Order", command=self.clear_order)
        self.clear_button.pack(side="left", padx=5)
        
        # Total Frame
        total_frame = ttk.Frame(self.root)
        total_frame.pack(fill="x", padx=10, pady=5)
        
        self.total_label = ttk.Label(total_frame, text="Total: 0.00", font=('Arial', 12, 'bold'))
        self.total_label.pack(side="right", padx=10)
    
    def open_product_management(self):
        ProductManagement()
        
    def open_view_orders(self):
        ViewOrders()
    
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
            product = next((p for p in self.products.values() if p["name"] == product_name), None)
            
            # Calculate subtotal
            price = product["price"]
            subtotal = qty * price * (1 - discount/100)
            
            # Add to order items
            self.order_items.append({
                "product_id": product["id"],
                "product_name": product["name"],
                "quantity": qty,
                "price": price,
                "discount": discount,
                "subtotal": subtotal
            })
            
            # Add to treeview
            self.tree.insert('', 'end', values=(
                product["name"],
                qty,
                f"{price:,.2f}",
                f"{discount:.2f}",
                f"{subtotal:,.2f}"
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
        
        # Remove from treeview and order_items
        for item in selected_item:
            item_idx = self.tree.index(item)
            self.tree.delete(item)
            if 0 <= item_idx < len(self.order_items):
                self.order_items.pop(item_idx)
        
        # Update total
        self.update_total()
    
    def update_total(self):
        total = sum(item["subtotal"] for item in self.order_items)
        self.total_label.config(text=f"Total: {total:,.2f}")
    
    def save_order(self):
        if not self.order_items:
            messagebox.showwarning("Warning", "Cannot save empty order")
            return
            
        if not self.order_number.get():
            messagebox.showerror("Error", "Order number is required")
            return
            
        try:
            conn = sqlite3.connect('order_system.db')
            c = conn.cursor()
            
            # Insert order header
            total_amount = sum(item["subtotal"] for item in self.order_items)
            c.execute('''INSERT INTO order_header 
                        (order_number, customer_ref, order_date, total_amount)
                        VALUES (?, ?, ?, ?)''',
                     (self.order_number.get(),
                      self.customer_ref.get(),
                      self.order_date.get(),
                      total_amount))
            
            order_id = c.lastrowid
            
            # Insert order details
            for item in self.order_items:
                c.execute('''INSERT INTO order_detail
                            (order_id, product_id, quantity, price, discount, subtotal)
                            VALUES (?, ?, ?, ?, ?, ?)''',
                         (order_id,
                          item["product_id"],
                          item["quantity"],
                          item["price"],
                          item["discount"],
                          item["subtotal"]))
            
            conn.commit()
            messagebox.showinfo("Success", "Order saved successfully")
            self.clear_order()
            
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", str(e))
            conn.rollback()
        finally:
            conn.close()
    
    def clear_order(self):
        self.order_number.delete(0, tk.END)
        self.customer_ref.delete(0, tk.END)
        self.order_date.delete(0, tk.END)
        self.order_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.tree.delete(*self.tree.get_children())
        self.order_items.clear()
        self.update_total()

if __name__ == "__main__":
    root = tk.Tk()
    app = OrderProcessingSystem(root)
    root.mainloop()