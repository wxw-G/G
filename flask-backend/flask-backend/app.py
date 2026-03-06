import traceback
from datetime import timedelta
from flask import Flask, jsonify
from flask_cors import CORS

from api.auth import auth_bp, disaster_bp, shelter_bp
from config import Config
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 启用 CORS 并允许携带凭证
app.config.from_object(Config)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=0.01)  # 10秒后过期

# 初始化 MySQL
mysql = MySQL(app)

@app.errorhandler(500)
def internal_error(error):
    tb = traceback.format_exc()
    app.logger.error(tb)
    return jsonify({"status": "error", "message": "Internal Server Error", "detail": tb}), 500

@app.route('/')
def db_connect_and_get_users():
    try:
        # 尝试获取数据库连接
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        cur.close()

        if not result:
            return jsonify({"status": "error", "message": "Failed to connect to database!"})

        # 查询用户表中的数据
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()

        return jsonify({"status": "success", "message": "Database connection successful!", "users": users})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Error connecting to database or fetching users: {str(e)}"})

# 注册 auth 蓝图
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(disaster_bp, url_prefix='/auth')
app.register_blueprint(shelter_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)