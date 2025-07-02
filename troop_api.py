from flask import Flask, request, jsonify
from datetime import datetime
import creds
from sql import create_connection

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def index():
    return "Troop API is running"

# POST endpoint to add a new troop
# Based on the pattern used in Homework 2 (Zoo API)
@app.route('/api/troop', methods=['POST'])
def add_troop():
    data = request.get_json()
    troop_number = data['troop_number']
    city = data['city']
    state = data['state']
    leader_name = data['leader_name']
    leader_email = data['leader_email']

    myCreds = creds.Creds()
    conn = create_connection(myCreds.hostname, myCreds.uname, myCreds.passwd, myCreds.dbname)

    if conn:
        cursor = conn.cursor()
        sql = """
            INSERT INTO Troop (troop_number, city, state, leader_name, leader_email)
            VALUES (%s, %s, %s, %s, %s)
        """
        val = (troop_number, city, state, leader_name, leader_email)
        cursor.execute(sql, val)
        conn.commit()
        conn.close()
        return "Troop added successfully.", 201
    else:
        return "Database connection error.", 500

# DELETE endpoint to remove a troop by leader email
# Also based on Homework 2, adapted to work with troop data
@app.route('/api/troop', methods=['DELETE'])
def delete_troop():
    data = request.get_json()
    leader_email = data.get('leader_email')

    if not leader_email:
        return "Missing leader_email in request", 400

    myCreds = creds.Creds()
    conn = create_connection(myCreds.hostname, myCreds.uname, myCreds.passwd, myCreds.dbname)

    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Troop WHERE leader_email = %s", (leader_email,))
        conn.commit()
        conn.close()
        return f"Troop with leader email {leader_email} deleted.", 200
    else:
        return "Database connection error.", 500

# Helper function to validate access code and check expiration date
# This is part of the extra credit for token-based access
def is_valid_access_code(access_code):
    valid_code = "BSA2025TOKEN"
    expires = datetime(2025, 12, 31, 23, 59, 59)
    return access_code == valid_code and datetime.now() <= expires

# GET endpoint to fetch a troop using the troop number
# Includes token validation as part of extra credit
@app.route('/api/troop', methods=['GET'])
def fetch_troop_by_number():
    troop_number = request.args.get('troop_number')
    access_code = request.args.get('access_code')

    if not access_code:
        return "Access code required to use this endpoint", 401

    if not is_valid_access_code(access_code):
        return "Invalid or expired access code", 403

    if not troop_number:
        return "Missing troop_number query parameter", 400

    myCreds = creds.Creds()
    conn = create_connection(myCreds.hostname, myCreds.uname, myCreds.passwd, myCreds.dbname)

    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Troop WHERE troop_number = %s", (troop_number,))
        troop = cursor.fetchone()
        conn.close()

        if troop:
            return jsonify(troop), 200
        else:
            return f"No troop found with number {troop_number}", 404
    else:
        return "Database connection error.", 500

# Start the Flask app
if __name__ == '__main__':
    app.run()
