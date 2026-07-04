import re
import hashlib

from database import get_connection
from otp import send_otp, verify_otp


# -----------------------------
# Hash Password
# -----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# -----------------------------
# Validate Phone
# -----------------------------
def validate_phone(phone):

    pattern = r"^09\d{9}$"

    if re.match(pattern, phone):
        return True

    return False


# -----------------------------
# Check Phone Exists
# -----------------------------
def phone_exists(phone):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE phone=?",
        (phone,)
    )

    user = cursor.fetchone()

    conn.close()

    return user is not None


# -----------------------------
# Register User
# -----------------------------
def register():

    print("\n===== Register =====")

    first_name = input("First Name : ").strip()
    last_name = input("Last Name : ").strip()

    phone = input("Phone : ").strip()

    if not validate_phone(phone):
        print("Invalid Phone Number.")
        return

    if phone_exists(phone):
        print("Phone Already Exists.")
        return

    password = input("Password : ")

    if len(password) < 6:
        print("Password Must Be At Least 6 Characters.")
        return

    print("\nSending OTP...")

    send_otp(phone)

    code = input("Enter OTP : ")

    if not verify_otp(phone, code):
        print("Wrong OTP.")
        return

    hashed = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users(
        first_name,
        last_name,
        phone,
        password
    )
    VALUES(?,?,?,?)
    """,
    (
        first_name,
        last_name,
        phone,
        hashed
    ))

    conn.commit()
    conn.close()

    print("Registration Successful.")

    # -----------------------------
# Login User
# -----------------------------
def login():

    print("\n===== Login =====")

    phone = input("Phone : ").strip()
    password = input("Password : ")

    hashed = hash_password(password)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            first_name,
            last_name,
            phone
        FROM users
        WHERE phone=? AND password=?
    """, (phone, hashed))

    user = cursor.fetchone()

    conn.close()

    if user is None:
        print("\nPhone or Password is incorrect.\n")
        return None

    print(f"\nWelcome {user[1]} {user[2]}\n")

    return {
        "id": user[0],
        "first_name": user[1],
        "last_name": user[2],
        "phone": user[3]
    }


# -----------------------------
# Get User By ID
# -----------------------------
def get_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            first_name,
            last_name,
            phone
        FROM users
        WHERE id=?
    """, (user_id,))

    user = cursor.fetchone()

    conn.close()

    if user is None:
        return None

    return {
        "id": user[0],
        "first_name": user[1],
        "last_name": user[2],
        "phone": user[3]
    }


# -----------------------------
# Show Profile
# -----------------------------
def show_profile(user_id):

    user = get_user(user_id)

    if user is None:
        print("User Not Found.")
        return

    print("\n========== PROFILE ==========")
    print(f"ID         : {user['id']}")
    print(f"First Name : {user['first_name']}")
    print(f"Last Name  : {user['last_name']}")
    print(f"Phone      : {user['phone']}")
    print("=============================\n")


# -----------------------------
# Change Password
# -----------------------------
def change_password(user_id):

    print("\n===== Change Password =====")

    current = input("Current Password : ")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE id=?",
        (user_id,)
    )

    result = cursor.fetchone()

    if result is None:
        conn.close()
        print("User Not Found.")
        return

    if hash_password(current) != result[0]:
        conn.close()
        print("Current Password Is Incorrect.")
        return

    new_password = input("New Password : ")

    if len(new_password) < 6:
        conn.close()
        print("Password Must Be At Least 6 Characters.")
        return

    confirm = input("Confirm Password : ")

    if new_password != confirm:
        conn.close()
        print("Passwords Do Not Match.")
        return

    cursor.execute(
        "UPDATE users SET password=? WHERE id=?",
        (
            hash_password(new_password),
            user_id
        )
    )

    conn.commit()
    conn.close()

    print("Password Changed Successfully.")


# -----------------------------
# Delete Account
# -----------------------------
def delete_account(user_id):

    answer = input(
        "Are You Sure? (Y/N): "
    ).upper()

    if answer != "Y":
        print("Cancelled.")
        return False

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()

    print("Account Deleted Successfully.")

    return True


# ---------------------------------
# Logout
# ---------------------------------
def logout():

    print("\nLogout Successful.\n")


# ---------------------------------
# Test Menu
# ---------------------------------
if __name__ == "__main__":

    current_user = None

    while True:

        print("\n========== AUTH MENU ==========")
        print("1. Register")
        print("2. Login")
        print("3. Show Profile")
        print("4. Change Password")
        print("5. Delete Account")
        print("6. Logout")
        print("0. Exit")
        print("================================")

        choice = input("Select : ")

        if choice == "1":
            register()

        elif choice == "2":

            user = login()

            if user:
                current_user = user

        elif choice == "3":

            if current_user:
                show_profile(current_user["id"])
            else:
                print("Please Login First.")

        elif choice == "4":

            if current_user:
                change_password(current_user["id"])
            else:
                print("Please Login First.")

        elif choice == "5":

            if current_user:

                deleted = delete_account(current_user["id"])

                if deleted:
                    current_user = None

            else:
                print("Please Login First.")

        elif choice == "6":

            current_user = None
            logout()

        elif choice == "0":

            print("Good Bye...")
            break

        else:

            print("Invalid Choice.")