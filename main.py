<<<<<<< HEAD
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
import pandas as pd
import os

# ----------------- File paths -----------------
DATA_DIR = "data"
FARMERS_FILE = os.path.join(DATA_DIR, "farmers.xlsx")
CROPS_FILE = os.path.join(DATA_DIR, "crops.xlsx")
USERS_FILE = os.path.join(DATA_DIR, "users.xlsx")

# ----------------- Ensure files exist -----------------
os.makedirs(DATA_DIR, exist_ok=True)

if not os.path.exists(FARMERS_FILE):
    pd.DataFrame(columns=["Farmer Name", "Contact", "Location"]).to_excel(FARMERS_FILE, index=False)

if not os.path.exists(CROPS_FILE):
    pd.DataFrame(columns=["Farmer Name", "Crop Name", "Quantity", "Season"]).to_excel(CROPS_FILE, index=False)

if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["Username", "Role"]).to_excel(USERS_FILE, index=False)

# ----------------- Utility -----------------
def pause():
    input("\nPress Enter to continue...")

def read_excel(file_path):
    return pd.read_excel(file_path)

def write_excel(df, file_path):
    df.to_excel(file_path, index=False)

def print_table(df):
    if df.empty:
        print("(no records)")
        return
    print(df.to_string(index=False))

# ----------------- Farmer CRUD -----------------
def register_farmer():
    name = input("Enter farmer name: ").strip()
    contact = input("Enter contact number: ").strip()
    location = input("Enter location: ").strip()

    df = read_excel(FARMERS_FILE)
    df = pd.concat([df, pd.DataFrame([{
        "Farmer Name": name,
        "Contact": contact,
        "Location": location
    }])], ignore_index=True)
    write_excel(df, FARMERS_FILE)
    print(f"✅ Farmer '{name}' registered successfully!")

def view_farmers():
    df = read_excel(FARMERS_FILE)
    print("\n--- Farmer Records ---")
    print_table(df)

def update_farmer():
    df = read_excel(FARMERS_FILE)
    print_table(df)
    name = input("Enter the Farmer Name to update: ").strip()
    if name not in df["Farmer Name"].values:
        print("❌ Farmer not found!")
        return
    idx = df.index[df["Farmer Name"] == name][0]
    for col in ["Farmer Name", "Contact", "Location"]:
        val = input(f"{col} [{df.at[idx,col]}]: ").strip()
        if val:
            df.at[idx,col] = val
    write_excel(df, FARMERS_FILE)
    print("✅ Farmer updated successfully!")

def delete_farmer():
    df = read_excel(FARMERS_FILE)
    print_table(df)
    name = input("Enter the Farmer Name to delete: ").strip()
    if name not in df["Farmer Name"].values:
        print("❌ Farmer not found!")
        return
    df = df[df["Farmer Name"] != name]
    write_excel(df, FARMERS_FILE)
    print("✅ Farmer deleted successfully!")

# ----------------- Crop CRUD -----------------
def add_crop():
    df_farmers = read_excel(FARMERS_FILE)
    farmer = input("Enter farmer name: ").strip()
    if farmer not in df_farmers["Farmer Name"].values:
        print("❌ Farmer not found! Register first.")
        return
    crop = input("Enter crop name: ").strip()
    qty = input("Enter quantity (kg): ").strip()
    season = input("Enter season: ").strip()
    df = read_excel(CROPS_FILE)
    df = pd.concat([df, pd.DataFrame([{
        "Farmer Name": farmer,
        "Crop Name": crop,
        "Quantity": qty,
        "Season": season
    }])], ignore_index=True)
    write_excel(df, CROPS_FILE)
    print(f"✅ Crop '{crop}' added for farmer '{farmer}'")

def view_crops():
    df = read_excel(CROPS_FILE)
    print("\n--- Crop Records ---")
    print_table(df)

def update_crop():
    df = read_excel(CROPS_FILE)
    print_table(df)
    crop_name = input("Enter Crop Name to update: ").strip()
    farmer = input("Enter Farmer Name for this crop: ").strip()
    mask = (df["Crop Name"] == crop_name) & (df["Farmer Name"] == farmer)
    if not mask.any():
        print("❌ Crop record not found!")
        return
    idx = df.index[mask][0]
    for col in ["Crop Name", "Quantity", "Season"]:
        val = input(f"{col} [{df.at[idx,col]}]: ").strip()
        if val:
            df.at[idx,col] = val
    write_excel(df, CROPS_FILE)
    print("✅ Crop record updated!")

def delete_crop():
    df = read_excel(CROPS_FILE)
    print_table(df)
    crop_name = input("Enter Crop Name to delete: ").strip()
    farmer = input("Enter Farmer Name for this crop: ").strip()
    mask = (df["Crop Name"] == crop_name) & (df["Farmer Name"] == farmer)
    if not mask.any():
        print("❌ Crop record not found!")
        return
    df = df[~mask]
    write_excel(df, CROPS_FILE)
    print("✅ Crop record deleted!")

# ----------------- Main Menu -----------------
def main_menu():
    while True:
        print("\n=== Crop Management Portal ===")
        print("1. Register Farmer")
        print("2. View Farmers")
        print("3. Update Farmer")
        print("4. Delete Farmer")
        print("5. Add Crop")
        print("6. View Crops")
        print("7. Update Crop")
        print("8. Delete Crop")
        print("9. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            register_farmer()
        elif choice == "2":
            view_farmers()
        elif choice == "3":
            update_farmer()
        elif choice == "4":
            delete_farmer()
        elif choice == "5":
            add_crop()
        elif choice == "6":
            view_crops()
        elif choice == "7":
            update_crop()
        elif choice == "8":
            delete_crop()
        elif choice == "9":
            print("Exiting portal. Goodbye 👋")
            sys.exit()
        else:
            print("❌ Invalid choice! Try again.")
        pause()

if __name__ == "__main__":
    main_menu()
>>>>>>> 4c27f91 (Initial commit)
