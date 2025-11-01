#===============================================
import sys
import os
import pandas as pd
import re
from tabulate import tabulate
from getpass import getpass

from storage import (
    DATA_DIR,
    load_users, save_users,
    load_crops, load_farmers, save_farmers,
    next_id, ensure_data_files
)
from security import hash_password, verify_password

# ================= File Paths =================
CROP_PROFIT_CSV = os.path.join(DATA_DIR, "crop_profit_data.csv")
CROP_DETAILS_CSV = os.path.join(DATA_DIR, "crop_details.csv")
FARMER_CROPS_CSV = os.path.join(DATA_DIR, "farmer_crops.csv")

#-------------Load Data---------------
try:
    CROP_PROFIT_DATA = pd.read_csv(CROP_PROFIT_CSV)
    crop_details_df = pd.read_csv(CROP_DETAILS_CSV)
    CROP_DETAILS = {row["Crop Name"]: {"description": row["Description"]} for idx, row in crop_details_df.iterrows()}
except Exception as e:  
    print(f"Warning: Error loading crop or details CSV: {e}")
    CROP_PROFIT_DATA = pd.DataFrame()
    CROP_DETAILS = {}

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

# ================= Password Validation =================
def is_valid_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(pattern, password)

# ================= Auth Functions =================
def register_user():
    users = load_users()
    print("\n=== User Registration ===")
    username = input("Choose a username: ").strip()
    if not users.empty and (users["username"] == username).any():
        print("Username already exists! Try another.")
        return
    
    name = input("Your full name: ").strip()
    if not name or len(name) < 2:
        print("❌ Please enter a valid name (at least 2 characters).")
        return

    while True:
        password = getpass("Choose a password: ").strip()
        if not is_valid_password(password):
            print("Password must have at least 1 uppercase, 1 lowercase, 1 digit, 1 special char, min 8 chars")
        else:
            break
            
    role = input("Enter role (admin/farmer): ").strip().lower()
    if role not in ["admin", "farmer"]:
        print("❌ Invalid role. Choose either 'admin' or 'farmer'.")
        return

    contact, location = "N/A", "N/A"
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
        location = input("Enter your location: ").strip()

    phash, salt = hash_password(password)
    user_id = next_id(users, "user_id")
    new_user_row = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "name": name,
        "password_hash": phash,
        "salt": salt
    }
    users = pd.concat([users, pd.DataFrame([new_user_row])], ignore_index=True)
    save_users(users)
    
    if role == "farmer":
        farmers = load_farmers()
        farmer_id = next_id(farmers, "farmer_id")
        new_farmer_row = {
            "farmer_id": farmer_id,
            "username": username,
            "name": name,
            "location": location,
            "contact": contact
        }
        farmers = pd.concat([farmers, pd.DataFrame([new_farmer_row])], ignore_index=True)
        save_farmers(farmers)
        print(f"✅ Farmer '{name}' registered successfully!")
        print(f"   Contact: {contact}")
        print(f"   Location: {location}")
    else:
        print(f"✅ Admin '{username}' registered successfully!")


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
def print_clean_farmers(df):
    available_farmers = df.reset_index(drop=True)
    print("\n--- Registered Farmers ---")
    print(f"{'No.':<3} {'ID':<5} {'Name':<16} {'User':<12} {'Location':<18} {'Contact':<12}")
    print("-" * 85)
    for idx, row in available_farmers.iterrows():
        print(f"{idx+1:<3} "
              f"{str(row['farmer_id']):<5} "
              f"{str(row['name'])[:15]:<16} "
              f"{str(row['username'])[:12]:<12} "
              f"{str(row['location'])[:17]:<18} "
              f"{str(row['contact'])[:12]:<12}"
        )

