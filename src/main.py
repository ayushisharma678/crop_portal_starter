
from tabulate import tabulate
import pandas as pd
from getpass import getpass

from storage import (
    load_users, save_users,
    load_crops, save_crops,
    load_farmers, save_farmers,
    next_id, ensure_data_files
)
from security import hash_password, verify_password

def pause():
    input("\nPress Enter to continue... ")

def print_table(df: pd.DataFrame, headers="keys"):
    if df is None or df.empty:
        print("(no records)")
    else:
        print(tabulate(df, headers=headers, tablefmt="grid", showindex=False))

# ----------------- Auth -----------------

def register_client():
    users = load_users()
    print("\n=== Client Registration ===")
    username = input("Choose a username: ").strip()
    if (users["username"] == username).any():
        print("Username already exists! Try another.")
        return
    name = input("Your full name: ").strip()
    password = getpass("Choose a password: ").strip()
    phash, salt = hash_password(password)
    user_id = next_id(users, "user_id")
    new_row = {
        "user_id": user_id,
        "username": username,
        "role": "client",
        "name": name,
        "password_hash": phash,
        "salt": salt
    }
    users = pd.concat([users, pd.DataFrame([new_row])], ignore_index=True)
    save_users(users)
    print("Registration successful! You can now log in.")

def login():
    users = load_users()
    print("\n=== Login ===")
    username = input("Username: ").strip()
    password = getpass("Password: ").strip()
    row = users[users["username"] == username]
    if row.empty:
        print("User not found.")
        return None
    row = row.iloc[0]
    if verify_password(password, row["password_hash"], row["salt"]):
        print(f"Welcome, {row['name']}! Role: {row['role']}")
        return {"user_id": int(row["user_id"]), "username": row["username"], "name": row["name"], "role": row["role"]}
    else:
        print("Incorrect password.")
        return None

# ----------------- Admin Menus -----------------

def admin_menu(user):
    while True:
        print("\n=== Admin Menu ===")
        print("1. View crops")
        print("2. Add crop")
        print("3. Update crop")
        print("4. Delete crop")
        print("5. View farmers")
        print("0. Logout")
        choice = input("Choose: ").strip()
        if choice == "1":
            view_crops()
        elif choice == "2":
            add_crop()
        elif choice == "3":
            update_crop()
        elif choice == "4":
            delete_crop()
        elif choice == "5":
            view_farmers()
        elif choice == "0":
            break
        else:
            print("Invalid choice!")
        pause()

def view_crops():
    crops = load_crops()
    print("\n=== Crop List ===")
    print_table(crops)

def add_crop():
    crops = load_crops()
    print("\n=== Add Crop ===")
    name = input("Crop name: ").strip()
    season = input("Season (Kharif/Rabi/Zaid): ").strip()
    price = input("Price per quintal: ").strip()
    fert = input("Fertilizer: ").strip()
    water = input("Water needs (Low/Medium/High): ").strip()
    crop_id = next_id(crops, "crop_id")
    new_row = {
        "crop_id": crop_id,
        "crop_name": name,
        "season": season,
        "price_per_quintal": price,
        "fertilizer": fert,
        "water_needs": water
    }
    crops = pd.concat([crops, pd.DataFrame([new_row])], ignore_index=True)
    save_crops(crops)
    print("Crop added.")

def update_crop():
    crops = load_crops()
    print_table(crops)
    cid = input("Enter crop_id to update: ").strip()
    if (crops["crop_id"] == cid).any():
        idx = crops.index[crops["crop_id"] == cid][0]
        print("Leave blank to keep existing value.")
        for field in ["crop_name", "season", "price_per_quintal", "fertilizer", "water_needs"]:
            cur = crops.at[idx, field]
            val = input(f"{field} [{cur}]: ").strip()
            if val:
                crops.at[idx, field] = val
        save_crops(crops)
        print("Crop updated.")
    else:
        print("Invalid crop_id.")

def delete_crop():
    crops = load_crops()
    print_table(crops)
    cid = input("Enter crop_id to delete: ").strip()
    if (crops["crop_id"] == cid).any():
        crops = crops[crops["crop_id"] != cid]
        save_crops(crops)
        print("Crop deleted.")
    else:
        print("Invalid crop_id.")

def view_farmers():
    farmers = load_farmers()
    print("\n=== Farmers ===")
    print_table(farmers)

# ----------------- Client Menus -----------------

