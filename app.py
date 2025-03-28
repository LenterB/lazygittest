from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # 允许跨域访问

# 连接 MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="test_db"
)
cursor = db.cursor(dictionary=True)

# 获取所有用户
@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return jsonify(users)

# 添加用户
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data['name'], data['email']))
    db.commit()
    return jsonify({"message": "User added"}), 201

if __name__ == '__main__':
    app.run(debug=True)