def view_crop_information():
    """Interactive crop information viewer"""
    while True:
        print("\n" + "="*60)
        print("🌱 CROP INFORMATION DATABASE")
        print("="*60)
        print("\n--- Available Crops ---")
        
        available_crops = CROP_PROFIT_DATA["Crop Name"].tolist()
        
        for idx, crop_name in enumerate(available_crops, 1):
            profit_data = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"] == crop_name]
            if not profit_data.empty:
                profit = profit_data["Profit Per Acre"].values[0]
                season = profit_data["Season"].values[0]
                print(f"{idx:<2} {crop_name:<15} | Season: {season:<12} | Profit/Acre: ₹{profit:,}")
        
        print(f"\n0. Return to Dashboard")  
        print("="*60)
        choice = input("\nEnter crop number to view detailed information (or 0 to return): ").strip()  
        if choice == "0":  
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



# ================= Search & Filter Crops =================
def search_and_filter_crops():
    """Search crops by season and profit range, then view details"""
    if CROP_PROFIT_DATA.empty:
        print("No crop data available.")
        return

    print("\n--- Search & Filter Crops ---")
    
    season_input = input("Enter season to filter (Kharif/Rabi/Year-round or leave blank for all): ").strip().capitalize()
    filtered_df = CROP_PROFIT_DATA.copy()
    if season_input:
        filtered_df = filtered_df[filtered_df["Season"] == season_input]
    
    min_profit_input = input("Enter minimum profit per acre (or leave blank for no minimum): ").strip()
    if min_profit_input:
        try:
            min_profit = float(min_profit_input)
            filtered_df = filtered_df[filtered_df["Profit Per Acre"] >= min_profit]
        except ValueError:
            print("Invalid input. Ignoring minimum profit filter.")
    
    max_profit_input = input("Enter maximum profit per acre (or leave blank for no maximum): ").strip()
    if max_profit_input:
        try:
            max_profit = float(max_profit_input)
            filtered_df = filtered_df[filtered_df["Profit Per Acre"] <= max_profit]
        except ValueError:
            print("Invalid input. Ignoring maximum profit filter.")
    
    if filtered_df.empty:
        print("No crops match your filter criteria.")
        return
    
    filtered_df = filtered_df.reset_index(drop=True)
    
    print("\n--- Filtered Crops ---")
    for idx, row in filtered_df.iterrows():
        print(f"{idx+1}. {row['Crop Name']:<15} | Season: {row['Season']:<12} | Profit/Acre: ₹{row['Profit Per Acre']:,}")

    choice = input("\nEnter crop number to view details or 'q' to quit: ").strip()
    if choice.lower() == 'q':
        return
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(filtered_df):
            selected_crop = filtered_df.iloc[choice_num - 1]["Crop Name"]
            display_single_crop_details(selected_crop)
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")



# ================= Export Reports Enhancement =================
def export_farmer_crops():
    if os.path.exists(FARMER_CROPS_CSV):
        df = pd.read_csv(FARMER_CROPS_CSV)
        export_file = os.path.join(DATA_DIR, "farmer_crops_export.xlsx")
        df.to_excel(export_file, index=False)
        print(f"✅ Farmer crops exported to {export_file}")
    else:
        print("No crop records to export.")

