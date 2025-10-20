#===============================================
import sys
import os
import pandas as pd
from tabulate import tabulate
from getpass import getpass

from storage import (
    load_users, save_users,
    load_crops, save_crops, 
    load_farmers, save_farmers,
    next_id, ensure_data_files
)
from security import hash_password, verify_password

# ================= File Paths =================


DATA_DIR = "data"
CROP_PROFIT_CSV = os.path.join(DATA_DIR, "crop_profit_data.csv")
CROP_DETAILS_CSV = os.path.join(DATA_DIR, "crop_details.csv")
FARMER_CROPS_CSV = os.path.join(DATA_DIR, "farmer_crops.csv")

try:
    CROP_PROFIT_DATA = pd.read_csv(CROP_PROFIT_CSV)
    crop_details_df = pd.read_csv(CROP_DETAILS_CSV)
    CROP_DETAILS = {row["Crop Name"]: {"description": row["Description"]} for idx, row in crop_details_df.iterrows()}
except Exception as e:  # <-- add this line to close the try-block!
    print(f"Warning: Error loading crop or details CSV: {e}")
    CROP_PROFIT_DATA = pd.DataFrame()
    CROP_DETAILS = {}

def ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(FARMER_CROPS_CSV):
        with open(FARMER_CROPS_CSV, "w", encoding="utf-8") as f:
            f.write("username,Crop Name,Field Size (acres),Profit Per Acre,Estimated Profit\n")
   

os.makedirs(DATA_DIR, exist_ok=True)

# ================= Helper Functions =================
def pause():
    input("\nPress Enter to continue... ")

def print_table(df: pd.DataFrame, headers="keys"):
    if df is None or df.empty:
        print("(no records)")
    else:
        print(tabulate(df, headers=headers, tablefmt="grid", showindex=False))

def display_available_crops():
    """Display available crops from database"""
    print("\n--- Available Crops in Database ---")
    for idx, row in CROP_PROFIT_DATA.iterrows():
        print(f"• {row['Crop Name']:<15} | Season: {row['Season']:<12} | Profit/Acre: ₹{row['Profit Per Acre']:,}")

# ================= Auth Functions =================
def register_user():
    users = load_users()
    print("\n=== User Registration ===")
    username = input("Choose a username: ").strip()
    if not users.empty and (users["username"] == username).any():
        print("Username already exists! Try another.")
        return
    
    name = input("Your full name: ").strip()
    password = getpass("Choose a password: ").strip()
    role = input("Enter role (admin/farmer): ").strip().lower()
    
    if role not in ["admin", "farmer"]:
        print("❌ Invalid role. Choose either 'admin' or 'farmer'.")
        return
    
    # Get contact for farmers
    contact = "N/A"
    if role == "farmer":
        while True:
            contact = input("Enter contact number (10 digits): ").strip()
            if len(contact) == 10 and contact.isdigit():
                break
            else:
                print("❌ Invalid contact number! Please enter exactly 10 digits.")
                retry = input("Try again? (yes/no): ").strip().lower()
                if retry != "yes":
                    print("Registration cancelled.")
                    return

    phash, salt = hash_password(password)
    user_id = next_id(users, "user_id")
    
    new_row = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "name": name,
        "password_hash": phash,
        "salt": salt
    }
    users = pd.concat([users, pd.DataFrame([new_row])], ignore_index=True)
    save_users(users)
    
    print(f"✅ {role.capitalize()} '{username}' registered successfully!")
    if role == "farmer":
        print(f"   Contact: {contact}")

def login():
    users = load_users()
    print("\n=== Login ===")
    username = input("Username: ").strip()
    password = getpass("Password: ").strip()
    
    if users.empty:
        print("No users found. Please register first.")
        return None
        
    row = users[users["username"] == username]
    if row.empty:
        print("User not found.")
        return None
        
    row = row.iloc[0]
    if verify_password(password, row["password_hash"], row["salt"]):
        print(f"✅ Welcome, {row['name']}! Role: {row['role']}")
        return {"user_id": int(row["user_id"]), "username": row["username"], "name": row["name"], "role": row["role"]}
    else:
        print("❌ Incorrect password.")
        return None

