import pyodbc as odbc
from flask import Flask, request, jsonify, render_template
from flask import session as login_session

app = Flask(__name__)

connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:sql-auth.database.windows.net,1433;Database=account;Uid=admin1;Pwd=Passw0rd;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
conn = odbc.connect(connection_string)

cursor = conn.cursor()


def admin():
    d = dict()
    connection_string = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:sql-auth.database.windows.net,1433;Database=account;Uid=admin1;Pwd=Passw0rd;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    SQL_QUERY = """
    SELECT * FROM user_details;
    """
    cursor.execute(SQL_QUERY)
    records = cursor.fetchall()
    conn.close()
    for r in records:
        d[r.email] = r.password
    return d


def insert_user_password(username, password):
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_details (email, password) VALUES (?, ?)",
        username,
        password,
    )
    conn.commit()
    conn.close()


def check_username_password(username, password):
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM user_details WHERE email = ? AND password = ?",
        username,
        password,
    )
    result = cursor.fetchone()
    conn.close()

    return result is not None


def update_password(username, new_password):
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_details SET password = ? WHERE email = ?", new_password, username
    )
    conn.commit()
    conn.close()
    print("updated Sucessfully")


def update_user_password(username, new_password):
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_details SET password = ? WHERE email = ?", new_password, username
    )
    conn.commit()
    conn.close()
    print("updated Successfully")


@app.route("/login", methods=["POST"])
def login():
    print("hi")
    data = request.get_json()  # Get the JSON data from the request
    username = data.get("email")  # Extract username from JSON data
    password = data.get("password")  # Extract password from JSON data
    print(username + "hi")
    if username and password:  # Check if both username and password are provided
        if check_username_password(username, password):
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Invalid username or password"}), 401
    else:
        return jsonify({"message": "Invalid Input"}), 400


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()  # Get the JSON data from the request
    username = data.get("email")  # Extract username from JSON data
    password = data.get("password")  # Extract password from JSON data

    if username and password:  # Check if both username and password are provided
        insert_user_password(username, password)  # Insert user details
        return jsonify({"message": "Signup successful"}), 201
    else:
        return jsonify({"message": "Invalid Input"}), 400


@app.route("/update_password", methods=["POST"])
def update_password():
    data = request.get_json()  # Get the JSON data from the request
    username = data.get("email")  # Extract username from JSON data
    new_password = data.get("new_password")  # Extract new password from JSON data

    if (
        username and new_password
    ):  # Check if both username and new password are provided
        update_user_password(username, new_password)  # Update the password
        return jsonify({"message": "Password updated successfully"}), 200
    else:
        return jsonify({"message": "Invalid Input"}), 400


@app.route("/admin")
def admin_page():
    d = dict()
    d = admin()
    return render_template("admin.html", data=d)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
