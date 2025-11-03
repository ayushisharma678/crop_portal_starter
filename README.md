# Crop Management Portal (CLI, Python)

A beginner-friendly **Command Line Interface (CLI)** portal with **Admin** and **Client (Farmer)** roles.
Data is stored in simple **CSV files** using **Pandas**. This is a perfect starting point for a team project with clear CRUD operations.

---

## 🧰 Prerequisites
- Python 3.10+
- Git (optional but recommended)
- VS Code (recommended)

---

## 🚀 Quick Start

```bash
# 1) Create & activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the app
python src/main.py
```

Default **admin** login:
- username: `admin`
- password: `admin123`

> You can change or add more admins in `data/users.csv` (passwords are stored as hashes).

---

## 📁 Project Structure

```
crop_portal_starter/
├─ data/
│  ├─ farmers.csv
│  └─ users.csv
├─ src/
│  ├─ main.py
|  ├─ frontend.py
│  ├─ storage.py
│  └─ security.py
├─ .gitignore
├─ requirements.txt
└─ README.md
```

---

## 🧪 What can you do now?
- Login as **admin** to manage crops and view farmers
- Register/login as **client (farmer)** to add/update/delete your crop record
- Practice **CRUD** on both datasets
- Push your project to **GitHub**

---

## 🧩 Team Work Ideas
- Member 1: Client auth (register/login)
- Member 2: Crop CRUD (admin)
- Member 3: Farmer record CRUD (client)
- Member 4: Reports (e.g., most grown crop, avg price)

---

## 🛠️ Extend Later (Optional)
- Replace CSV with **SQLite** (via `sqlite3` or SQLAlchemy)
- Add **input validation** and better error handling
- Add **reports**: top crops by season/location
- Add **export** to Excel
```bash
pip install openpyxl
```
- Switch CLI to a simple web app using **Flask**

Happy hacking! 🌱
