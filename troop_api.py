# Adapted from Homework 2 (Zoo API) for Exam 1 - Troop API

from flask import Flask, request, jsonify
import creds
from sql import create_connection

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def index():
    return "Troop API is running"

# POST endpoint to add new troop
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

# DELETE endpoint to remove a troop by leader_email
# Adapted from Homework 2 (Zoo API) for Exam 1 - Troop API
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

# Now the app starts after all routes are defined
if __name__ == '__main__':
    app.run()
