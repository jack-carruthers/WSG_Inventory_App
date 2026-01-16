from database import get_connection, hash_password

LOW_STOCK_THRESHOLD = 20

# function to calculate status based on quantity
def calculate_status(quantity):
    if quantity <= 0:
        return "OUT OF STOCK"
    elif quantity < LOW_STOCK_THRESHOLD:
        return "LOW STOCK"
    return "OK"

# login function to authenticate user
def login(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hashed_password)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None

# load all items from database
def load_inventory():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()
    conn.close()
    return rows

# add new item to database
def add_item(name, quantity, batch, location):
    status = calculate_status(quantity)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO inventory (itemName, quantity, batchNumber, location, status)
        VALUES (?, ?, ?, ?, ?)
    """, (name, quantity, batch, location, status))
    conn.commit()
    conn.close()

# delete item from database
def delete_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE id=?", (item_id,))
    conn.commit()
    conn.close()

# update existing item in database
def update_item(item_id, name, quantity, batch, location):
    status = calculate_status(quantity)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE inventory
        SET itemName=?, quantity=?, batchNumber=?, location=?, status=?
        WHERE id=?
    """, (name, quantity, batch, location, status, item_id))
    conn.commit()
    conn.close()

# search inventory items by name or batch number
def search_inventory(term):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM inventory
        WHERE itemName LIKE ? OR batchNumber LIKE ?
    """, (f"%{term}%", f"%{term}%"))
    results = cursor.fetchall()
    conn.close()
    return results
