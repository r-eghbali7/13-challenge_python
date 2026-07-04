from database import get_connection

def seed_flights():
    conn = get_connection()
    cursor = conn.cursor()

    # بررسی اینکه قبلاً اطلاعات ثبت شده یا نه
    cursor.execute("SELECT COUNT(*) FROM flights")
    count = cursor.fetchone()[0]

    if count > 0:
        print("Flights already exist.")
        conn.close()
        return

    flights = [
        ("تهران", "مشهد", "1405/05/01", "09:00", 2500000, 100),
        ("تهران", "کیش", "1405/05/03", "16:30", 3200000, 80),
        ("تهران", "شیراز", "1405/05/06", "11:15", 2100000, 90),
        ("تهران", "تبریز", "1405/05/10", "18:45", 1800000, 70),
        ("تهران", "اصفهان", "1405/05/15", "07:30", 1700000, 60),
    ]

    cursor.executemany("""
        INSERT INTO flights(
            origin,
            destination,
            flight_date,
            departure_time,
            ticket_price,
            capacity
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, flights)

    conn.commit()
    conn.close()

    print("5 Flights Added Successfully.")


if __name__ == "__main__":
    seed_flights()