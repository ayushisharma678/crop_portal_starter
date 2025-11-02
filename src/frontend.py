import streamlit as st
import pandas as pd
import os
from storage import (
    DATA_DIR, load_users, save_users, load_crops, save_crops,
    load_farmers, save_farmers, load_crop_profit, save_crop_profit,
    load_crop_details, save_crop_details, next_id, ensure_data_files,
    CROP_PROFIT_CSV, CROP_DETAILS_CSV
)
from security import hash_password, verify_password
import re

# Page configuration
st.set_page_config(
    page_title="🌾 Crop Management Portal",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2e7d32;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(120deg, #a8e063 0%, #56ab2f 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f7f0;
        padding: 1.5rem;
        border-radius: 10.1px;
        border-left: 5px solid #4caf50;
    }
    .stButton>button {
        width: 100%;
        background-color: #4caf50;
        color: white;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# Load crop data
ensure_data_files()
FARMER_CROPS_CSV = os.path.join(DATA_DIR, "farmer_crops.csv")

try:
    CROP_PROFIT_DATA = pd.read_csv(CROP_PROFIT_CSV)
    crop_details_df = pd.read_csv(CROP_DETAILS_CSV)
    CROP_DETAILS = {row["Crop Name"]: {"description": row["Description"]} 
                   for idx, row in crop_details_df.iterrows()}
except Exception as e:
    st.error(f"Error loading crop data: {e}")
    CROP_PROFIT_DATA = pd.DataFrame()
    CROP_DETAILS = {}

# Helper functions
def is_valid_password(password):
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(pattern, password)

def logout():
    st.session_state.user = None
    st.session_state.page = 'login'
    st.rerun()

# Registration Page
def registration_page():
    st.markdown('<div class="main-header">🌾 User Registration</div>', unsafe_allow_html=True)
    
    with st.form("registration_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username*")
            name = st.text_input("Full Name*")
            password = st.text_input("Password*", type="password", 
                                    help="Min 8 chars, 1 uppercase, 1 lowercase, 1 digit, 1 special char")
            confirm_password = st.text_input("Confirm Password*", type="password")
        
        with col2:
            role = st.selectbox("Role*", ["farmer", "admin"])
            
            if role == "farmer":
                contact = st.text_input("Contact Number* (10 digits)")
                location = st.text_input("Location*")
        
        submitted = st.form_submit_button("Register", type="primary")
        
        if submitted:
            users = load_users()
            
            # Validation
            if not username or not name or not password:
                st.error("❌ Please fill all required fields!")
            elif not users.empty and (users["username"] == username).any():
                st.error("❌ Username already exists!")
            elif len(name) < 2:
                st.error("❌ Name must be at least 2 characters!")
            elif password != confirm_password:
                st.error("❌ Passwords don't match!")
            elif not is_valid_password(password):
                st.error("❌ Password must have at least 1 uppercase, 1 lowercase, 1 digit, 1 special char, min 8 chars")
            elif role == "farmer" and (not contact or len(contact) != 10 or not contact.isdigit()):
                st.error("❌ Contact must be exactly 10 digits!")
            elif role == "farmer" and not location:
                st.error("❌ Location is required for farmers!")
            else:
                # Create user
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
                
                # Create farmer record if applicable
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
                
                st.success(f"✅ {role.capitalize()} '{name}' registered successfully!")
                st.info("Please go to Login page to access your account.")
    
    if st.button("Already have an account? Login"):
        st.session_state.page = 'login'
        st.rerun()

# Login Page
def login_page():
    st.markdown('<div class="main-header">🌾 Crop Management Portal</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", type="primary")
            
            if submitted:
                users = load_users()
                
                if users.empty:
                    st.error("❌ No users found. Please register first.")
                else:
                    row = users[users["username"] == username]
                    if row.empty:
                        st.error("❌ User not found.")
                    else:
                        row = row.iloc[0]
                        if verify_password(password, row["password_hash"], row["salt"]):
                            st.session_state.user = {
                                "user_id": int(row["user_id"]),
                                "username": row["username"],
                                "name": row["name"],
                                "role": row["role"]
                            }
                            st.success(f"✅ Welcome, {row['name']}!")
                            st.rerun()
                        else:
                            st.error("❌ Incorrect password.")
        
        if st.button("Don't have an account? Register"):
            st.session_state.page = 'register'
            st.rerun()

# Admin Dashboard
def admin_dashboard():
    st.sidebar.title(f"👤 {st.session_state.user['name']}")
    st.sidebar.caption(f"Role: Admin")
    
    menu = st.sidebar.radio("Navigation", [
        "📊 Dashboard",
        "👨‍🌾 Manage Farmers",
        "👥 Manage Users",
        "🌾 Crop Information",
        "💰 Update Crop Profits",
        "📈 Reports & Analytics"
    ])
    
    if st.sidebar.button("🚪 Logout"):
        logout()
    
    if menu == "📊 Dashboard":
        admin_dashboard_home()
    elif menu == "👨‍🌾 Manage Farmers":
        manage_farmers_page()
    elif menu == "👥 Manage Users":
        manage_users_page()
    elif menu == "🌾 Crop Information":
        view_crop_information_page()
    elif menu == "💰 Update Crop Profits":
        update_crop_profits_page()
    elif menu == "📈 Reports & Analytics":
        reports_analytics_page()

def admin_dashboard_home():
    st.markdown('<div class="main-header">📊 Admin Dashboard</div>', unsafe_allow_html=True)
    
    # Metrics
    users = load_users()
    farmers = load_farmers()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", len(users))
    with col2:
        st.metric("Total Farmers", len(farmers))
    with col3:
        st.metric("Total Crops", len(CROP_PROFIT_DATA))
    with col4:
        if os.path.exists(FARMER_CROPS_CSV):
            farmer_crops = pd.read_csv(FARMER_CROPS_CSV)
            st.metric("Crop Records", len(farmer_crops))
        else:
            st.metric("Crop Records", 0)
    
    st.markdown("---")
    
    # Recent farmers
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👨‍🌾 Recent Farmers")
        if not farmers.empty:
            st.dataframe(farmers.tail(5), use_container_width=True)
        else:
            st.info("No farmers registered yet.")
    
    with col2:
        st.subheader("🌾 Available Crops")
        if not CROP_PROFIT_DATA.empty:
            st.dataframe(CROP_PROFIT_DATA[['Crop Name', 'Season', 'Profit Per Acre']].head(5), 
                        use_container_width=True)
        else:
            st.info("No crop data available.")

def manage_farmers_page():
    st.title("👨‍🌾 Manage Farmers")
    
    tab1, tab2, tab3, tab4 = st.tabs(["View All", "Add New", "Update", "Delete"])
    
    with tab1:
        farmers = load_farmers()
        if not farmers.empty:
            st.dataframe(farmers, use_container_width=True)
        else:
            st.info("No farmers registered yet.")
    
    with tab2:
        st.subheader("Add New Farmer")
        with st.form("add_farmer_form"):
            name = st.text_input("Farmer Name*")
            username = st.text_input("Username")
            location = st.text_input("Location*")
            contact = st.text_input("Contact Number* (10 digits)")
            
            if st.form_submit_button("Add Farmer"):
                farmers = load_farmers()
                
                if not name or not location or not contact:
                    st.error("❌ Please fill all required fields!")
                elif len(contact) != 10 or not contact.isdigit():
                    st.error("❌ Contact must be exactly 10 digits!")
                elif not farmers.empty and name in farmers["name"].values:
                    st.error(f"⚠️ Farmer '{name}' already registered!")
                else:
                    farmer_id = next_id(farmers, "farmer_id")
                    new_row = {
                        "farmer_id": farmer_id,
                        "username": username if username else name.lower(),
                        "name": name,
                        "location": location,
                        "contact": contact
                    }
                    farmers = pd.concat([farmers, pd.DataFrame([new_row])], ignore_index=True)
                    save_farmers(farmers)
                    st.success(f"✅ Farmer '{name}' registered successfully!")
    
    with tab3:
        st.subheader("Update Farmer")
        farmers = load_farmers()
        if not farmers.empty:
            farmer_names = farmers["name"].tolist()
            selected_farmer = st.selectbox("Select Farmer", farmer_names)
            
            farmer_row = farmers[farmers["name"] == selected_farmer].iloc[0]
            
            with st.form("update_farmer_form"):
                new_username = st.text_input("Username", value=farmer_row["username"])
                new_name = st.text_input("Name", value=farmer_row["name"])
                new_location = st.text_input("Location", value=farmer_row["location"])
                new_contact = st.text_input("Contact", value=farmer_row["contact"])
                
                if st.form_submit_button("Update Farmer"):
                    if len(new_contact) != 10 or not new_contact.isdigit():
                        st.error("❌ Contact must be exactly 10 digits!")
                    else:
                        idx = farmers.index[farmers["name"] == selected_farmer][0]
                        farmers.at[idx, "username"] = new_username
                        farmers.at[idx, "name"] = new_name
                        farmers.at[idx, "location"] = new_location
                        farmers.at[idx, "contact"] = new_contact
                        save_farmers(farmers)
                        st.success("✅ Farmer updated successfully!")
                        st.rerun()
        else:
            st.info("No farmers to update.")
    
    with tab4:
        st.subheader("Delete Farmer")
        farmers = load_farmers()
        if not farmers.empty:
            farmer_ids = farmers["farmer_id"].astype(str).tolist()
            selected_id = st.selectbox("Select Farmer ID", farmer_ids)
            
            farmer_info = farmers[farmers["farmer_id"].astype(str) == selected_id].iloc[0]
            st.warning(f"You are about to delete: {farmer_info['name']}")
            
            if st.button("Delete Farmer", type="primary"):
                farmers = farmers[farmers["farmer_id"].astype(str) != selected_id]
                save_farmers(farmers)
                st.success("✅ Farmer deleted successfully!")
                st.rerun()
        else:
            st.info("No farmers to delete.")

def manage_users_page():
    st.title("👥 Manage Users")
    
    tab1, tab2, tab3 = st.tabs(["View All", "Update", "Delete"])
    
    with tab1:
        users = load_users()
        if not users.empty:
            display_users = users.drop(columns=["password_hash", "salt"], errors='ignore')
            st.dataframe(display_users, use_container_width=True)
        else:
            st.info("No users registered yet.")
    
    with tab2:
        st.subheader("Update User")
        users = load_users()
        if not users.empty:
            usernames = users["username"].tolist()
            selected_user = st.selectbox("Select User", usernames)
            
            user_row = users[users["username"] == selected_user].iloc[0]
            
            with st.form("update_user_form"):
                new_username = st.text_input("Username", value=user_row["username"])
                new_name = st.text_input("Name", value=user_row["name"])
                new_role = st.selectbox("Role", ["admin", "farmer"], 
                                       index=0 if user_row["role"] == "admin" else 1)
                new_password = st.text_input("New Password (leave blank to keep current)", type="password")
                
                if st.form_submit_button("Update User"):
                    if new_username != user_row["username"] and new_username in users["username"].values:
                        st.error("❌ Username already exists!")
                    else:
                        idx = users.index[users["username"] == selected_user][0]
                        users.at[idx, "username"] = new_username
                        users.at[idx, "name"] = new_name
                        users.at[idx, "role"] = new_role
                        
                        if new_password:
                            phash, salt = hash_password(new_password)
                            users.at[idx, "password_hash"] = phash
                            users.at[idx, "salt"] = salt
                        
                        save_users(users)
                        st.success("✅ User updated successfully!")
                        st.rerun()
        else:
            st.info("No users to update.")
    
    with tab3:
        st.subheader("Delete User")
        users = load_users()
        if not users.empty:
            usernames = users["username"].tolist()
            selected_user = st.selectbox("Select User to Delete", usernames)
            
            user_info = users[users["username"] == selected_user].iloc[0]
            st.warning(f"You are about to delete: {user_info['name']} ({user_info['role']})")
            
            confirm = st.checkbox("I confirm I want to delete this user")
            
            if confirm and st.button("Delete User", type="primary"):
                users = users[users["username"] != selected_user]
                save_users(users)
                st.success("✅ User deleted successfully!")
                st.rerun()
        else:
            st.info("No users to delete.")

def view_crop_information_page():
    st.title("🌾 Crop Information Database")
    
    if CROP_PROFIT_DATA.empty:
        st.warning("No crop data available.")
        return
    
    # Search and filter
    col1, col2 = st.columns(2)
    
    with col1:
        season_filter = st.selectbox("Filter by Season", 
                                     ["All"] + CROP_PROFIT_DATA["Season"].unique().tolist())
    
    with col2:
        search_crop = st.text_input("Search Crop Name")
    
    filtered_data = CROP_PROFIT_DATA.copy()
    
    if season_filter != "All":
        filtered_data = filtered_data[filtered_data["Season"] == season_filter]
    
    if search_crop:
        filtered_data = filtered_data[filtered_data["Crop Name"].str.contains(search_crop, case=False, na=False)]
    
    st.dataframe(filtered_data, use_container_width=True)
    
    # Detailed view
    if not filtered_data.empty:
        st.markdown("---")
        st.subheader("View Detailed Information")
        
        crop_names = filtered_data["Crop Name"].tolist()
        selected_crop = st.selectbox("Select Crop for Details", crop_names)
        
        if selected_crop:
            crop_data = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"] == selected_crop].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Crop Name", crop_data["Crop Name"])
            with col2:
                st.metric("Season", crop_data["Season"])
            with col3:
                st.metric("Profit Per Acre", f"₹{crop_data['Profit Per Acre']:,.2f}")
            
            if selected_crop in CROP_DETAILS:
                st.markdown("### Description")
                st.info(CROP_DETAILS[selected_crop]["description"])

def update_crop_profits_page():
    global CROP_PROFIT_DATA
    st.title("💰 Update Crop Profit Data")
    
    if CROP_PROFIT_DATA.empty:
        st.warning("No crop profit data available.")
        return
    
    st.dataframe(CROP_PROFIT_DATA, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Update Profit")
    
    crop_names = CROP_PROFIT_DATA["Crop Name"].tolist()
    selected_crop = st.selectbox("Select Crop", crop_names)
    
    if selected_crop:
        crop_row = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"] == selected_crop].iloc[0]
        current_profit = crop_row["Profit Per Acre"]
        
        st.info(f"Current Profit: ₹{current_profit:,.2f} per acre")
        
        new_profit = st.number_input("New Profit Per Acre (₹)", min_value=0.0, 
                                     value=float(current_profit), step=100.0)
        
        if st.button("Update Profit", type="primary"):
            CROP_PROFIT_DATA.loc[CROP_PROFIT_DATA["Crop Name"] == selected_crop, "Profit Per Acre"] = new_profit
            CROP_PROFIT_DATA.to_csv(CROP_PROFIT_CSV, index=False)
            
            change = new_profit - current_profit
            change_pct = (change / current_profit * 100) if current_profit != 0 else 0
            
            st.success(f"✅ Profit updated successfully for '{selected_crop}'!")
            st.metric("Change", f"₹{change:+,.2f}", f"{change_pct:+.1f}%")
            st.rerun()

def reports_analytics_page():
    st.title("📈 Reports & Analytics")
    
    tab1, tab2 = st.tabs(["Profit Summary", "Export Reports"])
    
    with tab1:
        if os.path.exists(FARMER_CROPS_CSV):
            df = pd.read_csv(FARMER_CROPS_CSV)
            if not df.empty:
                df['Estimated Profit'] = pd.to_numeric(df['Estimated Profit'], errors='coerce')
                summary = df.groupby("username")["Estimated Profit"].sum().reset_index()
                summary.columns = ["Farmer", "Total Expected Profit (₹)"]
                
                total_profit = summary["Total Expected Profit (₹)"].sum()
                
                st.metric("Total Portal Expected Profit", f"₹{total_profit:,.2f}")
                
                st.markdown("---")
                st.subheader("Profit by Farmer")
                st.dataframe(summary, use_container_width=True)
                
                # Chart
                st.bar_chart(summary.set_index("Farmer"))
            else:
                st.info("No crop records to analyze.")
        else:
            st.info("No crop records found.")
    
    with tab2:
        st.subheader("Export Data")
        
        if os.path.exists(FARMER_CROPS_CSV):
            df = pd.read_csv(FARMER_CROPS_CSV)
            
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download Farmer Crops (CSV)",
                data=csv,
                file_name="farmer_crops_export.csv",
                mime="text/csv"
            )
        else:
            st.info("No data to export.")

# Farmer Dashboard
def farmer_dashboard():
    st.sidebar.title(f"👤 {st.session_state.user['name']}")
    st.sidebar.caption(f"Role: Farmer")
    
    menu = st.sidebar.radio("Navigation", [
        "📊 Dashboard",
        "🌾 Crop Information",
        "🔍 Search Crops",
        "➕ Add My Crop",
        "📋 My Crops",
        "👤 My Profile"
    ])
    
    if st.sidebar.button("🚪 Logout"):
        logout()
    
    if menu == "📊 Dashboard":
        farmer_dashboard_home()
    elif menu == "🌾 Crop Information":
        view_crop_information_page()
    elif menu == "🔍 Search Crops":
        search_filter_crops_page()
    elif menu == "➕ Add My Crop":
        add_my_crop_page()
    elif menu == "📋 My Crops":
        my_crops_page()
    elif menu == "👤 My Profile":
        my_profile_page()

def farmer_dashboard_home():
    st.markdown('<div class="main-header">📊 Farmer Dashboard</div>', unsafe_allow_html=True)
    
    user = st.session_state.user
    
    # Load my crops
    if os.path.exists(FARMER_CROPS_CSV):
        df = pd.read_csv(FARMER_CROPS_CSV)
        df['username'] = df['username'].astype(str)
        my_crops = df[df["username"] == user["username"]]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("My Crops", len(my_crops))
        
        with col2:
            if not my_crops.empty:
                my_crops['Estimated Profit'] = pd.to_numeric(my_crops['Estimated Profit'], errors='coerce')
                total = my_crops['Estimated Profit'].sum()
                st.metric("Total Expected Profit", f"₹{total:,.2f}")
            else:
                st.metric("Total Expected Profit", "₹0")
        
        with col3:
            if not my_crops.empty:
                total_acres = my_crops['Field Size (acres)'].astype(float).sum()
                st.metric("Total Field Size", f"{total_acres:.2f} acres")
            else:
                st.metric("Total Field Size", "0 acres")
        
        st.markdown("---")
        
        if not my_crops.empty:
            st.subheader("📋 My Recent Crops")
            st.dataframe(my_crops.tail(5), use_container_width=True)
        else:
            st.info("🌱 You haven't added any crops yet. Start by adding your first crop!")
    else:
        st.info("🌱 You haven't added any crops yet. Start by adding your first crop!")
    
    st.markdown("---")
    st.subheader("🌾 Available Crops in Database")
    if not CROP_PROFIT_DATA.empty:
        st.dataframe(CROP_PROFIT_DATA, use_container_width=True)

def search_filter_crops_page():
    st.title("🔍 Search & Filter Crops")
    
    if CROP_PROFIT_DATA.empty:
        st.warning("No crop data available.")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        season_filter = st.selectbox("Season", ["All"] + CROP_PROFIT_DATA["Season"].unique().tolist())
    
    with col2:
        min_profit = st.number_input("Min Profit (₹)", min_value=0.0, value=0.0, step=1000.0)
    
    with col3:
        max_profit = st.number_input("Max Profit (₹)", min_value=0.0, value=0.0, step=1000.0)
    
    filtered_data = CROP_PROFIT_DATA.copy()
    
    if season_filter != "All":
        filtered_data = filtered_data[filtered_data["Season"] == season_filter]
    
    if min_profit > 0:
        filtered_data = filtered_data[filtered_data["Profit Per Acre"] >= min_profit]
    
    if max_profit > 0:
        filtered_data = filtered_data[filtered_data["Profit Per Acre"] <= max_profit]
    
    st.markdown("---")
    
    if filtered_data.empty:
        st.warning("No crops match your filter criteria.")
    else:
        st.success(f"Found {len(filtered_data)} crops matching your criteria")
        st.dataframe(filtered_data, use_container_width=True)
        
        # Detailed view
        crop_names = filtered_data["Crop Name"].tolist()
        selected_crop = st.selectbox("View Details", crop_names)
        
        if selected_crop:
            crop_data = filtered_data[filtered_data["Crop Name"] == selected_crop].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Crop", crop_data["Crop Name"])
            with col2:
                st.metric("Season", crop_data["Season"])
            with col3:
                st.metric("Profit/Acre", f"₹{crop_data['Profit Per Acre']:,.2f}")
            
            if selected_crop in CROP_DETAILS:
                st.markdown("### Description")
                st.info(CROP_DETAILS[selected_crop]["description"])

def add_my_crop_page():
    st.title("➕ Add My Crop with Profit Calculation")
    
    if CROP_PROFIT_DATA.empty:
        st.warning("No crop data available.")
        return
    
    st.subheader("Available Crops")
    st.dataframe(CROP_PROFIT_DATA[['Crop Name', 'Season', 'Profit Per Acre']], use_container_width=True)
    
    st.markdown("---")
    
    with st.form("add_crop_form"):
        crop_names = CROP_PROFIT_DATA["Crop Name"].tolist()
        selected_crop = st.selectbox("Select Crop*", crop_names)
        
        field_size = st.number_input("Field Size (acres)*", min_value=0.01, value=1.0, step=0.1)
        
        if st.form_submit_button("Calculate & Add Crop", type="primary"):
            crop_data = CROP_PROFIT_DATA[CROP_PROFIT_DATA["Crop Name"] == selected_crop].iloc[0]
            profit_per_acre = float(crop_data["Profit Per Acre"])
            total_profit = profit_per_acre * field_size
            
            # Show calculation
            st.success("💰 Profit Calculation")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Profit/Acre", f"₹{profit_per_acre:,.2f}")
            with col2:
                st.metric("Field Size", f"{field_size} acres")
            with col3:
                st.metric("Total Profit", f"₹{total_profit:,.2f}")
            
            # Save to CSV
            if not os.path.exists(FARMER_CROPS_CSV):
                with open(FARMER_CROPS_CSV, "w", encoding="utf-8") as f:
                    f.write("username,Crop Name,Field Size (acres),Profit Per Acre,Estimated Profit\n")
            
            df = pd.read_csv(FARMER_CROPS_CSV)
            new_row = {
                "username": st.session_state.user["username"],
                "Crop Name": selected_crop,
                "Field Size (acres)": field_size,
                "Profit Per Acre": profit_per_acre,
                "Estimated Profit": total_profit
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(FARMER_CROPS_CSV, index=False)
            
            st.success(f"✅ Crop '{selected_crop}' added successfully!")
            st.balloons()

def my_crops_page():
    st.title("📋 My Crops")
    
    user = st.session_state.user
    
    if not os.path.exists(FARMER_CROPS_CSV):
        st.info("You haven't added any crops yet.")
        return
    
    df = pd.read_csv(FARMER_CROPS_CSV)
    df['username'] = df['username'].astype(str)
    my_crops = df[df["username"] == user["username"]]
    
    if my_crops.empty:
        st.info("You haven't added any crops yet.")
        return
    
    # Display crops
    st.dataframe(my_crops, use_container_width=True)
    
    # Total profit
    my_crops['Estimated Profit'] = pd.to_numeric(my_crops['Estimated Profit'], errors='coerce')
    total = my_crops['Estimated Profit'].sum()
    st.metric("💰 Total Expected Profit", f"₹{total:,.2f}")
    
    st.markdown("---")
    st.subheader("Delete Crop Record")
    
    if len(my_crops) > 0:
        # Create a list of crops with index
        crop_options = [f"{idx+1}. {row['Crop Name']} - {row['Field Size (acres)']} acres" 
                       for idx, row in my_crops.iterrows()]
        
        selected_option = st.selectbox("Select crop to delete", [""] + crop_options + ["Delete All"])
        
        if selected_option and selected_option != "":
            if selected_option == "Delete All":
                if st.button("🗑️ Delete All My Crops", type="primary"):
                    df = df[df["username"] != user["username"]]
                    df.to_csv(FARMER_CROPS_CSV, index=False)
                    st.success("✅ All your crops have been deleted!")
                    st.rerun()
            else:
                # Extract index from option
                crop_idx = int(selected_option.split(".")[0]) - 1
                row_to_delete = my_crops.iloc[crop_idx]
                
                st.warning(f"Delete: {row_to_delete['Crop Name']} ({row_to_delete['Field Size (acres)']} acres)")
                
                if st.button("🗑️ Delete This Crop", type="primary"):
                    match = (
                        (df["username"] == user["username"]) &
                        (df["Crop Name"] == row_to_delete["Crop Name"]) &
                        (df["Field Size (acres)"] == row_to_delete["Field Size (acres)"]) &
                        (df["Profit Per Acre"] == row_to_delete["Profit Per Acre"]) &
                        (df["Estimated Profit"] == row_to_delete["Estimated Profit"])
                    )
                    df = df[~match]
                    df.to_csv(FARMER_CROPS_CSV, index=False)
                    st.success(f"✅ Crop '{row_to_delete['Crop Name']}' deleted!")
                    st.rerun()

def my_profile_page():
    st.title("👤 My Profile")
    
    user = st.session_state.user
    farmers = load_farmers()
    
    if farmers.empty or user["username"] not in farmers["username"].values:
        st.info("No profile information found. Create your profile below.")
        create_profile = True
    else:
        create_profile = False
        farmer_row = farmers[farmers["username"] == user["username"]].iloc[0]
    
    st.markdown("---")
    
    if create_profile:
        st.subheader("Create/Update Profile")
        with st.form("profile_form"):
            name = st.text_input("Full Name", value=user["name"])
            location = st.text_input("Location")
            contact = st.text_input("Contact Number (10 digits)")
            
            if st.form_submit_button("Save Profile"):
                if len(contact) != 10 or not contact.isdigit():
                    st.error("❌ Contact must be exactly 10 digits!")
                else:
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
                    st.success("✅ Profile saved successfully!")
                    st.rerun()
    else:
        st.subheader("Update Profile")
        with st.form("update_profile_form"):
            name = st.text_input("Full Name", value=farmer_row["name"])
            location = st.text_input("Location", value=farmer_row["location"])
            contact = st.text_input("Contact Number", value=farmer_row["contact"])
            
            if st.form_submit_button("Update Profile"):
                if len(contact) != 10 or not contact.isdigit():
                    st.error("❌ Contact must be exactly 10 digits!")
                else:
                    idx = farmers.index[farmers["username"] == user["username"]][0]
                    farmers.at[idx, "name"] = name
                    farmers.at[idx, "location"] = location
                    farmers.at[idx, "contact"] = contact
                    save_farmers(farmers)
                    st.success("✅ Profile updated successfully!")
                    st.rerun()
    
    st.markdown("---")
    st.subheader("⚠️ Danger Zone")
    
    with st.expander("Delete My Account"):
        st.warning("This will permanently delete your account and all associated data!")
        
        confirm_delete = st.checkbox("I understand this action cannot be undone")
        
        if confirm_delete:
            if st.button("🗑️ Delete My Account", type="primary"):
                # Delete user
                users = load_users()
                users = users[users["username"] != user["username"]]
                save_users(users)
                
                # Delete farmer record
                farmers = load_farmers()
                farmers = farmers[farmers["username"] != user["username"]]
                save_farmers(farmers)
                
                # Delete crop records
                if os.path.exists(FARMER_CROPS_CSV):
                    df = pd.read_csv(FARMER_CROPS_CSV)
                    df = df[df["username"] != user["username"]]
                    df.to_csv(FARMER_CROPS_CSV, index=False)
                
                st.success("✅ Your account has been deleted.")
                logout()

# Main App
def main():
    ensure_data_files()
    
    if st.session_state.user is None:
        if st.session_state.page == 'login':
            login_page()
        else:
            registration_page()
    else:
        if st.session_state.user['role'] == 'admin':
            admin_dashboard()
        else:
            farmer_dashboard()

if __name__ == "__main__":
    main()
