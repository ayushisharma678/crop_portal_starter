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