# ================= Profit Summary Dashboard Enhancement =================
def profit_summary_dashboard():
    if os.path.exists(FARMER_CROPS_CSV):
        df = pd.read_csv(FARMER_CROPS_CSV)
        summary = df.groupby("username")["Estimated Profit"].sum().reset_index()
        total_portal_profit = summary["Estimated Profit"].sum()
        print("\n--- Profit Summary per Farmer ---")
        print_table(summary)
        print(f"Total Portal Expected Profit: ₹{total_portal_profit:,.2f}")
    else:
        print("No crops to summarize.")


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
    
    df = pd.read_csv(FARMER_CROPS_CSV) 
    df['username'] = df['username'].astype(str)
    my_crops = df[df["username"] == user["username"]]
    
    print("\n--- My Crops ---")
    if my_crops.empty:
        print("No crops found for you.")
    else:
        print_table(my_crops)

        try:
            my_crops['Estimated Profit'] = pd.to_numeric(my_crops['Estimated Profit'], errors='coerce')
            total = my_crops['Estimated Profit'].sum()
            print(f"\n💰 Total Expected Profit: ₹{total:,.2f}")
        except Exception:
            pass



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
    print_clean_farmers(farmers)



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
def update_crop_profit_data_only():
    """Update crop profit data with neat column formatting"""
    global CROP_PROFIT_DATA
    
    if CROP_PROFIT_DATA.empty:
        print("No crop profit data available.")
        return

    print("\n" + "="*80)
    print("📊 UPDATE CROP PROFIT DATA")
    print("="*80)
    print()
    print(f"{'No.':<4} {'Crop Name':<20} {'Season':<15} {'Current Profit/Acre':<20}")
    print("-"*80)
    for idx, row in CROP_PROFIT_DATA.iterrows():
        crop_name = str(row['Crop Name'])[:19]  
        season = str(row['Season'])[:14]
        profit = f"₹{row['Profit Per Acre']:,.2f}"
        
        print(f"{idx+1:<4} {crop_name:<20} {season:<15} {profit:<20}")
    
    print("-"*80)
    print()
    try:
        sel = int(input("Enter crop number to update profit: ").strip())
        if sel < 1 or sel > len(CROP_PROFIT_DATA):
            print("❌ Invalid crop number.")
            return
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        return
    new_profit = input("Enter NEW Profit Per Acre (₹): ").strip()
    try:
        profit_value = float(new_profit)
        if profit_value < 0:
            print("❌ Profit cannot be negative!")
            return
    except ValueError:
        print("❌ Invalid number. Please enter a valid amount.")
        return
    crop_name = CROP_PROFIT_DATA.iloc[sel-1]["Crop Name"]
    old_profit = CROP_PROFIT_DATA.iloc[sel-1]["Profit Per Acre"]
    
    CROP_PROFIT_DATA.loc[CROP_PROFIT_DATA["Crop Name"] == crop_name, "Profit Per Acre"] = profit_value
    CROP_PROFIT_DATA.to_csv(CROP_PROFIT_CSV, index=False)
    CROP_PROFIT_DATA = pd.read_csv(CROP_PROFIT_CSV)

    print()
    print("="*80)
    print(f"✅ Profit updated successfully for '{crop_name}'!")
    print("="*80)
    print(f"  Old Profit: ₹{old_profit:,.2f}/acre")
    print(f"  New Profit: ₹{profit_value:,.2f}/acre")

    change_amount = profit_value - old_profit
    if old_profit != 0:
        change_percent = (change_amount / old_profit * 100)
        print(f"  Change:     ₹{change_amount:+,.2f}/acre ({change_percent:+.1f}%)")
    else:
        print(f"  Change:     ₹{change_amount:+,.2f}/acre (New entry)")
    print("="*80)



def update_farmer():
    farmers = load_farmers()
    if farmers.empty:
        print("No farmers to update.")
        return
    print_clean_farmers(farmers)
    fid = input("Enter farmer_id to update: ").strip()
    if (farmers["farmer_id"].astype(str) == fid).any():
        idx = farmers.index[farmers["farmer_id"].astype(str) == fid][0]
        print("Leave blank to keep existing value.")
        for field in ["username", "name", "location", "contact"]:
            cur = farmers.at[idx, field]
            val = input(f"{field} [{cur}]: ").strip()
            if val:
                farmers.at[idx, field] = val
        save_farmers(farmers)
        print("Farmer updated.")
    else:
        print("Invalid farmer_id.")

def delete_farmer():
    farmers = load_farmers()
    if farmers.empty:
        print("No farmers to delete.")
        return
    print_table(farmers)
    fid = input("Enter farmer_id to delete: ").strip()
    if (farmers["farmer_id"].astype(str) == fid).any():
        farmers = farmers[farmers["farmer_id"].astype(str) != fid]
        save_farmers(farmers)
        print("Farmer deleted.")
    else:
        print("Invalid farmer_id.")

