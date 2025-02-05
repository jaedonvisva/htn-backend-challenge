from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime, timezone

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect("hackathon.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- All Users Endpoint ----------------
@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    
    users = conn.execute("SELECT * FROM users").fetchall()
    
    user_data = []
    for user in users:
        scans = conn.execute("""
            SELECT activity_name, scanned_at, activity_category 
            FROM scans WHERE badge_code = ?
        """, (user["badge_code"],)).fetchall()
        
        user_dict = dict(user)
        user_dict["scans"] = [dict(scan) for scan in scans]
        user_data.append(user_dict)

    conn.close()
    return jsonify(user_data)

# ---------------- User Information Endpoint ----------------
@app.route("/users/<string:badge_code>", methods=["GET"])
def get_attendee_with_scans(badge_code):
    conn = get_db_connection()
    
    user = conn.execute("SELECT * FROM users WHERE badge_code = ?", (badge_code,)).fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "Attendee not found"}), 404

    scans = conn.execute("""
        SELECT activity_name, scanned_at, activity_category 
        FROM scans WHERE badge_code = ?
    """, (badge_code,)).fetchall()

    conn.close()
    
    user_data = dict(user)
    user_data["scans"] = [dict(scan) for scan in scans]
    return jsonify(user_data)

# ---------------- Updating User Data Endpoint ----------------
@app.route("/users/<string:badge_code>", methods=["PUT"])
def update_user(badge_code):
    conn = get_db_connection()
    
    user = conn.execute("SELECT * FROM users WHERE badge_code = ?", (badge_code,)).fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    
    # Update fields dynamically
    update_fields = []
    values = []
    for key, value in data.items():
        if key in ["name", "email", "phone"]:
            update_fields.append(f"{key} = ?")
            values.append(value)
    
    if not update_fields:
        conn.close()
        return jsonify({"error": "No valid fields to update"}), 400

    values.append(datetime.now(timezone.utc).isoformat())  # Updating `updated_at`
    values.append(badge_code)
    
    query = f"UPDATE users SET {', '.join(update_fields)}, updated_at = ? WHERE badge_code = ?"
    conn.execute(query, values)
    conn.commit()

    updated_user = conn.execute("SELECT * FROM users WHERE badge_code = ?", (badge_code,)).fetchone()
    conn.close()
    
    return jsonify(dict(updated_user))

# ---------------- Add Scan Endpoint ----------------
@app.route("/scan/<string:badge_code>", methods=["POST"])
def add_scan(badge_code):
    conn = get_db_connection()
    
    user = conn.execute("SELECT * FROM users WHERE badge_code = ?", (badge_code,)).fetchone()
    if not user:
        conn.close()
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    activity_name = data.get("activity_name")
    activity_category = data.get("activity_category")

    if not activity_name or not activity_category:
        conn.close()
        return jsonify({"error": "Missing activity_name or activity_category"}), 400

    scanned_at = datetime.now(timezone.utc).isoformat()

    conn.execute("""
        INSERT INTO scans (badge_code, activity_name, scanned_at, activity_category)
        VALUES (?, ?, ?, ?)
    """, (badge_code, activity_name, scanned_at, activity_category))

    conn.execute("""
        UPDATE users SET updated_at = ? WHERE badge_code = ?
    """, (scanned_at, badge_code))

    conn.commit()
    conn.close()

    return jsonify({
        "badge_code": badge_code,
        "activity_name": activity_name,
        "scanned_at": scanned_at,
        "activity_category": activity_category
    }), 201

# ---------------- Scan Data Endpoint ----------------
@app.route("/scans", methods=["GET"])
def get_scan_statistics():
    conn = get_db_connection()

    min_frequency = request.args.get("min_frequency", type=int)
    max_frequency = request.args.get("max_frequency", type=int)
    activity_category = request.args.get("activity_category")

    query = """
        SELECT activity_name, activity_category, COUNT(*) as frequency 
        FROM scans
    """
    conditions = []
    values = []

    if activity_category:
        conditions.append("activity_category = ?")
        values.append(activity_category)

    query += " GROUP BY activity_name, activity_category"

    having_conditions = []
    if min_frequency:
        having_conditions.append("COUNT(*) >= ?")
        values.append(min_frequency)
    
    if max_frequency:
        having_conditions.append("COUNT(*) <= ?")
        values.append(max_frequency)

    if having_conditions:
        query += " HAVING " + " AND ".join(having_conditions)

    query += " ORDER BY frequency DESC"

    scans = conn.execute(query, values).fetchall()
    conn.close()

    return jsonify([dict(scan) for scan in scans])


if __name__ == "__main__":
    app.run(debug=True)
