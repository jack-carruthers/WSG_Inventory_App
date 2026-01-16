import sqlite3
import hashlib

DB_NAME = "inventory.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def hash_password(password):

    # Hashing password using SHA-256 for added security
    return hashlib.sha256(password.encode()).hexdigest()

def initialise_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Create users table and inventory table if they dont exist already
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    # Create inventory table if it dont exist 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        itemName TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        batchNumber TEXT NOT NULL UNIQUE,
        location TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)

    # store hashed password for admin
    hashed_pass = hash_password("123")
    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
        ("admin", hashed_pass)
    )

    # sample data
    sample_items = [
        ("Flight Control Sensor", 45, "FCU-A12", "Hangar A", "OK"),
        ("Navigation Module", 12, "NAV-B07", "Avionics Lab", "LOW STOCK"),
        ("Power Distribution Unit", 0, "PDU-C03", "Warehouse 2", "OUT OF STOCK"),
        ("Temperature Probe", 87, "TMP-D21", "Warehouse 1", "OK"),
        ("Servo Actuator", 6, "ACT-E09", "Maintenance Bay", "LOW STOCK")
    ]
    
    # Insert sample data into inventory table if it dont exist already
    cursor.executemany("""
        INSERT OR IGNORE INTO inventory
        (itemName, quantity, batchNumber, location, status)
        VALUES (?, ?, ?, ?, ?)
    """, sample_items)

    conn.commit()
    conn.close()