# ================= Crop Information Functions =================
def view_crop_information():
    """Interactive crop information viewer"""
    while True:
        print("\n" + "="*60)
        print("🌱 CROP INFORMATION DATABASE")
        print("="*60)
        print("\n--- Available Crops ---")
        
        available_crops = list(CROP_DETAILS.keys())
        for idx, crop_name in enumerate(available_crops, 1):
            profit_data = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"] == crop_name]
            if not profit_data.empty:
                profit = profit_data["Profit Per Acre"].values[0]
                season = profit_data["Season"].values[0]
                print(f"{idx:<2} {crop_name:<15} | Season: {season:<12} | Profit/Acre: ₹{profit:,}")
        
        print(f"\n{len(available_crops) + 1} Return to Dashboard")
        print("="*60)
        
        choice = input("\nEnter crop number to view detailed information (or return option): ").strip()
        
        if choice == str(len(available_crops) + 1):
            print("Returning to dashboard...\n")
            break
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_crops):
                selected_crop = available_crops[choice_num - 1]
                display_single_crop_details(selected_crop)
            else:
                print("❌ Invalid choice! Please select a valid number.")
        except ValueError:
            print("❌ Invalid input! Please enter a number.")

def display_single_crop_details(crop_name):
    """Display detailed information for a specific crop"""
    print("\n" + "="*70)
    print(f"📋 DETAILED INFORMATION: {crop_name.upper()}")
    print("="*70)
    
    profit_data = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"] == crop_name]
    if not profit_data.empty:
        profit_per_acre = profit_data.iloc[0]["Profit Per Acre"]
        season = profit_data.iloc[0]["Season"]
        
        print(f"\n💰 Expected Profit: ₹{profit_per_acre:,} per acre")
        print(f"🌦️  Best Season: {season}")
        print("\n" + "-"*70)
    
    if crop_name in CROP_DETAILS:
        description = CROP_DETAILS[crop_name]["description"]
        print(description)
    
    print("\n" + "="*70)
    input("\nPress Enter to continue...")

# ================= Farmer Management Functions =================
def view_my_crops(user):
    if not os.path.exists(FARMER_CROPS_CSV):
        print("No crop records found.")
        return
    df = pd.read_csv(FARMER_CROPS_CSV, dtype=str)
    my_crops = df[df["username"] == user["username"]]
    print("\n--- My Crops ---")
    print_table(my_crops)
    if my_crops.empty:
        print("No crops found for you.")


def register_farmer():
    print("\n--- Register Farmer ---")
    name = input("Enter farmer name: ").strip()
    
    farmers = load_farmers()
    if not farmers.empty and name in farmers["name"].values:
        print(f"⚠️ Farmer '{name}' already registered!")
        return
    
    while True:
        contact = input("Enter contact number (10 digits): ").strip()
        if len(contact) == 10 and contact.isdigit():
            break
        else:
            print("❌ Invalid contact number! Please enter exactly 10 digits.")
            retry = input("Try again? (yes/no): ").strip().lower()
            if retry != "yes":
                print("Registration cancelled.")
                return
    
    location = input("Enter location: ").strip()
    username = input("Enter associated username (optional): ").strip() or name.lower()
    
    farmer_id = next_id(farmers, "farmer_id")
    new_row = {
        "farmer_id": farmer_id,
        "username": username,
        "name": name,
        "location": location,
        "crop_grown": "",
        "quantity_quintal": "",
        "contact": contact
    }
    farmers = pd.concat([farmers, pd.DataFrame([new_row])], ignore_index=True)
    save_farmers(farmers)
    
    print(f"✅ Farmer '{name}' registered successfully!")
    print(f"   Contact: {contact}")
    print(f"   Location: {location}")

def view_farmers():
    farmers = load_farmers()
    if farmers.empty:
        print("No farmers registered yet.")
        return
    print("\n--- Registered Farmers ---")
    print_table(farmers)

