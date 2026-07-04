from database import get_connection
from flight import show_flights


# -----------------------------
# Buy Ticket
# -----------------------------
def buy_ticket(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    print("\n===== AVAILABLE FLIGHTS =====")
    show_flights()

    flight_id = input("\nEnter Flight ID: ")

    cursor.execute("SELECT * FROM flights WHERE id=?", (flight_id,))
    flight = cursor.fetchone()

    if not flight:
        print("Flight Not Found.")
        conn.close()
        return

    print("\n1. Single Ticket")
    print("2. Family Ticket")

    t_type = input("Choose Type: ")

    if t_type == "1":
        ticket_type = "SINGLE"
        passenger_count = 1

    elif t_type == "2":
        ticket_type = "FAMILY"
        passenger_count = int(input("Number of passengers: "))

    else:
        print("Invalid Type.")
        conn.close()
        return

    available_capacity = flight[6]

    if passenger_count > available_capacity:
        print("Not Enough Capacity.")
        conn.close()
        return

    total_price = passenger_count * flight[5]

    cursor.execute("""
        INSERT INTO tickets(
            user_id,
            flight_id,
            ticket_type,
            passenger_count,
            total_price,
            status
        )
        VALUES (?, ?, ?, ?, ?, 'ACTIVE')
    """, (
        user_id,
        flight_id,
        ticket_type,
        passenger_count,
        total_price
    ))

    cursor.execute("""
        UPDATE flights
        SET capacity = capacity - ?
        WHERE id = ?
    """, (
        passenger_count,
        flight_id
    ))

    conn.commit()
    conn.close()

    print("\nTicket Purchased Successfully!")


# -----------------------------
# Show My Tickets
# -----------------------------
def show_my_tickets(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.id,
            f.origin,
            f.destination,
            f.flight_date,
            f.departure_time,
            t.ticket_type,
            t.passenger_count,
            t.total_price,
            t.status
        FROM tickets t
        JOIN flights f ON t.flight_id = f.id
        WHERE t.user_id=?
    """, (user_id,))

    tickets = cursor.fetchall()

    conn.close()

    if not tickets:
        print("\nNo Tickets Found.")
        return

    print("\n========== MY TICKETS ==========")

    for t in tickets:

        print(f"""
Ticket ID     : {t[0]}
Route         : {t[1]} -> {t[2]}
Date          : {t[3]} {t[4]}
Type          : {t[5]}
Passengers    : {t[6]}
Total Price   : {t[7]}
Status        : {t[8]}
----------------------------------
""")


# -----------------------------
# Delete Ticket
# -----------------------------
def delete_ticket(user_id):

    ticket_id = input("Enter Ticket ID: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT flight_id, passenger_count
        FROM tickets
        WHERE id=? AND user_id=?
    """, (ticket_id, user_id))

    ticket = cursor.fetchone()

    if not ticket:
        print("Ticket Not Found.")
        conn.close()
        return

    flight_id, count = ticket

    cursor.execute("DELETE FROM tickets WHERE id=?", (ticket_id,))

    cursor.execute("""
        UPDATE flights
        SET capacity = capacity + ?
        WHERE id=?
    """, (count, flight_id))

    conn.commit()
    conn.close()

    print("Ticket Deleted Successfully.")


# -----------------------------
# Edit Ticket
# -----------------------------
def edit_ticket(user_id):

    ticket_id = input("Enter Ticket ID: ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT flight_id, passenger_count, ticket_type
        FROM tickets
        WHERE id=? AND user_id=?
    """, (ticket_id, user_id))

    ticket = cursor.fetchone()

    if not ticket:
        print("Ticket Not Found.")
        conn.close()
        return

    flight_id, old_count, old_type = ticket

    cursor.execute("SELECT ticket_price, capacity FROM flights WHERE id=?", (flight_id,))
    flight = cursor.fetchone()

    price, capacity = flight

    print("\n1. Change Passenger Count")
    print("2. Change Ticket Type")

    choice = input("Choose: ")

    if choice == "1":

        new_count = int(input("New Passenger Count: "))

        diff = new_count - old_count

        if diff > capacity:
            print("Not enough capacity.")
            conn.close()
            return

        new_price = new_count * price

        cursor.execute("""
            UPDATE tickets
            SET passenger_count=?, total_price=?
            WHERE id=? AND user_id=?
        """, (new_count, new_price, ticket_id, user_id))

        cursor.execute("""
            UPDATE flights
            SET capacity = capacity - ?
            WHERE id=?
        """, (diff, flight_id))

    elif choice == "2":

        new_type = input("Enter NEW TYPE (SINGLE/FAMILY): ")

        cursor.execute("""
            UPDATE tickets
            SET ticket_type=?
            WHERE id=? AND user_id=?
        """, (new_type, ticket_id, user_id))

    else:
        print("Invalid Choice.")
        conn.close()
        return

    conn.commit()
    conn.close()

    print("Ticket Updated Successfully.")