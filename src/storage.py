import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
USERS_CSV = os.path.join(DATA_DIR, "users.csv")
CROPS_CSV = os.path.join(DATA_DIR, "crops.csv")
FARMERS_CSV = os.path.join(DATA_DIR, "farmers.csv")

def ensure_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    for path, header in [
        (USERS_CSV, "user_id,username,role,name,password_hash,salt\n"),
        (CROPS_CSV, "crop_id,crop_name,season,price_per_quintal,fertilizer,water_needs\n"),
        (FARMERS_CSV, "farmer_id,username,name,location,crop_grown,quantity_quintal,contact\n"),
    ]:
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(header)

def load_users() -> pd.DataFrame:
    ensure_data_files()
    return pd.read_csv(USERS_CSV, dtype=str)

def save_users(df: pd.DataFrame):
    df.to_csv(USERS_CSV, index=False)

def load_crops() -> pd.DataFrame:
    ensure_data_files()
    return pd.read_csv(CROPS_CSV, dtype=str)

def save_crops(df: pd.DataFrame):
    df.to_csv(CROPS_CSV, index=False)

def load_farmers() -> pd.DataFrame:
    ensure_data_files()
    return pd.read_csv(FARMERS_CSV, dtype=str)

def save_farmers(df: pd.DataFrame):
    df.to_csv(FARMERS_CSV, index=False)

def next_id(df, col_name: str) -> int:
    if df.empty:
        return 1
    try:
        return int(df[col_name].astype(int).max()) + 1
    except Exception:
        return len(df) + 1