def view_update_farmer_contact():
    """View or update farmer contact information"""
    print("\n--- Farmer Contact Management ---")
    
    farmers = load_farmers()
    if farmers.empty:
        print("No farmers registered yet.")
        return
    
    print("\n--- Registered Farmers ---")
    print_table(farmers)
    
    update = input("\nDo you want to update any contact? (yes/no): ").strip().lower()
    
    if update == "yes":
        farmer_name = input("Enter farmer name to update: ").strip()
        
        if farmer_name not in farmers["name"].values:
            print(f"❌ Farmer '{farmer_name}' not found!")
            return
        
        while True:
            new_contact = input("Enter new contact number (10 digits): ").strip()
            if len(new_contact) == 10 and new_contact.isdigit():
                break
            else:
                print("❌ Invalid contact number! Please enter exactly 10 digits.")
        
        farmers.loc[farmers["name"] == farmer_name, "contact"] = new_contact
        save_farmers(farmers)
        
        print(f"✅ Contact updated successfully for farmer '{farmer_name}'!")
        print(f"   New contact: {new_contact}")

# ================= Crop Management Functions =================
def add_crop_with_profit(user):
    print("\n--- Add Crop with Profit Calculation ---")
    display_available_crops()
    
    available_crops = CROP_PROFIT_DATA["Crop Name"].tolist()
    print(f"\nAvailable crop choices: {', '.join(available_crops)}")
    
    crop = input("\nEnter crop name from the list above: ").strip()
    crop_data = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"].str.lower() == crop.lower()]
    if crop_data.empty:
        print(f"❌ Crop '{crop}' not found in our database. Please choose from the available list.")
        return

    profit_per_acre = crop_data.iloc[0]["Profit Per Acre"]
    try:
        field_size = float(input("Enter field size (in acres): ").strip())
    except ValueError:
        print("❌ Invalid field size. Please enter a number.")
        return

    total_profit = profit_per_acre * field_size

    print("\n" + "="*50)
    print("💰 PROFIT CALCULATION")
    print("="*50)
    print(f"Crop Selected      : {crop}")
    print(f"Profit per Acre    : ₹{profit_per_acre:,.2f}")
    print(f"Field Size         : {field_size} acres")
    print(f"Estimated Profit   : ₹{total_profit:,.2f}")
    print("="*50)
    
    # Save farmer crop choice
    if not os.path.exists(FARMER_CROPS_CSV):
        with open(FARMER_CROPS_CSV, "w", encoding="utf-8") as f:
            f.write("username,Crop Name,Field Size (acres),Profit Per Acre,Estimated Profit\n")
    df = pd.read_csv(FARMER_CROPS_CSV, dtype=str)
    new_row = {
        "username": user["username"],
        "Crop Name": crop,
        "Field Size (acres)": field_size,
        "Profit Per Acre": profit_per_acre,
        "Estimated Profit": total_profit
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(FARMER_CROPS_CSV, index=False)
    
    print(f"\n✅ Crop '{crop}' added with profit calculation saved!")

def view_crops():
    crops = load_crops()
    if crops.empty:
        print("No crops found yet.")
        return

    print("\n--- Crop Records ---")
    print_table(crops)

def update_crop():
    crops = load_crops()
    if crops.empty:
        print("No crops to update.")
        return
        
    print_table(crops)
    cid = input("Enter crop_id to update: ").strip()
    
    if (crops["crop_id"].astype(str) == cid).any():
        idx = crops.index[crops["crop_id"].astype(str) == cid][0]
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
    if crops.empty:
        print("No crops to delete.")
        return
        
    print_table(crops)
    cid = input("Enter crop_id to delete: ").strip()
    
    if (crops["crop_id"].astype(str) == cid).any():
        crops = crops[crops["crop_id"].astype(str) != cid]
        save_crops(crops)
        print("Crop deleted.")
    else:
        print("Invalid crop_id.")

# ================= User Management Functions =================
def view_users():
    users = load_users()
    if users.empty:
        print("No users registered yet.")
        return
    print("\n--- Registered Users ---")
    # Hide password hash and salt for security
    display_df = users.drop(columns=["password_hash", "salt"], errors='ignore')
    print_table(display_df)

def update_user():
    users = load_users()
    if users.empty:
        print("No users to update.")
        return

    print("\n--- Update User ---")
    view_users()
    username = input("\nEnter username to update: ").strip()
    
    if username not in users["username"].values:
        print(f"❌ User '{username}' not found!")
        return
    
    idx = users.index[users["username"] == username][0]
    print("\nLeave blank to keep existing value.")

    new_username = input(f"Username [{users.at[idx, 'username']}]: ").strip()
    if new_username:
        if new_username in users["username"].values and new_username != users.at[idx, "username"]:
            print("❌ Username already exists!")
            return
        users.at[idx, "username"] = new_username

    new_password = input("Password [hidden]: ").strip()
    if new_password:
        phash, salt = hash_password(new_password)
        users.at[idx, "password_hash"] = phash
        users.at[idx, "salt"] = salt

    current_role = users.at[idx, "role"]
    new_role = input(f"Role [{current_role}]: ").strip()
    if new_role:
        if new_role.lower() not in ["admin", "farmer"]:
            print("❌ Invalid role.")
            return
        users.at[idx, "role"] = new_role

    new_name = input(f"Name [{users.at[idx, 'name']}]: ").strip()
    if new_name:
        users.at[idx, "name"] = new_name

    save_users(users)
    print(f"✅ User '{username}' updated successfully!")

def delete_user():
    users = load_users()
    if users.empty:
        print("No users to delete.")
        return

    print("\n--- Delete User ---")
    view_users()
    username = input("\nEnter username to delete: ").strip()
    
    if username not in users["username"].values:
        print(f"❌ User '{username}' not found!")
        return
        
    confirm = input(f"Are you sure you want to delete user '{username}'? (yes/no): ").strip().lower()
    
    if confirm == "yes":
        users = users[users["username"] != username]
        save_users(users)
        print(f"✅ User '{username}' deleted successfully!")
    else:
        print("Deletion cancelled.")

def user_management_menu():
    while True:
        print("\n=== User Management ===")
        print("1. View users")
        print("2. Update user")
        print("3. Delete user")
        print("0. Back to Admin Menu")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            view_users()
        elif choice == "2":
            update_user()
        elif choice == "3":
            delete_user()
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice!")
        pause()

# ================= Client/Farmer Functions =================
def upsert_my_record(user):
    farmers = load_farmers()
    mask = (farmers["username"] == user["username"])
    
    if not farmers.empty and mask.any():
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

# ================= Menu Functions =================
def admin_menu(user):
    while True:
        print(f"\n=== Admin Dashboard ({user['username']}) ===")
        print("1. Register Farmer")
        print("2. View Farmers")
        print("3. View/Update Farmer Contact")

        print("5. Add Crop with Profit Calculation")
        print("6. View Crop Information Database")

        print("8. Update Crop")
        print("9. Delete Crop")
        print("10. Manage Users")
        print("0. Logout")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            register_farmer()
        elif choice == "2":
            view_farmers()
        elif choice == "3":
            view_update_farmer_contact()

        elif choice == "5":
            add_crop_with_profit()
        elif choice == "6":
            view_crop_information()

        elif choice == "8":
            update_crop()
        elif choice == "9":
            delete_crop()
        elif choice == "10":
            user_management_menu()
        elif choice == "0":
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid choice!")
        pause()

def farmer_menu(user):
    while True:
        print(f"\n=== Farmer Dashboard ({user['username']}) ===")
        print("2. Add My Crop with Profit Calculation")
        print("3. Add/Update my crop record")
        print("4. Delete my crop record")
        print("5. View My Crops")
        print("6. Logout")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            view_crop_information()
        elif choice == "2":
            add_crop_with_profit(user)
        elif choice == "3":
            delete_my_record(user)
        elif choice == "4":
            upsert_my_record(user)
        elif choice == "5":
            view_my_crops(user)
        elif choice == "6":
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid choice!")
        pause()

# ================= Main Menu =================
def main():
    ensure_data_files()
    while True:
        print("\n=== 🌾 Crop Management Portal ===")
        print("1. Register User")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            user = login()
            if user:
                if user["role"] == "admin":
                    admin_menu(user)
                else:
                    farmer_menu(user)
        elif choice == "3":
            print("Exiting portal. Goodbye 👋")
            sys.exit()
        else:
            print("❌ Invalid choice! Try again.")

# ================= Run Program =================
if __name__ == "__main__":
    main()
