# bale -> parsaeghbali 
# address bot -> python_learnbot

import json
import os

FILE_NAME = "passwords.json"


# -------------------------
# Load Passwords
# -------------------------
def load_passwords():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    return {}


# -------------------------
# Save Passwords
# -------------------------
def save_passwords(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


# -------------------------
# Add Password
# -------------------------
def add_password(passwords):
    website = input("Website Name: ").strip()

    username = input("Username: ").strip()

    password = input("Password: ").strip()

    passwords[website] = {
        "username": username,
        "password": password
    }

    save_passwords(passwords)

    print("✅ Password saved successfully.")


# -------------------------
# Search Password
# -------------------------
def search_password(passwords):
    website = input("Website Name: ").strip()

    if website in passwords:
        print("\nFound:")
        print(f"Username: {passwords[website]['username']}")
        print(f"Password: {passwords[website]['password']}")
    else:
        print("❌ Website not found.")


# -------------------------
# Delete Password
# -------------------------
def delete_password(passwords):
    website = input("Website Name: ").strip()

    if website in passwords:
        del passwords[website]
        save_passwords(passwords)
        print("🗑 Password deleted.")
    else:
        print("❌ Website not found.")


# -------------------------
# Show All
# -------------------------
def show_all(passwords):
    if not passwords:
        print("No passwords stored.")
        return

    print("\nStored Accounts:")
    print("-" * 40)

    for website, info in passwords.items():
        print(f"Website : {website}")
        print(f"Username: {info['username']}")
        print(f"Password: {info['password']}")
        print("-" * 40)


# -------------------------
# Main Menu
# -------------------------
def main():
    passwords = load_passwords()

    while True:
        print("\n===== Password Manager =====")
        print("1. Add Password")
        print("2. Search Password")
        print("3. Delete Password")
        print("4. Show All Passwords")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_password(passwords)

        elif choice == "2":
            search_password(passwords)

        elif choice == "3":
            delete_password(passwords)

        elif choice == "4":
            show_all(passwords)

        elif choice == "5":
            print("Goodbye 👋")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()