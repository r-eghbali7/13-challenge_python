# bale -> @parsaeghbali
# address bot -> @python_learnbot


from database import create_tables
from seed import seed_flights
from auth import register, login
from ticket import (
    buy_ticket,
    show_my_tickets,
    delete_ticket,
    edit_ticket
)


# ---------------------------------
# INIT SYSTEM
# ---------------------------------
create_tables()
seed_flights()


# ---------------------------------
# MAIN APP
# ---------------------------------
def main():

    current_user = None

    while True:

        if current_user is None:

            print("\n========== WELCOME ==========")
            print("1. Register")
            print("2. Login")
            print("0. Exit")
            print("=============================")

            choice = input("Select: ")

            if choice == "1":
                register()

            elif choice == "2":
                user = login()

                if user:
                    current_user = user

            elif choice == "0":
                print("Good Bye 👋")
                break

            else:
                print("Invalid Choice")

        else:

            print(f"\nWelcome {current_user['first_name']} {current_user['last_name']}")
            print("\n========== DASHBOARD ==========")
            print("1. Buy Ticket")
            print("2. My Tickets")
            print("3. Edit Ticket")
            print("4. Delete Ticket")
            print("5. Logout")
            print("0. Exit")
            print("==============================")

            choice = input("Select: ")

            if choice == "1":
                buy_ticket(current_user["id"])

            elif choice == "2":
                show_my_tickets(current_user["id"])

            elif choice == "3":
                edit_ticket(current_user["id"])

            elif choice == "4":
                delete_ticket(current_user["id"])

            elif choice == "5":
                current_user = None
                print("Logged out successfully.")

            elif choice == "0":
                print("Good Bye 👋")
                break

            else:
                print("Invalid Choice")


# ---------------------------------
# RUN PROGRAM
# ---------------------------------
if __name__ == "__main__":
    main()