import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

app = Flask(__name__)
CORS(app)  # 允许跨域访问

# 获取 MySQL 连接信息
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}

# 获取所有用户
@app.route('/users', methods=['GET'])
def get_users():
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

# 添加用户
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data['name'], data['email']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User added"}), 201

if __name__ == '__main__':
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    app.run(debug=True, port=port)