def add_crop_with_profit(user):
    print("\n--- Add Crop with Profit Calculation ---")
    display_available_crops()
    
    available_crops = CROP_PROFIT_DATA["Crop Name"].tolist()
    print(f"\nAvailable crop choices: {', '.join(available_crops)}")
    
    crop = input("\nEnter crop name from the list above: ").strip()
    crop_data = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"].astype(str).str.lower() == crop.lower()]
    if crop_data.empty:
        print(f"❌ Crop '{crop}' not found in our database. Please choose from the available list.")
        return

    profit_per_acre = crop_data.iloc[0]["Profit Per Acre"]
    try:
        field_size = float(input("Enter field size (in acres): ").strip())
        if field_size <= 0:
            print("❌ Field size must be greater than 0!")
            return
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
    
  
    if not os.path.exists(FARMER_CROPS_CSV):
        with open(FARMER_CROPS_CSV, "w", encoding="utf-8") as f:
            f.write("username,Crop Name,Field Size (acres),Profit Per Acre,Estimated Profit\n")
    df = pd.read_csv(FARMER_CROPS_CSV)
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

<<<<<<< HEAD
def add_crop_record():
    """Admin: Add a new crop record directly to crop_details.csv and crop_profit_data.csv"""
    print("\n--- Add New Crop Record ---")

  
    try:
        crop_details = pd.read_csv(CROP_DETAILS_CSV)
    except FileNotFoundError:
        crop_details = pd.DataFrame(columns=["Crop Name", "Description"])

    try:
        crop_profit = pd.read_csv(CROP_PROFIT_CSV)
    except FileNotFoundError:
        crop_profit = pd.DataFrame(columns=["Crop Name", "Profit Per Acre", "Season"])

    crop_name = input("Crop Name: ").strip()
    description = input("Description: ").strip()

    while True:
        profit_per_acre = input("Profit Per Acre: ").strip()
        try:
            profit_per_acre = float(profit_per_acre)
            break
        except ValueError:
            print("❌ Invalid value! Enter a number for Profit Per Acre.")

    season = input("Season: ").strip()

 
    new_details = {"Crop Name": crop_name, "Description": description}
    crop_details = pd.concat([crop_details, pd.DataFrame([new_details])], ignore_index=True)

    new_profit = {"Crop Name": crop_name, "Profit Per Acre": profit_per_acre, "Season": season}
    crop_profit = pd.concat([crop_profit, pd.DataFrame([new_profit])], ignore_index=True)

    crop_details.to_csv(CROP_DETAILS_CSV, index=False)
    crop_profit.to_csv(CROP_PROFIT_CSV, index=False)

    print(f"✅ Crop '{crop_name}' added successfully!")


