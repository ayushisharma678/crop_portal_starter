import os
import pandas as pd

# ----------------- File Paths -----------------

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
USERS_CSV = os.path.join(DATA_DIR, "users.csv")
FARMERS_CSV = os.path.join(DATA_DIR, "farmers.csv")
CROP_PROFIT_CSV = os.path.join(DATA_DIR, "crop_profit_data.csv")
CROP_DETAILS_CSV = os.path.join(DATA_DIR, "crop_details.csv")

# ----------------- Ensure Data Files -----------------

def ensure_data_files():
    """Create data directory and CSV files with headers if they don't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    files_headers = [
        (USERS_CSV, "user_id,username,role,name,password_hash,salt\n"),
        (FARMERS_CSV, "farmer_id,username,name,location,contact\n"),
        (CROP_PROFIT_CSV, "Crop Name,Profit Per Acre,Season\n"),
        (CROP_DETAILS_CSV, "Crop Name,Description\n"),
        (os.path.join(DATA_DIR, "farmer_crops.csv"), 
         "username,Crop Name,Field Size (acres),Profit Per Acre,Estimated Profit\n"),
    ]
    
    for path, header in files_headers:
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(header)


# ----------------- Load & Save Functions -----------------

def load_csv(path: str) -> pd.DataFrame:
    ensure_data_files()
    return pd.read_csv(path, dtype=str)

def save_csv(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)

def load_users() -> pd.DataFrame:
    return load_csv(USERS_CSV)

def save_users(df: pd.DataFrame):
    save_csv(df, USERS_CSV)

def load_crops() -> pd.DataFrame:
    """Load farmer_crops.csv data"""
    farmer_crops_path = os.path.join(DATA_DIR, "farmer_crops.csv")
    if os.path.exists(farmer_crops_path):
        return pd.read_csv(farmer_crops_path, dtype=str)
    return pd.DataFrame()

def save_crops(df: pd.DataFrame):
    """Save farmer_crops.csv data"""
    farmer_crops_path = os.path.join(DATA_DIR, "farmer_crops.csv")
    save_csv(df, farmer_crops_path)


def load_farmers() -> pd.DataFrame:
    return load_csv(FARMERS_CSV)

def save_farmers(df: pd.DataFrame):
    save_csv(df, FARMERS_CSV)

def load_crop_profit() -> pd.DataFrame:
    return load_csv(CROP_PROFIT_CSV)

def save_crop_profit(df: pd.DataFrame):
    save_csv(df, CROP_PROFIT_CSV)

def load_crop_details() -> pd.DataFrame:
    return load_csv(CROP_DETAILS_CSV)

def save_crop_details(df: pd.DataFrame):
    save_csv(df, CROP_DETAILS_CSV)

# ----------------- Utility -----------------

def next_id(df: pd.DataFrame, col_name: str) -> int:
    """Get the next integer ID for a column. Returns 1 if empty."""
    if df.empty:
        return 1
    try:
        return int(df[col_name].astype(int).max()) + 1
    except Exception:
        return len(df) + 1
