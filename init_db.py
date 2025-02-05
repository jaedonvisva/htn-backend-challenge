import json
import sqlite3
from datetime import datetime, timezone

# Load JSON data
with open("data/participants.json", "r") as file:
    data = json.load(file)

# Connect to SQLite database
conn = sqlite3.connect("hackathon.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    badge_code TEXT PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    updated_at TEXT
);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    badge_code TEXT,
    activity_name TEXT,
    activity_category TEXT,
    scanned_at TEXT,
    FOREIGN KEY (badge_code) REFERENCES users (badge_code)
);
""")

# Insert data into tables
for entry in data:
    name = entry["name"]
    email = entry["email"]
    phone = entry["phone"]
    badge_code = entry["badge_code"]
    updated_at = datetime.now(timezone.utc).isoformat()

    if badge_code:  # Ensure badge_code is not empty
        # Insert attendee into users table
        cursor.execute("""
            INSERT OR IGNORE INTO users (badge_code, name, email, phone, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (badge_code, name, email, phone, updated_at))

        # Insert scans
        for scan in entry["scans"]:
            cursor.execute("""
                INSERT INTO scans (badge_code, activity_name, activity_category, scanned_at)
                VALUES (?, ?, ?, ?)
            """, (badge_code, scan["activity_name"], scan["activity_category"], scan["scanned_at"]))

# Commit and close connection
conn.commit()
conn.close()

print("Database created successfully!")