def update_crop():
    """Admin: Update an existing crop record in crop_details.csv and crop_profit_data.csv"""
    try:
        crop_details = pd.read_csv(CROP_DETAILS_CSV)
    except FileNotFoundError:
        print("❌ No crop details found.")
        return

    try:
        crop_profit = pd.read_csv(CROP_PROFIT_CSV)
    except FileNotFoundError:
        print("❌ No crop profit data found.")
        return

    print("\n--- Existing Crops ---")
    for idx, row in crop_details.iterrows():
        print(f"{idx+1}: {row['Crop Name']} | {row['Description'][:30]}...")

    choice = input("Enter crop number to update: ").strip()
    try:
        choice_idx = int(choice) - 1
        if choice_idx < 0 or choice_idx >= len(crop_details):
            print("❌ Invalid choice!")
            return
    except ValueError:
        print("❌ Invalid input!")
        return

    crop_name_old = crop_details.at[choice_idx, "Crop Name"]

    cur_desc = crop_details.at[choice_idx, "Description"]
    desc = input(f"Description [{cur_desc}]: ").strip()
    if desc:
        crop_details.at[choice_idx, "Description"] = desc

    profit_idx = crop_profit.index[crop_profit["Crop Name"] == crop_name_old][0]
    cur_profit = crop_profit.at[profit_idx, "Profit Per Acre"]
    cur_season = crop_profit.at[profit_idx, "Season"]

    val_profit = input(f"Profit Per Acre [{cur_profit}]: ").strip()
    if val_profit:
        try:
            val_profit = float(val_profit)
            crop_profit.at[profit_idx, "Profit Per Acre"] = val_profit
        except ValueError:
            print("❌ Invalid number! Profit not updated.")

    val_season = input(f"Season [{cur_season}]: ").strip()
    if val_season:
        crop_profit.at[profit_idx, "Season"] = val_season

    crop_details.to_csv(CROP_DETAILS_CSV, index=False)
    crop_profit.to_csv(CROP_PROFIT_CSV, index=False)

    print(f"✅ Crop '{crop_details.at[choice_idx, 'Crop Name']}' updated successfully!")


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

=======
def save_crop_files(crops_df):
    """Save crops to both crop_details and crop_profit CSVs."""
    global CROP_PROFIT_DATA 
    crops_df.to_csv(CROP_DETAILS_CSV, index=False)
    profit_cols = ["crop_id", "crop_name", "price_per_quintal"]
    if all(col in crops_df.columns for col in profit_cols):
        CROP_PROFIT_DATA = crops_df[profit_cols].copy()
        CROP_PROFIT_DATA.to_csv(CROP_PROFIT_CSV, index=False)
    else:
        print("⚠️ Some columns missing for profit CSV. Skipping profit update.")

>>>>>>> 514730fdf167a65a8ca4ba0a0f55f69982400934
# ================= User Management Functions =================
def view_users():
    users = load_users()
    if users.empty:
        print("No users registered yet.")
        return
    print("\n--- Registered Users ---")
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
        for field in ["name", "location", "contact"]:
            cur = farmers.at[idx, field]
            if field == "contact":
                while True:
                    val = input(f"{field} [{cur}]: ").strip()
                    if not val or (len(val) == 10 and val.isdigit()):
                        break
                    print("❌ Invalid! Enter 10 digits.")
            else:
                val = input(f"{field} [{cur}]: ").strip()
            if val:
                farmers.at[idx, field] = val



    else:
        print("Creating your crop record.")
        name = input("Full name: ").strip() or user["name"]
        location = input("Location: ").strip()
        while True:
            contact = input("Contact (10 digits): ").strip()
            if len(contact) == 10 and contact.isdigit():
                break
            print("❌ Invalid contact number! Please enter exactly 10 digits.")

        farmer_id = next_id(farmers, "farmer_id")
        new_row = {
            "farmer_id": farmer_id,
            "username": user["username"],
            "name": name,
            "location": location,
            "contact": contact
        }
        farmers = pd.concat([farmers, pd.DataFrame([new_row])], ignore_index=True)
    
    save_farmers(farmers)
    print("Saved!")

