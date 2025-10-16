
import sys
import pandas as pd
import os

# File paths
FARMERS_FILE = "data/farmers.xlsx"
CROPS_FILE = "data/crops.xlsx"
USERS_FILE = "data/users.xlsx"

# Ensure files exist
if not os.path.exists(FARMERS_FILE):
    pd.DataFrame(columns=["Farmer Name", "Contact", "Location"]).to_excel(FARMERS_FILE, index=False)

if not os.path.exists(CROPS_FILE):
    pd.DataFrame(columns=["Farmer Name", "Crop Name", "Quantity", "Season"]).to_excel(CROPS_FILE, index=False)

if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["Username", "Role"]).to_excel(USERS_FILE, index=False)


# ================= Functions =================

def register_farmer():
    name = input("Enter farmer name: ")
    contact = input("Enter contact number: ")
    location = input("Enter location: ")

    df = pd.read_excel(FARMERS_FILE)
    new_row = pd.DataFrame([{"Farmer Name": name, "Contact": contact, "Location": location}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(FARMERS_FILE, index=False)

    print(f"✅ Farmer '{name}' registered successfully!")

def add_crop():
    farmer = input("Enter farmer name: ")

    df_farmers = pd.read_excel(FARMERS_FILE)
    if farmer not in df_farmers["Farmer Name"].values:
        print(f"❌ Farmer '{farmer}' not found! Please register first.")
        return

    crop = input("Enter crop name: ")
    quantity = input("Enter quantity (kg): ")
    season = input("Enter season: ")

    df_crops = pd.read_excel(CROPS_FILE)
    new_row = pd.DataFrame([{
        "Farmer Name": farmer,
        "Crop Name": crop,
        "Quantity": quantity,
        "Season": season
    }])
    df_crops = pd.concat([df_crops, new_row], ignore_index=True)
    df_crops.to_excel(CROPS_FILE, index=False)

    print(f"✅ Crop '{crop}' added for farmer '{farmer}'")

def view_crops():
    df_crops = pd.read_excel(CROPS_FILE)
    if df_crops.empty:
        print("No crops found yet.")
        return

    print("\n--- Crop Records ---")
    for i, row in df_crops.iterrows():
        print(f"Farmer: {row['Farmer Name']}, Crop: {row['Crop Name']}, Quantity: {row['Quantity']} kg, Season: {row['Season']}")


# ================= Main Menu =================

def main_menu():
    while True:
        print("\n=== Crop Management Portal ===")
        print("1. Register Farmer")
        print("2. Add Crop")
        print("3. View Crops")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_farmer()
        elif choice == "2":
            add_crop()
        elif choice == "3":
            view_crops()
        elif choice == "4":
            print("Exiting portal. Goodbye 👋")
            sys.exit()
        else:
            print("❌ Invalid choice! Try again.")


# ================= Run Program =================
if __name__ == "__main__":
    main_menu()
=======
import sys
import os
import pandas as pd

# ================= File Paths =================
DATA_DIR = "data"
FARMERS_FILE = os.path.join(DATA_DIR, "farmers.xlsx")
CROPS_FILE = os.path.join(DATA_DIR, "crops.xlsx")
USERS_FILE = os.path.join(DATA_DIR, "users.xlsx")

os.makedirs(DATA_DIR, exist_ok=True)

# ================= File Setup =================
if not os.path.exists(FARMERS_FILE):
    pd.DataFrame(columns=["Farmer Name", "Contact", "Location"]).to_excel(FARMERS_FILE, index=False)

if not os.path.exists(CROPS_FILE):
    pd.DataFrame(columns=["Farmer Name", "Crop Name", "Quantity", "Season"]).to_excel(CROPS_FILE, index=False)

if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["Username", "Password", "Role"]).to_excel(USERS_FILE, index=False)

# ================= Functions =================

def register_user():
    print("\n--- Register New User ---")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    role = input("Enter role (admin/farmer): ").strip().lower()

    if role not in ["admin", "farmer"]:
        print("❌ Invalid role. Choose either 'admin' or 'farmer'.")
        return

    df = pd.read_excel(USERS_FILE)

    if username in df["Username"].values:
        print("⚠️ Username already exists. Try another one.")
        return

    new_user = pd.DataFrame([{"Username": username, "Password": password, "Role": role}])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_excel(USERS_FILE, index=False)

    print(f"✅ {role.capitalize()} '{username}' registered successfully!")


def login():
    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    df = pd.read_excel(USERS_FILE)

    user = df[(df["Username"] == username) & (df["Password"] == password)]

    if not user.empty:
        role = user.iloc[0]["Role"]
        print(f"\n✅ Login successful! Welcome, {username} ({role})")
        if role == "admin":
            admin_menu(username)
        else:
            farmer_menu(username)
    else:
        print("❌ Invalid credentials. Try again.")


# ================= CRUD: Farmers =================

def register_farmer():
    print("\n--- Register Farmer ---")
    name = input("Enter farmer name: ")
    contact = input("Enter contact number: ")
    location = input("Enter location: ")

    df = pd.read_excel(FARMERS_FILE)
    new_row = pd.DataFrame([{"Farmer Name": name, "Contact": contact, "Location": location}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(FARMERS_FILE, index=False)

    print(f"✅ Farmer '{name}' registered successfully!")


def view_farmers():
    df = pd.read_excel(FARMERS_FILE)
    if df.empty:
        print("No farmers registered yet.")
        return
    print("\n--- Registered Farmers ---")
    print(df.to_string(index=False))


# ================= CRUD: Crops =================

def add_crop():
    print("\n--- Add Crop ---")
    farmer = input("Enter farmer name: ")

    df_farmers = pd.read_excel(FARMERS_FILE)
    if farmer not in df_farmers["Farmer Name"].values:
        print(f"❌ Farmer '{farmer}' not found! Please register first.")
        return

    crop = input("Enter crop name: ")
    quantity = input("Enter quantity (kg): ")
    season = input("Enter season: ")

    df_crops = pd.read_excel(CROPS_FILE)
    new_row = pd.DataFrame([{
        "Farmer Name": farmer,
        "Crop Name": crop,
        "Quantity": quantity,
        "Season": season
    }])
    df_crops = pd.concat([df_crops, new_row], ignore_index=True)
    df_crops.to_excel(CROPS_FILE, index=False)

    print(f"✅ Crop '{crop}' added for farmer '{farmer}'")


def view_crops():
    df_crops = pd.read_excel(CROPS_FILE)
    if df_crops.empty:
        print("No crops found yet.")
        return

    print("\n--- Crop Records ---")
    print(df_crops.to_string(index=False))


# ================= Menus =================

def admin_menu(username):
    while True:
        print(f"\n=== Admin Dashboard ({username}) ===")
        print("1. Register Farmer")
        print("2. View Farmers")
        print("3. Add Crop")
        print("4. View Crops")
        print("5. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_farmer()
        elif choice == "2":
            view_farmers()
        elif choice == "3":
            add_crop()
        elif choice == "4":
            view_crops()
        elif choice == "5":
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid choice!")


def farmer_menu(username):
    while True:
        print(f"\n=== Farmer Dashboard ({username}) ===")
        print("1. Add My Crop")
        print("2. View My Crops")
        print("3. Logout")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_crop()
        elif choice == "2":
            df = pd.read_excel(CROPS_FILE)
            crops = df[df["Farmer Name"].str.lower() == username.lower()]
            if crops.empty:
                print("No crops found for you.")
            else:
                print(crops.to_string(index=False))
        elif choice == "3":
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid choice!")


# ================= Main Menu =================

def main_menu():
    while True:
        print("\n=== 🌾 Crop Management Portal ===")
        print("1. Register User")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting portal. Goodbye 👋")
            sys.exit()
        else:
            print("❌ Invalid choice! Try again.")


# ================= Run Program =================
if __name__ == "__main__":
    main_menu()


#fb57263 (Updated crop and user data files + modified main.py)
