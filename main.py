"""
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
    main_menu()"""
#===============================================
import sys
import os
import pandas as pd

# ================= File Paths =================
DATA_DIR = "data"
FARMERS_FILE = os.path.join(DATA_DIR, "farmers.xlsx")
CROPS_FILE = os.path.join(DATA_DIR, "crops.xlsx")
USERS_FILE = os.path.join(DATA_DIR, "users.xlsx")
CROP_PROFIT_CSV = os.path.join(DATA_DIR, "crop_profit_data.csv")
CROP_DETAILS_CSV = os.path.join(DATA_DIR, "crop_details.csv")

CROP_PROFIT_DATA = pd.read_csv(CROP_PROFIT_CSV)
crop_details_df = pd.read_csv(CROP_DETAILS_CSV)
CROP_DETAILS = {row["Crop Name"]: {"description": row["Description"]} for idx, row in crop_details_df.iterrows()}

os.makedirs(DATA_DIR, exist_ok=True)



# ================= File Setup =================
if not os.path.exists(FARMERS_FILE):
    pd.DataFrame(columns=["Farmer Name", "Contact", "Location"]).to_excel(FARMERS_FILE, index=False)

if not os.path.exists(CROPS_FILE):
    pd.DataFrame(columns=["Farmer Name", "Crop Name", "Quantity", "Season", "Field Size (acres)", "Expected Profit"]).to_excel(CROPS_FILE, index=False)

if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["Username", "Password", "Role", "Contact"]).to_excel(USERS_FILE, index=False)


# ================= Functions =================
def view_crop_information():
    """Interactive crop information viewer"""
    while True:
        print("\n" + "="*60)
        print("🌱 CROP INFORMATION DATABASE")
        print("="*60)
        print("\n--- Available Crops ---")
        
        
        available_crops = list(CROP_DETAILS.keys())
        for idx, crop_name in enumerate(available_crops, 1):
            profit = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"] == crop_name]["Profit Per Acre"].values[0]
            season = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"] == crop_name]["Season"].values[0]
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

def view_update_farmer_contact():
    """View or update farmer contact information"""
    print("\n--- Farmer Contact Management ---")
    
    df = pd.read_excel(FARMERS_FILE)
    if df.empty:
        print("No farmers registered yet.")
        return
    
    
    print("\n--- Registered Farmers ---")
    for idx, row in df.iterrows():
        print(f"{idx + 1}. {row['Farmer Name']:<20} | Contact: {row['Contact']:<12} | Location: {row['Location']}")
    
    
    update = input("\nDo you want to update any contact? (yes/no): ").strip().lower()
    
    if update == "yes":
        farmer_name = input("Enter farmer name to update: ").strip()
        
        
        if farmer_name not in df["Farmer Name"].values:
            print(f"❌ Farmer '{farmer_name}' not found!")
            return
        
        
        while True:
            new_contact = input("Enter new contact number (10 digits): ").strip()
            
            if len(new_contact) == 10 and new_contact.isdigit():
                break
            else:
                print("❌ Invalid contact number! Please enter exactly 10 digits.")
        
        
        df.loc[df["Farmer Name"] == farmer_name, "Contact"] = new_contact
        df.to_excel(FARMERS_FILE, index=False)
        
        print(f"✅ Contact updated successfully for farmer '{farmer_name}'!")
        print(f"   New contact: {new_contact}")



def display_single_crop_details(crop_name):
    """Display detailed information for a specific crop"""
    print("\n" + "="*70)
    print(f"📋 DETAILED INFORMATION: {crop_name.upper()}")
    print("="*70)
    
    
    crop_profit_info = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"] == crop_name]
    profit_per_acre = crop_profit_info.iloc[0]["Profit Per Acre"]
    season = crop_profit_info.iloc[0]["Season"]
    
    print(f"\n💰 Expected Profit: ₹{profit_per_acre:,} per acre")
    print(f"🌦️  Best Season: {season}")
    print("\n" + "-"*70)
    
    
    description = CROP_DETAILS[crop_name]["description"]
    print(description)
    
    print("\n" + "="*70)
    
    
    input("\nPress Enter to continue...")


