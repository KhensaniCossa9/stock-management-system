import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime
import csv


conn = sqlite3.connect("glowmark_stock.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    date_added TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    quantity_sold INTEGER NOT NULL,
    total_sale REAL NOT NULL,
    date_sold TEXT NOT NULL
)
""")

desired_columns = ["id", "name", "phone", "email", "product_type", "active"]


cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='suppliers'")
if cursor.fetchone() is None:
    
    cursor.execute("""
    CREATE TABLE suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        product_type TEXT,
        active INTEGER DEFAULT 1
    )
    """)
else:
    
    cursor.execute("PRAGMA table_info(suppliers)")
    existing_columns = [info[1] for info in cursor.fetchall()]
    
    if existing_columns != desired_columns:
        cursor.execute("ALTER TABLE suppliers RENAME TO suppliers_old")
        
        cursor.execute("""
        CREATE TABLE suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            product_type TEXT,
            active INTEGER DEFAULT 1
        )
        """)
        
        copy_columns = [col for col in desired_columns if col in existing_columns]
        if copy_columns:
            cols_str = ", ".join(copy_columns)
            cursor.execute(f"INSERT INTO suppliers ({cols_str}) SELECT {cols_str} FROM suppliers_old")
        
        cursor.execute("DROP TABLE suppliers_old")

conn.commit()

# main screen
app = tk.Tk()
app.title("Glowmark Stock Management System")
app.geometry("1100x650")
app.configure(bg="#ffffff")

# side bar
sidebar = tk.Frame(app, width=200, bg="#001F54", height=650)
sidebar.pack(side="left", fill="y")

# upload image to the system
logo_image = Image.open("glowmark_logo.png")
logo_image = logo_image.resize((150, 150))
logo = ImageTk.PhotoImage(logo_image)
logo_label = tk.Label(sidebar, image=logo, bg="#001F54")
logo_label.pack(pady=20)

# Sidebar buttons
button_specs = [
    ("Welcome", "#001F54"),
    ("Manage Stock", "#00BFFF"),
    ("Sales", "#32CD32"),
    ("Suppliers", "#FF69B4"),
    ("Alerts", "#FF4500"),
    ("Reports", "#8A2BE2")
]

buttons = {}
for text, color in button_specs:
    btn = tk.Button(sidebar, text=text, bg=color, fg="white", width=20, height=2)
    btn.pack(pady=5)
    buttons[text] = btn

# ---------------- Main Panel ----------------
main_panel = tk.Frame(app, bg="#ffffff", width=900, height=650)
main_panel.pack(side="right", fill="both", expand=True)

# ---------------- Welcome Page ----------------
def welcome_page():
    for widget in main_panel.winfo_children():
        widget.destroy()

    # Main container to center everything
    container = tk.Frame(main_panel, bg="#ffffff")
    container.pack(expand=True, fill="both")  # This will center the inner frame

    # Inner frame to hold content
    content = tk.Frame(container, bg="#ffffff")
    content.pack(expand=True)  # Vertically centered

    # Title
    tk.Label(content, text="Welcome to Glowmark's Stock Management System",
             font=("Arial", 22, "bold"), bg="#ffffff").pack(pady=20)

    # Stats Cards Frame
    stats_frame = tk.Frame(content, bg="#ffffff")
    stats_frame.pack(pady=10)

    # Total Sales Card
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("SELECT SUM(total_sale) FROM sales WHERE date_sold=?", (today,))
    total_sales_today = cursor.fetchone()[0] or 0

    sales_card = tk.Frame(stats_frame, bg="#32CD32", width=200, height=100)
    sales_card.pack(side="left", padx=20)
    sales_card.pack_propagate(False)
    tk.Label(sales_card, text="Total Sales Today", font=("Arial", 12, "bold"), bg="#32CD32", fg="white").pack(pady=10)
    tk.Label(sales_card, text=f"R{total_sales_today:.2f}", font=("Arial", 14), bg="#32CD32", fg="white").pack()

    # Low Stock Card
    cursor.execute("SELECT COUNT(*) FROM batches WHERE quantity <= 15")
    low_stock_count = cursor.fetchone()[0] or 0

    stock_card = tk.Frame(stats_frame, bg="#FF4500", width=200, height=100)
    stock_card.pack(side="left", padx=20)
    stock_card.pack_propagate(False)
    tk.Label(stock_card, text="Low Stock Items", font=("Arial", 12, "bold"), bg="#FF4500", fg="white").pack(pady=10)
    tk.Label(stock_card, text=f"{low_stock_count} item(s)", font=("Arial", 14), bg="#FF4500", fg="white").pack()

    # Low Stock Details (if any)
    cursor.execute("SELECT product_name, quantity FROM batches WHERE quantity <= 15")
    low_stock_items = cursor.fetchall()
    if low_stock_items:
        alert_frame = tk.Frame(content, bg="#ffffff")
        alert_frame.pack(pady=10)
        tk.Label(alert_frame, text="⚠ Low Stock Details:", font=("Arial", 16, "bold"), bg="#ffffff", fg="red").pack()
        for item in low_stock_items:
            tk.Label(alert_frame, text=f"{item[0]} - {item[1]} left", bg="#ffffff", fg="red").pack()

# ---------------- Manage Stock Page ----------------
def manage_stock_page():
    for widget in main_panel.winfo_children():
        widget.destroy()

    tk.Label(main_panel, text="Manage Stock", font=("Arial", 18, "bold"), bg="#ffffff").pack(pady=10)

    # Form
    form_frame = tk.Frame(main_panel, bg="#ffffff")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Product Name:", bg="#ffffff").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    name_entry = tk.Entry(form_frame, width=25)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Quantity:", bg="#ffffff").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    qty_entry = tk.Entry(form_frame, width=25)
    qty_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Price per Unit (R):", bg="#ffffff").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    price_entry = tk.Entry(form_frame, width=25)
    price_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Batch Date (YYYY-MM-DD):", bg="#ffffff").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    date_entry = tk.Entry(form_frame, width=25)
    date_entry.grid(row=3, column=1, padx=5, pady=5)
    date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    error_label = tk.Label(form_frame, text="", fg="red", bg="#ffffff")
    error_label.grid(row=4, column=0, columnspan=2)

    # Table
    table_frame = tk.Frame(main_panel, bg="#ffffff")
    table_frame.pack(pady=10, fill="both", expand=True)

    columns = ("ID", "Product Name", "Quantity", "Price (R)", "Total Amount (R)", "Batch Date")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    # ---------------- Functions ----------------
    def load_table():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT * FROM batches")
        batches = cursor.fetchall()
        for idx, batch in enumerate(batches):
            pid, pname, qty, price, date_added = batch
            total = qty * price
            tree.insert("", "end", values=(pid, pname, qty, f"{price:.2f}", f"{total:.2f}", date_added),
                        tags=("low_stock",) if qty <= 15 else ())
        tree.tag_configure("low_stock", background="#FFCCCC")

    def add_batch():
        error_label.config(text="")
        name = name_entry.get().strip()
        qty_text = qty_entry.get().strip()
        price_text = price_entry.get().strip()
        batch_date = date_entry.get().strip()
        try:
            qty = int(qty_text)
            price = float(price_text)
            datetime.strptime(batch_date, "%Y-%m-%d")
            if not name or qty <= 0 or price < 0:
                raise ValueError
        except:
            error_label.config(text="Enter valid details and date (YYYY-MM-DD)!")
            return
        cursor.execute(
            "INSERT INTO batches (product_name, quantity, price, date_added) VALUES (?, ?, ?, ?)",
            (name, qty, price, batch_date)
        )
        conn.commit()
        name_entry.delete(0, tk.END)
        qty_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        load_table()

    def delete_stock():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select an item to delete.")
            return
        stock_id = tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm Delete", "Delete this stock?"):
            cursor.execute("DELETE FROM batches WHERE id=?", (stock_id,))
            conn.commit()
            load_table()

    def edit_stock():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select an item to edit.")
            return
        stock = tree.item(selected[0])["values"]
        stock_id, name, qty, price, total, date_added = stock
        edit_win = tk.Toplevel(app)
        edit_win.title("Edit Stock")
        edit_win.geometry("300x260")
        tk.Label(edit_win, text="Product Name").pack(pady=5)
        name_e = tk.Entry(edit_win)
        name_e.pack()
        name_e.insert(0, name)
        tk.Label(edit_win, text="Quantity").pack(pady=5)
        qty_e = tk.Entry(edit_win)
        qty_e.pack()
        qty_e.insert(0, qty)
        tk.Label(edit_win, text="Price per Unit (R)").pack(pady=5)
        price_e = tk.Entry(edit_win)
        price_e.pack()
        price_e.insert(0, price)
        tk.Label(edit_win, text="Batch Date (YYYY-MM-DD)").pack(pady=5)
        date_e = tk.Entry(edit_win)
        date_e.pack()
        date_e.insert(0, date_added)

        def save_changes():
            try:
                new_name = name_e.get().strip()
                new_qty = int(qty_e.get())
                new_price = float(price_e.get())
                new_date = date_e.get().strip()
                datetime.strptime(new_date, "%Y-%m-%d")
                if not new_name or new_qty <= 0 or new_price < 0:
                    raise ValueError
                cursor.execute(
                    "UPDATE batches SET product_name=?, quantity=?, price=?, date_added=? WHERE id=?",
                    (new_name, new_qty, new_price, new_date, stock_id)
                )
                conn.commit()
                edit_win.destroy()
                load_table()
            except:
                messagebox.showerror("Invalid Input", "Enter valid stock details and date (YYYY-MM-DD).")

        tk.Button(edit_win, text="Save Changes", bg="#32CD32", fg="white", width=20, command=save_changes).pack(pady=15)

    # Buttons below table
    action_frame = tk.Frame(main_panel, bg="#ffffff")
    action_frame.pack(pady=10)
    tk.Button(action_frame, text="Edit Selected", bg="#32CD32", fg="white", width=18, command=edit_stock).pack(side="left", padx=10)
    tk.Button(action_frame, text="Delete Selected", bg="#FF4500", fg="white", width=18, command=delete_stock).pack(side="left", padx=10)
    tk.Button(action_frame, text="Add Batch", bg="#00BFFF", fg="white", width=18, command=add_batch).pack(side="left", padx=10)

    load_table()

def sales_page():
    for widget in main_panel.winfo_children():
        widget.destroy()

    tk.Label(main_panel, text="Record Sale", font=("Arial", 18, "bold"), bg="#ffffff").pack(pady=10)

    # ---------------- Form ----------------
    form_frame = tk.Frame(main_panel, bg="#ffffff")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Product Name:", bg="#ffffff").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    product_var = tk.StringVar()
    product_dropdown = ttk.Combobox(form_frame, textvariable=product_var, width=22)
    product_dropdown.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Quantity Sold:", bg="#ffffff").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    qty_entry = tk.Entry(form_frame, width=25)
    qty_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Date of Sale (YYYY-MM-DD):", bg="#ffffff").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    date_entry = tk.Entry(form_frame, width=25)
    date_entry.grid(row=2, column=1, padx=5, pady=5)
    date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    error_label = tk.Label(form_frame, text="", fg="red", bg="#ffffff")
    error_label.grid(row=3, column=0, columnspan=2)

    tk.Button(form_frame, text="Record Sale", bg="#32CD32", fg="white", width=20, command=lambda: record_sale()).grid(row=4, column=0, columnspan=2, pady=10)

    # ---------------- Search ----------------
    search_frame = tk.Frame(main_panel, bg="#ffffff")
    search_frame.pack(pady=5)
    tk.Label(search_frame, text="Search Product:", bg="#ffffff").pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, width=25)
    search_entry.pack(side="left", padx=5)
    tk.Button(search_frame, text="Search", bg="#00BFFF", fg="white", command=lambda: load_sales_table(search_entry.get(),
                                                                                                     from_date_entry.get(),
                                                                                                     to_date_entry.get())).pack(side="left", padx=5)

    # ---------------- Date Range Filters ----------------
    filter_frame = tk.Frame(main_panel, bg="#ffffff")
    filter_frame.pack(pady=5)

    tk.Label(filter_frame, text="From (YYYY-MM-DD):", bg="#ffffff").pack(side="left", padx=5)
    from_date_entry = tk.Entry(filter_frame, width=12)
    from_date_entry.pack(side="left", padx=5)

    tk.Label(filter_frame, text="To (YYYY-MM-DD):", bg="#ffffff").pack(side="left", padx=5)
    to_date_entry = tk.Entry(filter_frame, width=12)
    to_date_entry.pack(side="left", padx=5)

    tk.Button(filter_frame, text="Filter", bg="#32CD32", fg="white",
              command=lambda: load_sales_table(search_entry.get(), from_date_entry.get(), to_date_entry.get())).pack(side="left", padx=5)

    tk.Button(filter_frame, text="Clear Filter", bg="#FF4500", fg="white",
              command=lambda: [from_date_entry.delete(0, tk.END), to_date_entry.delete(0, tk.END), load_sales_table()]).pack(side="left", padx=5)

    # ---------------- Past Sales Table ----------------
    table_frame = tk.Frame(main_panel, bg="#ffffff")
    table_frame.pack(pady=10, fill="both", expand=True)

    columns = ("ID", "Product Name", "Quantity Sold", "Price per Unit", "Total Sale", "Date of Sale")
    sales_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    sales_tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=sales_tree.yview)
    scrollbar.pack(side="right", fill="y")
    sales_tree.configure(yscroll=scrollbar.set)

    for col in columns:
        sales_tree.heading(col, text=col)
        sales_tree.column(col, anchor="center", width=120)

    # ---------------- Functions ----------------
    def load_products():
        cursor.execute("SELECT DISTINCT product_name FROM batches WHERE quantity>0")
        products = [row[0] for row in cursor.fetchall()]
        product_dropdown['values'] = products

    def load_sales_table(search_term="", from_date="", to_date=""):
        for row in sales_tree.get_children():
            sales_tree.delete(row)

        query = "SELECT * FROM sales WHERE 1=1"
        params = []

        if search_term:
            query += " AND (product_name LIKE ? OR date_sold LIKE ?)"
            params.extend([f"%{search_term}%", f"%{search_term}%"])

        if from_date:
            query += " AND date_sold >= ?"
            params.append(from_date)
        if to_date:
            query += " AND date_sold <= ?"
            params.append(to_date)

        query += " ORDER BY date_sold DESC"
        cursor.execute(query, params)

        for sale in cursor.fetchall():
            sid, pname, qty, total, date_sold_val = sale[0], sale[1], sale[2], sale[3], sale[4]
            price_per_unit = total / qty if qty != 0 else 0

            # Highlight low stock
            cursor.execute("SELECT SUM(quantity) FROM batches WHERE product_name=?", (pname,))
            stock_qty = cursor.fetchone()[0] or 0
            fg_color = "red" if stock_qty <= 5 else "black"

            sales_tree.insert("", "end", values=(sid, pname, qty, f"{price_per_unit:.2f}", f"{total:.2f}", date_sold_val),
                              tags=(fg_color,))

        sales_tree.tag_configure("red", foreground="red")
        sales_tree.tag_configure("black", foreground="black")

    def record_sale():
        error_label.config(text="")
        product_name = product_var.get().strip()
        try:
            qty_to_sell = int(qty_entry.get())
            date_sold_val = date_entry.get().strip()
            datetime.strptime(date_sold_val, "%Y-%m-%d")
            if not product_name or qty_to_sell <= 0:
                raise ValueError
        except:
            error_label.config(text="Enter valid product and quantity/date!")
            return

        cursor.execute("SELECT id, quantity, price FROM batches WHERE product_name=? ORDER BY date_added ASC", (product_name,))
        batches = cursor.fetchall()
        if not batches:
            error_label.config(text="Product not found in stock!")
            return

        total_available = sum(batch[1] for batch in batches)
        if qty_to_sell > total_available:
            error_label.config(text=f"Not enough stock! Available: {total_available}")
            return

        total_sale = 0
        remaining_qty = qty_to_sell
        for batch_id, batch_qty, price in batches:
            if remaining_qty == 0:
                break
            if batch_qty <= remaining_qty:
                total_sale += batch_qty * price
                cursor.execute("DELETE FROM batches WHERE id=?", (batch_id,))
                remaining_qty -= batch_qty
            else:
                total_sale += remaining_qty * price
                cursor.execute("UPDATE batches SET quantity=? WHERE id=?", (batch_qty - remaining_qty, batch_id))
                remaining_qty = 0
        conn.commit()

        cursor.execute("INSERT INTO sales (product_name, quantity_sold, total_sale, date_sold) VALUES (?, ?, ?, ?)",
                       (product_name, qty_to_sell, total_sale, date_sold_val))
        conn.commit()

        messagebox.showinfo("Sale Recorded", f"Sale recorded!\nTotal: R{total_sale:.2f}")
        qty_entry.delete(0, tk.END)
        load_sales_table()
        load_products()

    # ---------------- Initial load ----------------
    load_products()
    load_sales_table()

def suppliers_page():
    for widget in main_panel.winfo_children():
        widget.destroy()

    tk.Label(main_panel, text="Suppliers", font=("Arial", 18, "bold"), bg="#ffffff").pack(pady=10)

    # ---------- Form ----------
    form = tk.Frame(main_panel, bg="#ffffff")
    form.pack(pady=10)

    labels = ["Supplier Name", "Phone", "Email", "Product Type"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(form, text=label + ":", bg="#ffffff").grid(row=i, column=0, sticky="e", padx=5, pady=5)
        ent = tk.Entry(form, width=30)
        ent.grid(row=i, column=1, padx=5, pady=5)
        entries[label] = ent

    active_var = tk.IntVar(value=1)
    tk.Checkbutton(form, text="Active Supplier", variable=active_var, bg="#ffffff").grid(
        row=4, column=1, sticky="w", pady=5
    )

    error_label = tk.Label(form, text="", fg="red", bg="#ffffff")
    error_label.grid(row=5, column=0, columnspan=2)

    # ---------- Table ----------
    table_frame = tk.Frame(main_panel, bg="#ffffff")
    table_frame.pack(fill="both", expand=True, pady=10)

    columns = ("ID", "Name", "Phone", "Email", "Product", "Active", "Edit", "Delete")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    # ---------- Load Suppliers ----------
    def load_suppliers(filter_text=""):
        for row in tree.get_children():
            tree.delete(row)

        query = "SELECT * FROM suppliers"
        params = ()
        if filter_text:
            query += " WHERE name LIKE ? OR product_type LIKE ?"
            params = (f"%{filter_text}%", f"%{filter_text}%")

        cursor.execute(query, params)
        for sup in cursor.fetchall():
            sid, name, phone, email, product, active = sup
            tree.insert("", "end",
                        values=(sid, name, phone, email, product,
                                "Yes" if active else "No", "Edit", "Delete"))

    # ---------- Add Supplier ----------
    def add_supplier():
        error_label.config(text="")
        name = entries["Supplier Name"].get().strip()
        if not name:
            error_label.config(text="Supplier name is required!")
            return

        try:
            cursor.execute("""
                INSERT INTO suppliers (name, phone, email, product_type, active)
                VALUES (?, ?, ?, ?, ?)
            """, (
                name,
                entries["Phone"].get().strip(),
                entries["Email"].get().strip(),
                entries["Product Type"].get().strip(),
                active_var.get()
            ))
            conn.commit()
        except Exception as e:
            error_label.config(text=f"Error adding supplier: {e}")
            return

        # Clear form
        for ent in entries.values():
            ent.delete(0, tk.END)
        active_var.set(1)

        load_suppliers()

    tk.Button(form, text="Add Supplier", bg="#00BFFF", fg="white", width=20,
              command=add_supplier).grid(row=6, column=0, columnspan=2, pady=10)

    # ---------- Edit / Delete ----------
    def on_click(event):
        item = tree.identify_row(event.y)
        if not item:
            return
        col = tree.identify_column(event.x)
        sid = tree.item(item, "values")[0]

        if col == "#7":  # Edit
            edit_supplier(sid)
        elif col == "#8":  # Delete
            if messagebox.askyesno("Confirm", "Delete supplier?"):
                cursor.execute("DELETE FROM suppliers WHERE id=?", (sid,))
                conn.commit()
                load_suppliers()

    tree.bind("<Button-1>", on_click)

    def edit_supplier(sid):
        cursor.execute("SELECT * FROM suppliers WHERE id=?", (sid,))
        sup = cursor.fetchone()

        win = tk.Toplevel(app)
        win.title("Edit Supplier")
        win.geometry("350x300")

        fields = ["Name", "Phone", "Email", "Product"]
        values = sup[1:5]
        edits = {}

        for i, (f, v) in enumerate(zip(fields, values)):
            tk.Label(win, text=f).pack()
            e = tk.Entry(win)
            e.pack()
            e.insert(0, v)
            edits[f] = e

        active_var_edit = tk.IntVar(value=sup[5])
        tk.Checkbutton(win, text="Active", variable=active_var_edit).pack()

        def save():
            cursor.execute("""
                UPDATE suppliers SET
                name=?, phone=?, email=?, product_type=?, active=?
                WHERE id=?
            """, (
                edits["Name"].get(),
                edits["Phone"].get(),
                edits["Email"].get(),
                edits["Product"].get(),
                active_var_edit.get(),
                sid
            ))
            conn.commit()
            win.destroy()
            load_suppliers()

        tk.Button(win, text="Save Changes", bg="#32CD32", fg="white", command=save).pack(pady=10)

    # ---------- Search ----------
    search_frame = tk.Frame(main_panel, bg="#ffffff")
    search_frame.pack(pady=5)
    tk.Label(search_frame, text="Search:", bg="#ffffff").pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, width=25)
    search_entry.pack(side="left", padx=5)
    tk.Button(search_frame, text="Search", bg="#00BFFF", fg="white",
              command=lambda: load_suppliers(search_entry.get())).pack(side="left", padx=5)

    load_suppliers()

def alerts_page():
    for widget in main_panel.winfo_children():
        widget.destroy()

    tk.Label(main_panel, text="Stock Alerts", font=("Arial", 18, "bold"), bg="#ffffff").pack(pady=10)

    # Guidelines
    tk.Label(main_panel, text="Guidelines: Red = Critical (<15), Yellow = Low (15-29), Green = Healthy (30+)",
             font=("Arial", 10), bg="#ffffff").pack(pady=5)

    # Filter by status
    filter_frame = tk.Frame(main_panel, bg="#ffffff")
    filter_frame.pack(pady=5)
    tk.Label(filter_frame, text="Filter by Status:", bg="#ffffff").pack(side="left", padx=5)
    status_var = tk.StringVar(value="All")
    status_dropdown = ttk.Combobox(filter_frame, textvariable=status_var,
                                   values=["All", "Healthy", "Low", "Critical"], width=12)
    status_dropdown.pack(side="left", padx=5)

    # Table
    table_frame = tk.Frame(main_panel, bg="#ffffff")
    table_frame.pack(fill="both", expand=True, pady=10)

    columns = ("ID", "Product Name", "Quantity", "Price (R)", "Total (R)", "Batch Date")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    tree.tag_configure("critical", background="#FC4F69")
    tree.tag_configure("low", background="#F8F879")
    tree.tag_configure("healthy", background="#62EF62")

    # ---------------- Functions ----------------
    def load_alerts():
        for row in tree.get_children():
            tree.delete(row)
        cursor.execute("SELECT * FROM batches")
        batches = cursor.fetchall()
        for pid, pname, qty, price, date_added in batches:
            total = qty * price
            # Determine tag
            if qty < 15:
                tag = "critical"
            elif qty < 30:
                tag = "low"
            else:
                tag = "healthy"
            # Apply filter
            selected = status_var.get()
            if selected == "Critical" and tag != "critical":
                continue
            elif selected == "Low" and tag != "low":
                continue
            elif selected == "Healthy" and tag != "healthy":
                continue
            tree.insert("", "end", values=(pid, pname, qty, f"{price:.2f}", f"{total:.2f}", date_added),
                        tags=(tag,))

    # Reorder button
    def reorder():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Select a product to reorder.")
            return
        # Go to Suppliers page
        suppliers_page()

    tk.Button(main_panel, text="Reorder Selected", bg="#00BFFF", fg="white", width=20, command=reorder).pack(pady=10)
    tk.Button(filter_frame, text="Apply Filter", bg="#32CD32", fg="white", command=load_alerts).pack(side="left", padx=5)

    load_alerts()
    
def reports_page():
    for widget in main_panel.winfo_children():
        widget.destroy()

    tk.Label(main_panel, text="Reports", font=("Arial", 20, "bold"), bg="#ffffff").pack(pady=10)

    # Scrollable main frame
    canvas = tk.Canvas(main_panel, bg="#ffffff")
    scrollbar = ttk.Scrollbar(main_panel, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ffffff")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ---------------- Stock Levels Report ----------------
    tk.Label(scrollable_frame, text="Stock Levels Report", font=("Arial", 16, "bold"), bg="#ffffff").pack(pady=5)

    table_frame = tk.Frame(scrollable_frame, bg="#ffffff")
    table_frame.pack(fill="both", expand=True, pady=5)

    stock_columns = ("ID", "Product Name", "Quantity", "Price (R)", "Total (R)")
    stock_tree = ttk.Treeview(table_frame, columns=stock_columns, show="headings")
    stock_tree.pack(side="left", fill="both", expand=True)

    stock_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=stock_tree.yview)
    stock_scroll.pack(side="right", fill="y")
    stock_tree.configure(yscrollcommand=stock_scroll.set)

    for col in stock_columns:
        stock_tree.heading(col, text=col)
        stock_tree.column(col, anchor="center", width=120)

    # Color coding
    stock_tree.tag_configure("critical", background="#FF9999")
    stock_tree.tag_configure("low", background="#FFFF99")
    stock_tree.tag_configure("healthy", background="#CCFFCC")

    # Load stock data sorted by lowest quantity first
    def load_stock_table():
        for row in stock_tree.get_children():
            stock_tree.delete(row)
        cursor.execute("SELECT * FROM batches ORDER BY quantity ASC")
        batches = cursor.fetchall()
        global stock_data
        stock_data = []
        for pid, pname, qty, price, date_added in batches:
            total = qty * price
            stock_data.append((pid, pname, qty, price, total))
            # Determine tag
            if qty < 15:
                tag = "critical"
            elif qty < 30:
                tag = "low"
            else:
                tag = "healthy"
            stock_tree.insert("", "end", values=(pid, pname, qty, f"{price:.2f}", f"{total:.2f}"), tags=(tag,))

    tk.Button(scrollable_frame, text="Export Stock CSV", bg="#32CD32", fg="white", width=25,
              command=lambda: export_stock_csv("stock_report_full.csv", stock_data)).pack(pady=5)
    load_stock_table()

    # Bar graph for stock
    tk.Label(scrollable_frame, text="Stock Levels Graph", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)
    graph_frame = tk.Frame(scrollable_frame, bg="#ffffff")
    graph_frame.pack(fill="both", expand=True)

    def load_stock_graph():
        for widget in graph_frame.winfo_children():
            widget.destroy()
        cursor.execute("SELECT product_name, SUM(quantity) FROM batches GROUP BY product_name ORDER BY SUM(quantity) ASC")
        data = cursor.fetchall()
        if not data:
            tk.Label(graph_frame, text="No stock data available", bg="#ffffff").pack()
            return

        max_qty = max([qty for _, qty in data]) or 1
        bar_width = 50
        spacing = 40
        canvas_width = len(data) * (bar_width + spacing) + 50

        stock_canvas = tk.Canvas(graph_frame, width=canvas_width, height=300, bg="#f0f0f0")
        stock_canvas.pack()

        for i, (pname, qty) in enumerate(data):
            x0 = i * (bar_width + spacing) + 50
            x1 = x0 + bar_width
            height = (qty / max_qty) * 200
            y0 = 250 - height
            y1 = 250

            # Color code
            if qty < 15:
                color = "#e74c3c"
            elif qty <= 30:
                color = "#f39c12"
            else:
                color = "#27ae60"

            stock_canvas.create_rectangle(x0, y0, x1, y1, fill=color)

            # Split long names vertically without slashes
            pname_lines = pname.split(" ")
            display_name = "\n".join(pname_lines)
            stock_canvas.create_text((x0 + x1)/2, y1 + 10, text=display_name, anchor="n")
            stock_canvas.create_text((x0 + x1)/2, y0 - 10, text=str(qty), anchor="s")

        # Legend
        legend_items = [("Critical (<15)", "#e74c3c"), ("Low (15–30)", "#f39c12"), ("Healthy (30+)", "#27ae60")]
        lx = 10
        for text, color in legend_items:
            stock_canvas.create_rectangle(lx, 10, lx+15, 25, fill=color)
            stock_canvas.create_text(lx+20, 17, text=text, anchor="w")
            lx += 120

    load_stock_graph()

    

# ---------------- CSV EXPORT FUNCTIONS ----------------

def export_stock_csv(filename, data):
    import csv
    if not data:
        messagebox.showinfo("Export CSV", "No data to export!")
        return
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Product Name", "Quantity", "Price (R)", "Total (R)"])
        writer.writerows(data)
    messagebox.showinfo("Export CSV", f"Stock report saved as {filename}!")

def export_sales_csv(filename, data):
    import csv
    if not data:
        messagebox.showinfo("Export CSV", "No data to export!")
        return
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Product Name", "Quantity Sold", "Total Sale (R)", "Date Sold"])
        writer.writerows(data)
    messagebox.showinfo("Export CSV", f"Sales report saved as {filename}!")

# 
buttons["Welcome"].config(command=welcome_page)
buttons["Manage Stock"].config(command=manage_stock_page)
buttons["Sales"].config(command=sales_page)
buttons["Suppliers"].config(command=suppliers_page)
buttons["Alerts"].config(command=alerts_page)
buttons["Reports"].config(command=reports_page)


welcome_page()
app.mainloop()