def client_menu(user):
    while True:
        print(f"\n=== Client Menu ({user['username']}) ===")
        print("1. View available crops")
        print("2. Add/Update my crop record")
        print("3. Delete my crop record")
        print("0. Logout")
        choice = input("Choose: ").strip()
        if choice == "1":
            view_crops()
        elif choice == "2":
            upsert_my_record(user)
        elif choice == "3":
            delete_my_record(user)
        elif choice == "0":
            break
        else:
            print("Invalid choice!")
        pause()

def upsert_my_record(user):
    farmers = load_farmers()
    mask = (farmers["username"] == user["username"])
    if mask.any():
        idx = farmers.index[mask][0]
        print("Updating your existing record. Leave blank to keep current value.")
        for field in ["name", "location", "crop_grown", "quantity_quintal", "contact"]:
            cur = farmers.at[idx, field]
            val = input(f"{field} [{cur}]: ").strip()
            if val:
                farmers.at[idx, field] = val
    else:
        print("Creating your crop record.")
        name = input("Full name: ").strip() or user["name"]
        location = input("Location: ").strip()
        crop_grown = input("Crop grown: ").strip()
        quantity = input("Quantity (quintal): ").strip()
        contact = input("Contact: ").strip()
        farmer_id = next_id(farmers, "farmer_id")
        new_row = {
            "farmer_id": farmer_id,
            "username": user["username"],
            "name": name,
            "location": location,
            "crop_grown": crop_grown,
            "quantity_quintal": quantity,
            "contact": contact
        }
        farmers = pd.concat([farmers, pd.DataFrame([new_row])], ignore_index=True)
    save_farmers(farmers)
    print("Saved!")

def delete_my_record(user):
    farmers = load_farmers()
    before = len(farmers)
    farmers = farmers[farmers["username"] != user["username"]]
    after = len(farmers)
    save_farmers(farmers)
    if after < before:
        print("Your record was deleted.")
    else:
        print("No record found to delete.")

# User Management
def user_management_menu():
    while True:
        print("\n=== User Management ===")
        print("1. View users")
        print("2. Update user")
        print("3. Delete user")
        print("0. Back")
        choice = input("Choose: ").strip()
        if choice == "1":
            view_users()
        elif choice == "2":
            update_user()
        elif choice == "3":
            delete_user()
        elif choice == "0":
            break
        else:
            print("Invalid choice!")
        pause()

def view_users():
    users = load_users()
    print("\n=== Users ===")
    print_table(users)

def update_user():
    users = load_users()
    print_table(users)
    uid = input("Enter user_id to update: ").strip()
    if (users["user_id"].astype(str) == uid).any():
        idx = users.index[users["user_id"].astype(str) == uid][0]
        print("Leave blank to keep existing value.")
        for field in ["username", "name", "role"]:
            cur = users.at[idx, field]
            val = input(f"{field} [{cur}]: ").strip()
            if val:
                users.at[idx, field] = val
        save_users(users)
        print("User updated.")
    else:
        print("Invalid user_id.")

def delete_user():
    users = load_users()
    print_table(users)
    uid = input("Enter user_id to delete: ").strip()
    if (users["user_id"].astype(str) == uid).any():
        users = users[users["user_id"].astype(str) != uid]
        save_users(users)
        print("User deleted.")
    else:
        print("Invalid user_id.")

# updating admin menu
def admin_menu(user):
    while True:
        print("\n=== Admin Menu ===")
        print("1. View crops")
        print("2. Add crop")
        print("3. Update crop")
        print("4. Delete crop")
        print("5. View farmers")
        print("6. Manage users")   # <-- NEW
        print("0. Logout")
        choice = input("Choose: ").strip()
        if choice == "1":
            view_crops()
        elif choice == "2":
            add_crop()
        elif choice == "3":
            update_crop()
        elif choice == "4":
            delete_crop()
        elif choice == "5":
            view_farmers()
        elif choice == "6":         # <-- NEW
            user_management_menu()
        elif choice == "0":
            break
        else:
            print("Invalid choice!")
        pause()

# ----------------- Main Loop -----------------

def main():
    ensure_data_files()
    while True:
        print("\n===== Crop Management Portal =====")
        print("1. Register (client)")
        print("2. Login (admin/client)")
        print("0. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            register_client()
        elif choice == "2":
            user = login()
            if user:
                if user["role"] == "admin":
                    admin_menu(user)
                else:
                    client_menu(user)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