def delete_my_account(user):
    """Delete the user's account and related data"""
    confirm = input("\n⚠️ Are you sure you want to delete your account permanently? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        return

    users = load_users()
    users = users[users["username"] != user["username"]]
    save_users(users)

    farmers = load_farmers()
    farmers = farmers[farmers["username"] != user["username"]]
    save_farmers(farmers)

    if os.path.exists(FARMER_CROPS_CSV):
        df = pd.read_csv(FARMER_CROPS_CSV)
        df = df[df["username"] != user["username"]]
        df.to_csv(FARMER_CROPS_CSV, index=False)

    print("✅ Your account and all associated data have been deleted. Logging out...")
    sys.exit()

def delete_my_record(user):
    if not os.path.exists(FARMER_CROPS_CSV):
        print("No crop records found.")
        return
    df = pd.read_csv(FARMER_CROPS_CSV)
    df['username'] = df['username'].astype(str)
    my_crops = df[df["username"] == user["username"]]
    if my_crops.empty:
        print("No crops found for you.")
        return
    print("\n--- Your Crops ---")
    my_crops = my_crops.reset_index(drop=True)
    for i, row in my_crops.iterrows():
        print(f"{i+1}. {row['Crop Name']} | Field Size: {row['Field Size (acres)']} acres | Profit Per Acre: {row['Profit Per Acre']}")
    print("\nType the crop number to delete, or type 'all' to delete all your crops.")
    ans = input("Delete crop number/all or 'q' to cancel: ").strip().lower()
    if ans == 'q':
        print("Cancelled.")
        return
    elif ans == 'all':
        df = df[df["username"] != user["username"]]
        df.to_csv(FARMER_CROPS_CSV, index=False)
        print("All your crops have been deleted.")
        return
    else:
        try:
            idx = int(ans) - 1
            if idx < 0 or idx >= len(my_crops):
                print("Invalid crop number.")
                return
            row_to_delete = my_crops.iloc[idx]
            match = (
                (df["username"] == user["username"]) &
                (df["Crop Name"] == row_to_delete["Crop Name"]) &
                (df["Field Size (acres)"] == row_to_delete["Field Size (acres)"]) &
                (df["Profit Per Acre"] == row_to_delete["Profit Per Acre"]) &
                (df["Estimated Profit"] == row_to_delete["Estimated Profit"])
            )
            df = df[~match]
            df.to_csv(FARMER_CROPS_CSV, index=False)
            print(f"Crop '{row_to_delete['Crop Name']}' deleted.")
        except Exception:
            print("Invalid input. Cancelled.")

def reports_menu():
    while True:
        print("\n=== Reports & Analytics ===")
        print("1. Export Farmer Crops Report (CSV/Excel)")
        print("2. Profit Summary Dashboard")
        print("0. Back to Admin Menu")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            export_farmer_crops()
        elif choice == "2":
            profit_summary_dashboard()
        elif choice == "0":
            break
        else:
            print("❌ Invalid choice!")
        pause()


# ================= Menu Functions =================
def admin_menu(user):
    while True:
        print(f"\n=== Admin Dashboard ({user['username']}) ===")
        print("1. Register Farmer")
        print("2. View Farmers")
        print("3. Update Farmer")
        print("4. Delete Farmer")
        print("5. Manage Users")
        print("6. View Crop Information Database")
        print("7. Update Crop Profit Data Only")
        print("8. Reports & Analytics")
        print("0. Logout")
        
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
            user_management_menu()  
        elif choice == "6":
            view_crop_information()  
        elif choice == "7":
            update_crop_profit_data_only()
        elif choice == "8":
            reports_menu()  
        elif choice == "0":
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid choice!")
        pause()





def farmer_menu(user):
    while True:
        print(f"\n=== Farmer Dashboard ({user['username']}) ===")
        print("1. View Crop Information Database")
        print("2. Search & Filter Crops")
        print("3. Add My Crop with Profit Calculation")
        print("4. View My Crops")
        print("5. Delete My Crop Record")
        print("6. Update My Personal Record (name, location, contact)")
        print("7. Delete My Account")
        print("0. Logout")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            view_crop_information()
        elif choice == "2":
            search_and_filter_crops()
        elif choice == "3":
            add_crop_with_profit(user)  
        elif choice == "4":
            view_my_crops(user) 
        elif choice == "5":
            delete_my_record(user)  
        elif choice == "6":
            upsert_my_record(user)  
        elif choice == "7":
            delete_my_account(user)  
        elif choice == "0":
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
        print("0. Exit")

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
        elif choice == "0":
            print("Exiting portal. Goodbye 👋")
            sys.exit()
        else:
            print("Invalid choice! Try again.")

# ================= Run Program =================
if __name__ == "__main__":
    main()