def add_crop_with_profit():
    print("\n--- Add Crop with Profit Calculation ---")
    farmer = input("Enter farmer name: ")
    
    
    df_farmers = pd.read_excel(FARMERS_FILE)
    if farmer not in df_farmers["Farmer Name"].values:
        print(f"❌ Farmer '{farmer}' not found! Please register first.")
        return
    
   
    display_available_crops()
    
    
    available_crops = CROP_PROFIT_DATA["Crop Name"].tolist()
    print(f"\nAvailable crop choices: {', '.join(available_crops)}")
    
    
    crop = input("\nEnter crop name from the list above: ").strip()
    
    
    crop_data = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"].str.lower() == crop.lower()]
    
    if crop_data.empty:
        print(f"❌ Crop '{crop}' not found in our database. Please choose from the available list.")
        return
    
    
    profit_per_acre = crop_data.iloc[0]["Profit Per Acre"]
    recommended_season = crop_data.iloc[0]["Season"]
    
    
    quantity = input("Enter quantity (kg): ").strip()
    season = input(f"Enter season (Recommended: {recommended_season}): ").strip()
    
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
    
    
    if season.lower() != recommended_season.lower():
        print(f"⚠️  Warning: Recommended season for {crop} is {recommended_season}")
    
    
    df_crops = pd.read_excel(CROPS_FILE)
    new_row = pd.DataFrame([{
        "Farmer Name": farmer,
        "Crop Name": crop,
        "Quantity": quantity,
        "Season": season,
        "Field Size (acres)": field_size,
        "Expected Profit": total_profit
    }])
    df_crops = pd.concat([df_crops, new_row], ignore_index=True)
    df_crops.to_excel(CROPS_FILE, index=False)
    
    print(f"\n✅ Crop '{crop}' added for farmer '{farmer}' with profit calculation saved!")

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
        
        new_user = pd.DataFrame([{"Username": username, "Password": password, "Role": role, "Contact": contact}])
    else:
        
        new_user = pd.DataFrame([{"Username": username, "Password": password, "Role": role, "Contact": "N/A"}])
    
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_excel(USERS_FILE, index=False)
    
    print(f"✅ {role.capitalize()} '{username}' registered successfully!")
    if role == "farmer":
        print(f"   Contact: {contact}")


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
    name = input("Enter farmer name: ").strip()
    
    
    df = pd.read_excel(FARMERS_FILE)
    if name in df["Farmer Name"].values:
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
    
    
    new_row = pd.DataFrame([{"Farmer Name": name, "Contact": contact, "Location": location}])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(FARMERS_FILE, index=False)
    
    print(f"✅ Farmer '{name}' registered successfully!")
    print(f"   Contact: {contact}")
    print(f"   Location: {location}")



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
        print("3. View/Update Farmer Contact")  
        print("4. Add Crop (Simple)")
        print("5. Add Crop with Profit Calculation")
        print("6. View Crop Information Database")
        print("7. View Crops")
        print("8. Logout")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            register_farmer()
        elif choice == "2":
            view_farmers()
        elif choice == "3":
            view_update_farmer_contact() 
        elif choice == "4":
            add_crop()
        elif choice == "5":
            add_crop_with_profit()
        elif choice == "6":
            view_crop_information()
        elif choice == "7":
            view_crops()
        elif choice == "8":
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid choice!")


def farmer_menu(username):
    while True:
        print(f"\n=== Farmer Dashboard ({username}) ===")
        print("1. Add My Crop (Simple)")
        print("2. Add My Crop with Profit Calculation")
        print("3. View Crop Information Database")  
        print("4. View My Crops")
        print("5. Logout")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            add_crop()
        elif choice == "2":
            add_crop_with_profit()
        elif choice == "3":
            view_crop_information()  
        elif choice == "4":
            df = pd.read_excel(CROPS_FILE)
            crops = df[df["Farmer Name"].str.lower() == username.lower()]
            if crops.empty:
                print("No crops found for you.")
            else:
                print(crops.to_string(index=False))
        elif choice == "5":
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
