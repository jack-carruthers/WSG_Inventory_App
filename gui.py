import tkinter as tk
from tkinter import ttk, messagebox
from services import *

# Helper to center windows
def centre_window(window, w, h):
    window.update_idletasks()
    x = (window.winfo_screenwidth() // 2) - (w // 2)
    y = (window.winfo_screenheight() // 2) - (h // 2)
    window.geometry(f"{w}x{h}+{x}+{y}")



# ------------------------- Login window --------------------------

def login_window():
    win = tk.Tk()
    win.title("Login")
    win.configure(bg="white")
    centre_window(win, 350, 300)

    # Title label
    title_label = tk.Label(
        win,
        text="WSG Inventory Login",
        bg="#03B185",
        fg="white",
        font=("Arial", 18, "bold"),
        pady=10
    )
    title_label.pack(fill=tk.X, pady=(20, 30))

    form_frame = tk.Frame(win, bg="white")
    form_frame.pack(pady=10)

    # Username textbox
    tk.Label(form_frame, text="Username:", bg="white", fg="#03B185", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=10, pady=5)
    user_entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
    user_entry.grid(row=0, column=1, padx=10, pady=5)

    # Password textbox
    tk.Label(form_frame, text="Password:", bg="white", fg="#03B185", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
    pass_entry = tk.Entry(form_frame, show="*", font=("Arial", 12), width=20)
    pass_entry.grid(row=1, column=1, padx=10, pady=5)

    # Login function handler
    def attempt_login():
        if login(user_entry.get(), pass_entry.get()):
            win.destroy()
            inventory_window()
        else:
            messagebox.showerror("Error", "Invalid login")

    # Login button
    login_btn = tk.Button(
        win,
        text="Login",
        command=attempt_login,
        bg="#03B185",
        fg="white",
        font=("Arial", 12, "bold"),
        padx=20,
        pady=5
    )
    login_btn.pack(pady=20)

    win.mainloop()

# ------------------ Inventory management window -----------------------

def inventory_window():
    win = tk.Tk()
    win.title("Component Inventory System")
    centre_window(win, 900, 500)

    header_frame = tk.Frame(win)
    header_frame.pack(fill=tk.X, pady=15)

    # Page header
    header_label = tk.Label(
        header_frame,
        text="Wyre Systems Group Inventory System",
        bg="#03B185",
        fg="white",
        font=("Arial", 16, "bold")
    )
    header_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    # search bar on the right
    search_entry = tk.Entry(header_frame, font=("Arial", 12))
    search_entry.pack(side=tk.RIGHT, padx=(0,5))

    # Button to trigger search
    search_btn = tk.Button(
        header_frame, 
        text="Go", 
        command=lambda: refresh(search_inventory(search_entry.get())),
        bg="white", 
        fg="#03B185", 
        font=("Arial", 10, "bold")
    )
    search_btn.pack(side=tk.RIGHT, padx=(5,10))

    
    
    # Inventory table
    columns = ("ID", "Item", "Qty", "Batch", "Location", "Status")
    tree = ttk.Treeview(win, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=140)

    tree.pack(fill=tk.BOTH, expand=True)

    def refresh(data=None):
        tree.delete(*tree.get_children())
        rows = data if data else load_inventory()
        for row in rows:
            tree.insert("", tk.END, values=row)

    refresh()



    # ----------------------------- ADD ITEM ----------------------------

    # breakout window to add new item
    def add_item_window():
        popup = tk.Toplevel(win)
        popup.title("Add Inventory Item")
        centre_window(popup, 350, 350)

        tk.Label(popup, text="Item Name:").pack(pady=5)
        name_entry = tk.Entry(popup)
        name_entry.pack(pady=5)

        tk.Label(popup, text="Quantity:").pack(pady=5)
        qty_entry = tk.Entry(popup)
        qty_entry.pack(pady=5)

        tk.Label(popup, text="Batch Number:").pack(pady=5)
        batch_entry = tk.Entry(popup)
        batch_entry.pack(pady=5)

        tk.Label(popup, text="Location:").pack(pady=5)
        loc_entry = tk.Entry(popup)
        loc_entry.pack(pady=5)

        def save_add():
            name = name_entry.get()
            qty = qty_entry.get()
            batch = batch_entry.get()
            loc = loc_entry.get()

            # Input validation
            if not name or not qty or not batch or not loc:
                messagebox.showwarning("Warning", "All fields are required.")
                return
            if not qty.isdigit() or int(qty) < 0:
                messagebox.showwarning("Warning", "Quantity must be a non-negative number.")
                return

            add_item(name, int(qty), batch, loc)
            refresh()
            popup.destroy()

        tk.Button(popup, text="Save Item", command=save_add).pack(pady=20)



    # ----------------------------- UPDATE ITEM -----------------------------

    # breakout window to update selected item
    def update_item_window():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an item to update")
            return

        item = tree.item(selected[0])["values"]
        item_id, name_val, qty_val, batch_val, loc_val, status_val = item

        popup = tk.Toplevel(win)
        popup.title("Update Inventory Item")
        centre_window(popup, 350, 350)

        tk.Label(popup, text="Item Name:").pack(pady=5)
        name_entry = tk.Entry(popup)
        name_entry.pack(pady=5)
        name_entry.insert(0, name_val) # insert current value to edit

        tk.Label(popup, text="Quantity:").pack(pady=5)
        qty_entry = tk.Entry(popup)
        qty_entry.pack(pady=5)
        qty_entry.insert(0, qty_val)

        tk.Label(popup, text="Batch Number:").pack(pady=5)
        batch_entry = tk.Entry(popup)
        batch_entry.pack(pady=5)
        batch_entry.insert(0, batch_val) #insert current value to edit

        tk.Label(popup, text="Location:").pack(pady=5)
        loc_entry = tk.Entry(popup)
        loc_entry.pack(pady=5)
        loc_entry.insert(0, loc_val) #insert current value to edit

        def save_update():
            name = name_entry.get()
            qty = qty_entry.get()
            batch = batch_entry.get()
            loc = loc_entry.get() 


            # Input validation 
            if not name or not qty or not batch or not loc:
                messagebox.showwarning("Warning", "All fields are required.")
                return
            if not qty.isdigit() or int(qty) < 0:
                messagebox.showwarning("Warning", "Quantity must be a non-negative number.")
                return

            update_item(item_id, name, int(qty), batch, loc)
            refresh()
            popup.destroy()

        tk.Button(popup, text="Save Changes", command=save_update).pack(pady=20)



    # ----------------------------- DELETE ITEM -----------------------------
    
    # delete selected item from inventory
    def delete_selected():
        selected = tree.selection()
        if not selected:
            return
        item_id = tree.item(selected[0])["values"][0]
        delete_item(item_id)
        refresh()


    # ---------------- BUTTONS ----------------

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame,bg="#CECECE", fg="#03B185", text="Add Item", command=add_item_window).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame,bg="#CECECE", fg="#03B185", text="Update Item", command=update_item_window).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame,bg="#CECECE", fg="#03B185", text="Delete Item", command=delete_selected).grid(row=0, column=2, padx=5)

    win.mainloop()
