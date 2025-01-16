from flask import Flask, jsonify, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)


# MySQL database connection, add your credentials
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='pass',
        database='user_db'
    )


@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)


@app.route('/user', methods=['POST'])
def create_user():
    new_user = request.json
    name = new_user.get('name')
    dob_str = new_user.get('dob')
    dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, dob) VALUES (%s, %s)', (name, dob))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User created successfully!"}), 201


@app.route('/user/<identifier>', methods=['PUT'])
def update_user(identifier):
    updated_user = request.json
    new_name = updated_user.get('name')
    dob_str = updated_user.get('dob')
    dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

    conn = get_db_connection()
    cursor = conn.cursor()

    if identifier.isdigit():  # If the identifier is an ID
        cursor.execute('UPDATE users SET name = %s, dob = %s WHERE id = %s', (new_name, dob, identifier))
    else:  # If the identifier is a Name
        cursor.execute('UPDATE users SET name = %s, dob = %s WHERE name = %s', (new_name, dob, identifier))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User updated successfully!"})


@app.route('/user/<identifier>', methods=['DELETE'])
def delete_user(identifier):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if identifier.isdigit():  # If the identifier is an ID
            cursor.execute('DELETE FROM users WHERE id = %s', (identifier,))
        else:  # If the identifier is a Name
            cursor.execute('DELETE FROM users WHERE name = %s', (identifier,))

        if cursor.rowcount > 0:
            conn.commit()
            response = {"message": "User deleted successfully!"}
        else:
            response = {"message": "User not found!"}

        cursor.close()
        conn.close()
        return jsonify(response)

    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


