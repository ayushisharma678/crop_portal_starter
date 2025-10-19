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
# ================= Crop Profit Database =================
CROP_PROFIT_DATA = pd.DataFrame({
    "Crop Name": ["Rice", "Wheat", "Cotton", "Sugarcane", "Maize", "Potato", "Tomato", "Onion", "Groundnut", "Soybean"],
    "Profit Per Acre": [25000, 30000, 35000, 45000, 22000, 40000, 38000, 32000, 28000, 26000],
    "Season": ["Kharif", "Rabi", "Kharif", "Year-round", "Kharif", "Rabi", "Year-round", "Rabi", "Kharif", "Kharif"]
})

# ================= Detailed Crop Information Database =================
CROP_DETAILS = {
    "Rice": {
        "description": """Rice is one of the most important staple crops in India, feeding millions of people daily. It thrives in warm, humid climates and requires specific growing conditions for optimal yield.
        
GROWING PROCESS: Rice cultivation begins with land preparation through plowing and leveling. Seeds are either directly sown or transplanted as seedlings after 20-25 days in nursery beds. Transplanting is preferred as it allows better weed control and water management. The crop goes through four main growth stages: vegetative (tillering), reproductive (panicle initiation), flowering, and grain filling.

WATER REQUIREMENTS: Rice is a water-intensive crop requiring 1200-1500mm of water throughout its lifecycle. Fields must be kept flooded with 2-5 inches of standing water during most of the growing period. Proper drainage is essential 10-15 days before harvest. Alternate wetting and drying techniques can save water while maintaining yields.

SUNLIGHT REQUIREMENTS: Rice requires full sunlight, needing 6-8 hours of direct sunlight daily. It grows best in temperatures between 20-35°C. The crop is sensitive to temperature extremes during flowering stage.

SOIL REQUIREMENTS: Clay or clay-loam soils with good water retention capacity are ideal. Soil pH should range between 5.5-7.0. The field must be able to retain water without excessive seepage.

DURATION: The crop matures in 120-150 days depending on the variety. Early maturing varieties take 90-110 days while long-duration varieties need 150-160 days.

FERTILIZER NEEDS: Rice requires balanced NPK fertilization. Apply nitrogen in split doses - basal, tillering, and panicle initiation stages. Phosphorus and potassium should be applied as basal dose during field preparation."""
    },
    
    "Wheat": {
        "description": """Wheat is a crucial rabi crop and the second most important staple food in India. It's grown primarily in northern and central regions during the winter season.

GROWING PROCESS: Sowing begins after the monsoon season in October-November when temperatures drop. Seeds are sown using seed drill or broadcast method at 2-3 inch depth with row spacing of 20-23 cm. Germination occurs within 5-7 days. The crop undergoes crown root initiation, tillering, stem elongation, heading, and grain filling stages.

WATER REQUIREMENTS: Wheat requires 450-650mm of water during its entire growth period. It needs 4-6 irrigations depending on soil type and climate. Critical irrigation stages include crown root initiation (20-25 days after sowing), tillering, flowering, and grain filling stages. Proper drainage prevents waterlogging which can damage roots.

SUNLIGHT REQUIREMENTS: Wheat needs full sun exposure with 6-8 hours of bright sunlight daily. It grows optimally in temperatures between 10-25°C. Cool nights and warm days during grain filling enhance quality and yield.

SOIL REQUIREMENTS: Well-drained loamy soils with good organic matter content are best. Soil pH should range from 6.0-7.5. Heavy clay soils with poor drainage should be avoided as wheat is sensitive to waterlogging.

DURATION: The crop matures in 110-130 days for early varieties and 130-150 days for late-maturing varieties. Timely sowing is crucial for achieving maximum yields.

FERTILIZER NEEDS: Apply nitrogen in three splits - half at sowing, one-fourth at first irrigation (21 days), and remaining at second irrigation (40-45 days). Phosphorus and potassium should be applied at the time of sowing. Zinc application is beneficial in deficient soils."""
    },
    
    "Cotton": {
        "description": """Cotton is a major cash crop and fiber crop in India, providing raw material for the textile industry. It's grown as a kharif crop in tropical and subtropical regions.

GROWING PROCESS: Seeds are sown in rows with spacing of 60-90 cm between rows and 30-60 cm between plants. Germination occurs in 5-10 days. The plant develops vegetative branches and fruiting branches. Square formation (flower buds) begins 35-40 days after sowing, followed by flowering and boll development. Bolls mature and burst open revealing cotton fiber.

WATER REQUIREMENTS: Cotton requires 700-1300mm of water throughout the season. It needs moderate but regular water supply. Critical irrigation stages include germination, flowering, and boll development. The crop is drought-tolerant during vegetative stage but sensitive to moisture stress during flowering and boll formation. Over-irrigation causes excessive vegetative growth at the expense of fruiting.

SUNLIGHT REQUIREMENTS: Cotton is a sun-loving crop requiring 7-8 hours of bright sunlight daily. It thrives in temperatures between 21-30°C. Warm days and cool nights favor fiber quality. High humidity increases pest and disease problems.

SOIL REQUIREMENTS: Deep, well-drained black cotton soils or alluvial soils are ideal. Soil pH should range from 5.8-8.0, with 6.5-7.5 being optimal. Good soil aeration is essential for root development.

DURATION: Cotton takes 150-180 days to mature. Multiple pickings are done at 15-20 day intervals as bolls mature at different times.

FERTILIZER NEEDS: Apply nitrogen in splits at sowing, square formation, and flowering. Phosphorus and potassium boost boll formation and fiber quality. Micronutrients like zinc and boron are essential for good yields."""
    },
    
    "Sugarcane": {
        "description": """Sugarcane is a long-duration tropical crop and primary source of sugar production in India. It's a perennial grass that can be harvested multiple times from the same planting.

GROWING PROCESS: Two-budded setts from mature canes are planted horizontally in furrows 75-90 cm apart. Germination begins in 7-10 days with shoot emergence. The crop undergoes germination, tillering, grand growth, and maturity phases. Ratoon crops (subsequent harvests from the same roots) can be taken for 2-3 years.

WATER REQUIREMENTS: Sugarcane is one of the most water-demanding crops, requiring 1500-2500mm water during its lifecycle. It needs frequent irrigation every 7-10 days during summer and 12-15 days during winter. Critical stages include germination, tillering, and grand growth phase. Moisture stress reduces cane length and juice content.

SUNLIGHT REQUIREMENTS: Sugarcane requires abundant sunlight, needing 8-10 hours of direct sun daily. It grows best in temperatures between 20-35°C with high humidity. The crop shows excellent growth in warm, sunny conditions with adequate moisture.

SOIL REQUIREMENTS: Deep, well-drained loamy to clay-loam soils rich in organic matter are ideal. Soil pH should range from 6.5-7.5. Good drainage prevents waterlogging which causes root rot.

DURATION: The crop takes 10-18 months to mature depending on variety and growing conditions. Plant cane takes 12-18 months while ratoon crops mature in 10-12 months.

FERTILIZER NEEDS: Heavy feeder requiring large quantities of NPK. Apply nitrogen in splits at planting, tillering, and grand growth phase. Adequate potassium improves sugar content and disease resistance."""
    },
    
    "Maize": {
        "description": """Maize (corn) is a versatile cereal crop used as food, feed, and industrial raw material. It's grown in both kharif and rabi seasons across diverse agro-climatic conditions.

GROWING PROCESS: Seeds are sown 5-7 cm deep with row spacing of 60-75 cm and plant spacing of 20-25 cm. Germination occurs within 5-7 days. The crop passes through vegetative growth, tasseling (male flower emergence), silking (female flower emergence), pollination, and grain filling stages. Cross-pollination is essential for proper kernel development.

WATER REQUIREMENTS: Maize requires 500-800mm of water throughout its growing period. It needs adequate moisture during germination, knee-high stage, tasseling, and grain filling. The crop is highly sensitive to water stress during flowering and pollination, which can significantly reduce yields. Proper drainage prevents root diseases.

SUNLIGHT REQUIREMENTS: Maize needs full sun with 6-8 hours of direct sunlight daily. It grows optimally in temperatures between 21-30°C. High light intensity promotes photosynthesis and grain filling. The crop is sensitive to shade and cloudy conditions during critical growth stages.

SOIL REQUIREMENTS: Well-drained sandy loam to clay loam soils with good fertility are best. Soil pH should range from 5.5-7.5, with 6.0-7.0 being optimal. Proper soil aeration is important for root development.

DURATION: Early varieties mature in 75-90 days while medium and late varieties take 90-120 days. Sweet corn varieties mature earlier than grain corn.

FERTILIZER NEEDS: Apply nitrogen in splits at sowing, knee-high stage, and before tasseling. Phosphorus promotes root development and should be applied basally. Adequate zinc and sulfur improve yields significantly."""
    },
    
    "Potato": {
        "description": """Potato is a major vegetable crop and important food staple grown primarily during rabi season. It's a cool-season crop providing high yields in short duration.

GROWING PROCESS: Seed tubers (40-50g with 2-3 eyes) are planted 5-7 cm deep in ridges 60 cm apart with 15-20 cm plant spacing. Sprouts emerge in 7-12 days. The crop undergoes sprouting, vegetative growth, tuber initiation, tuber bulking, and maturity stages. Earthing up is done 25-30 days after planting to prevent tuber greening.

WATER REQUIREMENTS: Potato requires 500-750mm water during the growing season. It needs light frequent irrigation rather than heavy watering. Critical stages include tuber initiation and bulking phases. Moisture stress during tuber formation reduces yields while excess water causes rotting. Stop irrigation 10-15 days before harvest.

SUNLIGHT REQUIREMENTS: Potato grows best with 6-7 hours of bright sunlight daily in cool conditions. It prefers temperatures between 15-25°C. High temperatures above 30°C reduce tuber formation. Cool nights favor tuber development while warm days support foliage growth.

SOIL REQUIREMENTS: Well-drained sandy loam to loamy soils rich in organic matter are ideal. Soil pH should range from 5.0-6.5 (slightly acidic). Heavy clay soils cause tuber deformation while very sandy soils require frequent irrigation.

DURATION: Early varieties mature in 70-90 days, medium varieties in 90-110 days, and late varieties in 110-140 days. Harvest when leaves turn yellow and start drying.

FERTILIZER NEEDS: Potato is a heavy feeder requiring substantial NPK. Apply full dose of phosphorus and potassium at planting. Split nitrogen application at planting and earthing up. Adequate potassium improves tuber quality and storage life."""
    },
    
    "Tomato": {
        "description": """Tomato is the most popular vegetable crop grown worldwide for fresh consumption and processing. It can be grown year-round in different seasons with appropriate variety selection.

GROWING PROCESS: Seeds are sown in nursery beds and transplanted after 4-6 weeks when seedlings have 4-5 true leaves. Plant spacing varies: 75x60 cm for indeterminate varieties and 60x45 cm for determinate types. Staking and pruning are essential for indeterminate varieties. The crop flowers within 30-40 days of transplanting and fruits mature 55-70 days after transplanting.

WATER REQUIREMENTS: Tomato requires 600-800mm water during the entire crop period. It needs regular moisture for uniform fruit development. Critical stages include transplanting, flowering, and fruit development. Irregular watering causes fruit cracking and blossom end rot. Drip irrigation is highly recommended for water efficiency and disease prevention.

SUNLIGHT REQUIREMENTS: Tomato requires full sun with 7-8 hours of bright light daily. It grows optimally in temperatures between 18-27°C. High temperatures above 35°C cause flower drop while low temperatures below 10°C reduce fruit set. Adequate sunlight promotes better fruit color and flavor.

SOIL REQUIREMENTS: Well-drained sandy loam to loam soils rich in organic matter are ideal. Soil pH should range from 6.0-7.0. Good drainage is essential as tomatoes are susceptible to root rot in waterlogged conditions.

DURATION: The crop duration varies from 90-150 days depending on variety. Determinate varieties mature earlier (90-110 days) while indeterminate varieties produce over longer periods (120-150 days).

FERTILIZER NEEDS: Apply nitrogen in splits during vegetative growth and fruiting stages. Adequate phosphorus promotes root development and flowering. Calcium prevents blossom end rot while potassium improves fruit quality and disease resistance."""
    },
    
    "Onion": {
        "description": """Onion is an essential vegetable crop and commercial crop grown primarily during rabi season. It's used fresh and in processed forms, with significant domestic and export demand.

GROWING PROCESS: Seeds are sown in nursery beds and transplanted after 6-8 weeks when seedlings are pencil-thick. Plant spacing of 15x10 cm is maintained. The crop undergoes vegetative growth, bulb initiation, bulb development, and maturity stages. Day length triggers bulb formation - short-day varieties for kharif and long-day varieties for rabi season.

WATER REQUIREMENTS: Onion requires 350-550mm water throughout the growing season. It has shallow roots requiring frequent light irrigation. Critical stages include transplanting, vegetative growth, and bulb development. Stop irrigation 10-15 days before harvest to allow bulbs to mature and cure properly. Excess moisture during maturity causes bulb diseases.

SUNLIGHT REQUIREMENTS: Onion needs full sun with 6-8 hours of direct sunlight daily. It grows best in temperatures between 13-24°C during vegetative phase and 16-25°C during bulb development. Day length is crucial - longer days promote bulb formation in long-day varieties.

SOIL REQUIREMENTS: Well-drained loamy to sandy loam soils with good organic matter content are ideal. Soil pH should range from 6.0-7.0. Heavy clay soils cause bulb deformation while very light soils require frequent irrigation. Good soil structure is essential for proper bulb development.

DURATION: Short-day varieties mature in 90-120 days while long-day varieties take 140-180 days. Harvest when 50-70% of tops fall over naturally.

FERTILIZER NEEDS: Apply nitrogen in splits at planting, 30 days, and 45 days after transplanting. Adequate phosphorus promotes early rooting. Sulfur is essential for pungency and storage quality. Avoid excessive nitrogen which delays maturity and reduces storage life."""
    },
    
    "Groundnut": {
        "description": """Groundnut (peanut) is an important oilseed and cash crop grown primarily during kharif season. It's unique as pods develop underground, requiring specific cultivation practices.

GROWING PROCESS: Seeds are sown 5-6 cm deep in rows 30 cm apart with 10 cm plant spacing. Germination occurs in 5-7 days. The crop undergoes vegetative growth, flowering, pegging (downward growth of fertilized ovary), pod development, and maturity. After flowering, pegs penetrate soil where pods develop. Loose soil is essential for pod penetration.

WATER REQUIREMENTS: Groundnut requires 500-600mm water during the growing season. It's moderately drought-tolerant but needs adequate moisture during flowering, pegging, and pod development stages. Critical irrigation stages include flowering (30-40 days), pegging and pod formation (50-70 days). Excess moisture during maturity reduces oil content and causes aflatoxin contamination.

SUNLIGHT REQUIREMENTS: Groundnut is a sun-loving crop requiring 7-8 hours of bright sunlight daily. It grows optimally in temperatures between 25-30°C. Warm sunny weather promotes better pod filling and oil synthesis. The crop is sensitive to prolonged cloudy conditions during pod development.

SOIL REQUIREMENTS: Well-drained sandy loam to loam soils with loose structure are ideal. Soil pH should range from 6.0-6.5 (slightly acidic). Calcium-rich soils produce better quality pods. Heavy clay soils restrict pod development and harvesting becomes difficult.

DURATION: Early varieties mature in 100-110 days while medium and late varieties take 120-140 days. Harvest when leaves turn yellow and inner pod surface shows dark brown markings.

FERTILIZER NEEDS: Groundnut has moderate nutrient requirements. Apply full dose of phosphorus and potassium at sowing. Limited nitrogen as excessive nitrogen promotes vegetative growth at the expense of pods. Gypsum application at flowering improves pod filling and reduces empty pods."""
    },
    
    "Soybean": {
        "description": """Soybean is a major kharif oilseed crop and excellent protein source. It's called the 'golden bean' due to its high protein and oil content with significant industrial applications.

GROWING PROCESS: Seeds are sown 3-5 cm deep in rows 45 cm apart with 5-7 cm plant spacing. Germination occurs within 4-6 days. The crop undergoes vegetative growth, flowering, pod formation, and maturity stages. Soybean forms root nodules with nitrogen-fixing bacteria, reducing nitrogen fertilizer requirements. Proper seed inoculation with Rhizobium culture enhances nitrogen fixation.

WATER REQUIREMENTS: Soybean requires 450-700mm water during the growing season. It needs adequate but not excessive moisture. Critical stages include germination, flowering, and pod filling. Moisture stress during flowering causes flower drop while stress during pod filling reduces seed size. Good drainage prevents root diseases and nodule damage.

SUNLIGHT REQUIREMENTS: Soybean requires full sun with 6-8 hours of direct sunlight daily. It's a short-day plant sensitive to photoperiod. Optimum temperature range is 20-30°C. High temperatures during flowering reduce pod set while low temperatures delay maturity.

SOIL REQUIREMENTS: Well-drained loamy soils with good organic matter content are ideal. Soil pH should range from 6.0-7.0. The crop is sensitive to waterlogging and acidic soils. Good soil structure promotes nodule formation and root development.

DURATION: Early varieties mature in 75-90 days, medium varieties in 90-105 days, and late varieties in 105-120 days. Harvest when 95% pods turn brown and leaves drop.

FERTILIZER NEEDS: Soybean has low nitrogen requirements due to biological nitrogen fixation. Seed inoculation with Rhizobium is crucial. Apply phosphorus and potassium at sowing. Adequate sulfur improves oil content. Avoid excessive nitrogen which inhibits nodule formation and reduces protein content."""
    }
}



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
        
        # Display crops with numbering
        available_crops = list(CROP_DETAILS.keys())
        for idx, crop_name in enumerate(available_crops, 1):
            profit = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"] == crop_name]["Profit Per Acre"].values[0]
            season = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"] == crop_name]["Season"].values[0]
            print(f"{idx}. {crop_name:<15} | Season: {season:<12} | Profit/Acre: ₹{profit:,}")
        
        print(f"\n{len(available_crops) + 1}. Return to Dashboard")
        print("="*60)
        
        choice = input("\nEnter crop number to view detailed information (or return option): ").strip()
        
        # Check if user wants to return
        if choice == str(len(available_crops) + 1):
            print("Returning to dashboard...\n")
            break
        
        # Validate choice
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
    
    # Display all farmers with their contacts
    print("\n--- Registered Farmers ---")
    for idx, row in df.iterrows():
        print(f"{idx + 1}. {row['Farmer Name']:<20} | Contact: {row['Contact']:<12} | Location: {row['Location']}")
    
    # Option to update contact
    update = input("\nDo you want to update any contact? (yes/no): ").strip().lower()
    
    if update == "yes":
        farmer_name = input("Enter farmer name to update: ").strip()
        
        # Check if farmer exists
        if farmer_name not in df["Farmer Name"].values:
            print(f"❌ Farmer '{farmer_name}' not found!")
            return
        
        # Get new contact number
        while True:
            new_contact = input("Enter new contact number (10 digits): ").strip()
            
            if len(new_contact) == 10 and new_contact.isdigit():
                break
            else:
                print("❌ Invalid contact number! Please enter exactly 10 digits.")
        
        # Update the contact
        df.loc[df["Farmer Name"] == farmer_name, "Contact"] = new_contact
        df.to_excel(FARMERS_FILE, index=False)
        
        print(f"✅ Contact updated successfully for farmer '{farmer_name}'!")
        print(f"   New contact: {new_contact}")



