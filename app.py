from flask import Flask, request, jsonify
import duckdb

app = Flask(__name__)

# Connect to DuckDB and load the data
con = duckdb.connect(database=':memory:')
with open('/Users/arnavsahai/Desktop/Arnav_Charlotte_API/arnav_charlotte_api/setup_database.sql', 'r') as f:
    con.execute(f.read())

@app.route("/", methods=["GET"])
def get_universities():
    """Fetches all universities."""
    universities = con.execute("SELECT * FROM universities").fetchall()
    columns = [desc[0] for desc in con.description]
    result = [dict(zip(columns, row)) for row in universities]
    return jsonify(result)

@app.route("/university/<int:univ_id>", methods=["GET"])
def get_university(univ_id):
    """Fetch a single university by ID."""
    university = con.execute("SELECT * FROM universities WHERE Rank = ?", [univ_id]).fetchone()
    if not university:
        return jsonify({"error": "University not found"}), 404
    columns = [desc[0] for desc in con.description]
    result = dict(zip(columns, university))
    return jsonify(result)

@app.route("/users", methods=["POST"])
def add_user():
    """Add a new user."""
    data = request.get_json()
    username = data.get('username')
    age = data.get('age')
    country = data.get('country')
    
    if not username or not age or not country:
        return jsonify({"error": "Missing data"}), 400
    
    try:
        con.execute("INSERT INTO users (username, age, country) VALUES (?, ?, ?)", (username, age, country))
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    return jsonify({"message": "User added successfully"}), 201

@app.route("/user_stats", methods=["GET"])
def get_user_stats():
    """Get user statistics."""
    num_users = con.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    avg_age = con.execute("SELECT AVG(age) FROM users").fetchone()[0]
    top_countries = con.execute("SELECT country, COUNT(*) as count FROM users GROUP BY country ORDER BY count DESC LIMIT 3").fetchall()
    
    result = {
        "number_of_users": num_users,
        "average_age": avg_age,
        "top_countries": [country for country, count in top_countries]
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5001)