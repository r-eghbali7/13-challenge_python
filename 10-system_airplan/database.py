import sqlite3

DB_NAME = "database.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # =======================
    # Users Table
    # =======================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =======================
    # Flights Table
    # =======================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flights(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        flight_date TEXT NOT NULL,
        departure_time TEXT NOT NULL,
        ticket_price INTEGER NOT NULL,
        capacity INTEGER NOT NULL
    )
    """)

    # =======================
    # Tickets Table
    # =======================
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        flight_id INTEGER NOT NULL,
        ticket_type TEXT NOT NULL,
        passenger_count INTEGER NOT NULL,
        total_price INTEGER NOT NULL,
        status TEXT DEFAULT 'ACTIVE',

        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(flight_id) REFERENCES flights(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database Created Successfully.")