def display_single_crop_details(crop_name):
    """Display detailed information for a specific crop"""
    print("\n" + "="*70)
    print(f"📋 DETAILED INFORMATION: {crop_name.upper()}")
    print("="*70)
    
    # Get profit and season information
    crop_profit_info = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"] == crop_name]
    profit_per_acre = crop_profit_info.iloc[0]["Profit Per Acre"]
    season = crop_profit_info.iloc[0]["Season"]
    
    print(f"\n💰 Expected Profit: ₹{profit_per_acre:,} per acre")
    print(f"🌦️  Best Season: {season}")
    print("\n" + "-"*70)
    
    # Display detailed description
    description = CROP_DETAILS[crop_name]["description"]
    print(description)
    
    print("\n" + "="*70)
    
    # Wait for user to read
    input("\nPress Enter to continue...")


def add_crop_with_profit():
    print("\n--- Add Crop with Profit Calculation ---")
    farmer = input("Enter farmer name: ")
    
    # Check if farmer exists
    df_farmers = pd.read_excel(FARMERS_FILE)
    if farmer not in df_farmers["Farmer Name"].values:
        print(f"❌ Farmer '{farmer}' not found! Please register first.")
        return
    
    # Display available crops
    display_available_crops()
    
    # Get list of available crop names
    available_crops = CROP_PROFIT_DATA["Crop Name"].tolist()
    print(f"\nAvailable crop choices: {', '.join(available_crops)}")
    
    # Input crop selection
    crop = input("\nEnter crop name from the list above: ").strip()
    
    # Check if crop exists in database
    crop_data = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"].str.lower() == crop.lower()]
    
    if crop_data.empty:
        print(f"❌ Crop '{crop}' not found in our database. Please choose from the available list.")
        return
    
    # Extract profit per acre for selected crop
    profit_per_acre = crop_data.iloc[0]["Profit Per Acre"]
    recommended_season = crop_data.iloc[0]["Season"]
    
    # Get user inputs
    quantity = input("Enter quantity (kg): ").strip()
    season = input(f"Enter season (Recommended: {recommended_season}): ").strip()
    
    try:
        field_size = float(input("Enter field size (in acres): ").strip())
    except ValueError:
        print("❌ Invalid field size. Please enter a number.")
        return
    
    # Calculate total profit
    total_profit = profit_per_acre * field_size
    
    # Display profit calculation
    print("\n" + "="*50)
    print("💰 PROFIT CALCULATION")
    print("="*50)
    print(f"Crop Selected      : {crop}")
    print(f"Profit per Acre    : ₹{profit_per_acre:,.2f}")
    print(f"Field Size         : {field_size} acres")
    print(f"Estimated Profit   : ₹{total_profit:,.2f}")
    print("="*50)
    
    # Seasonal recommendation check
    if season.lower() != recommended_season.lower():
        print(f"⚠️  Warning: Recommended season for {crop} is {recommended_season}")
    
    # Save crop data with profit information
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
    
    # If registering as farmer, collect phone number
    if role == "farmer":
        while True:
            contact = input("Enter contact number (10 digits): ").strip()
            
            # Validate phone number
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
        # Admin doesn't need contact
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
    
    # Check if farmer already exists
    df = pd.read_excel(FARMERS_FILE)
    if name in df["Farmer Name"].values:
        print(f"⚠️ Farmer '{name}' already registered!")
        return
    
    # Get and validate contact number
    while True:
        contact = input("Enter contact number (10 digits): ").strip()
        
        # Validate phone number
        if len(contact) == 10 and contact.isdigit():
            break
        else:
            print("❌ Invalid contact number! Please enter exactly 10 digits.")
            retry = input("Try again? (yes/no): ").strip().lower()
            if retry != "yes":
                print("Registration cancelled.")
                return
    
    location = input("Enter location: ").strip()
    
    # Add new farmer
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
        print("3. View/Update Farmer Contact")  # New option
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
            view_update_farmer_contact()  # New function call
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
        print("3. View Crop Information Database")  # Changed from "View Available Crops Database"
        print("4. View My Crops")
        print("5. Logout")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            add_crop()
        elif choice == "2":
            add_crop_with_profit()
        elif choice == "3":
            view_crop_information()  # Changed function call
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
