from database import get_connection


# -----------------------------
# Show All Flights
# -----------------------------
def show_flights():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, origin, destination, flight_date,
               departure_time, ticket_price, capacity
        FROM flights
    """)

    flights = cursor.fetchall()
    conn.close()

    if not flights:
        print("No Flights Available.")
        return

    print("\n========== FLIGHTS ==========")

    for f in flights:
        print(f"""
Flight ID   : {f[0]}
Route       : {f[1]} -> {f[2]}
Date        : {f[3]}
Time        : {f[4]}
Price       : {f[5]}
Capacity    : {f[6]}
-----------------------------
""")


# -----------------------------
# Search Flights
# -----------------------------
def search_flights():

    origin = input("Origin: ").strip()
    destination = input("Destination: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, origin, destination, flight_date,
               departure_time, ticket_price, capacity
        FROM flights
        WHERE origin=? AND destination=?
    """, (origin, destination))

    flights = cursor.fetchall()
    conn.close()

    if not flights:
        print("No Matching Flights Found.")
        return

    print("\n===== SEARCH RESULTS =====")

    for f in flights:
        print(f"""
Flight ID   : {f[0]}
Route       : {f[1]} -> {f[2]}
Date        : {f[3]}
Time        : {f[4]}
Price       : {f[5]}
Capacity    : {f[6]}
-----------------------------
""")


# -----------------------------
# Get Flight By ID
# -----------------------------
def get_flight_by_id(flight_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, origin, destination, flight_date,
               departure_time, ticket_price, capacity
        FROM flights
        WHERE id=?
    """, (flight_id,))

    flight = cursor.fetchone()
    conn.close()

    return flight


# -----------------------------
# Show Single Flight Detail
# -----------------------------
def show_flight_detail(flight_id):

    flight = get_flight_by_id(flight_id)

    if not flight:
        print("Flight Not Found.")
        return

    print("\n===== FLIGHT DETAIL =====")
    print(f"ID        : {flight[0]}")
    print(f"Route     : {flight[1]} -> {flight[2]}")
    print(f"Date      : {flight[3]}")
    print(f"Time      : {flight[4]}")
    print(f"Price     : {flight[5]}")
    print(f"Capacity  : {flight[6]}")
    print("=========================\n")