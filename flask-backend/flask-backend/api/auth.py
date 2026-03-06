from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors

# 创建蓝图
auth_bp = Blueprint('auth', __name__)
disaster_bp = Blueprint('disaster', __name__)
shelter_bp = Blueprint('shelter', __name__)

def get_db():
    from app import mysql  # 从主app导入mysql实例
    return mysql.connection

### 用户认证相关路由 ###
@auth_bp.route('/register', methods=['POST'])
def register():
    # 1. 获取数据
    data = request.get_json()
    username = data.get('username', '').strip()  # 去除前后空格
    password = data.get('password', '').strip()
    email = data.get('email', '').strip()  # 获取邮箱字段

    # 2. 基本验证
    if not username or not password or not email:
        return jsonify({"status": "error", "message": "用户名、密码和邮箱不能为空"}), 400

    if len(password) < 6:
        return jsonify({"status": "error", "message": "密码至少需要6位"}), 400

    try:
        # 3. 数据库操作
        with get_db().cursor() as cur:
            # 直接存储明文密码
            cur.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                (username, password, email)  # 将明文密码存储到数据库
            )
            get_db().commit()

        # 4. 返回成功响应
        return jsonify({
            "status": "success",
            "message": "注册成功",
            "data": {"username": username, "email": email}
        }), 201

    except Exception as e:
        get_db().rollback()
        return jsonify({"status": "error", "message": "注册失败"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "error", "message": "用户名和密码是必填项！"}), 400

    try:
        conn = get_db()
        cur = conn.cursor(MySQLdb.cursors.DictCursor)

        # 查询用户，直接比较明文密码
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()

        if not user:
            return jsonify({"status": "error", "message": "用户名或密码错误！"}), 401

        # 设置会话
        session['user_id'] = user['id']
        session['username'] = user['username']

        return jsonify({
            "status": "success",
            "message": "登录成功！",
            "user": {
                "id": user['id'],
                "username": user['username'],
                "email": user['email']
            }
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": f"登录失败: {str(e)}"}), 500
    finally:
        cur.close()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"status": "success", "message": "已退出登录！"}), 200

@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        return jsonify({
            "status": "success",
            "user": {
                "id": session['user_id'],
                "username": session['username']
            }
        }), 200
    return jsonify({"status": "error", "message": "未登录"}), 401

### 灾害数据相关路由 ###
@disaster_bp.route('/disaster-list', methods=['GET'])
def get_disaster_list():
    cursor = None
    try:
        conn = get_db()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        # 安全起见，明确指定字段
        cursor.execute("""
            SELECT 
                id,
                location_name AS name,
                disaster_type AS type,
                description,
                timestamp AS time,
                CONCAT(latitude, ',', longitude) AS coordinates
            FROM disaster_locations
        """)

        data = cursor.fetchall()

        # 确保时间可序列化
        for item in data:
            if 'time' in item and item['time']:
                item['time'] = item['time'].isoformat()

        return jsonify({
            "status": "success",
            "data": data,
            "count": len(data)
        })

    except MySQLdb.OperationalError as e:
        return jsonify({
            "status": "error",
            "message": "Database connection failed",
            "detail": str(e)
        }), 500
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Server error",
            "detail": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()


@disaster_bp.route('/disaster-list', methods=['POST'])
def add_disaster():
    data = request.get_json()
    location_name = data.get('location_name')
    disaster_type = data.get('disaster_type')
    description = data.get('description')
    timestamp = data.get('timestamp')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not location_name or not disaster_type or not description or not timestamp or not latitude or not longitude:
        return jsonify({"status": "error", "message": "缺少必填字段"}), 400

    try:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO disaster_locations (location_name, disaster_type, description, timestamp, latitude, longitude, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
            """,
            (location_name, disaster_type, description, timestamp, format_decimal(latitude), format_decimal(longitude))
        )
        connection.commit()
        return jsonify({
            "status": "success",
            "message": "灾害信息已添加"
        }), 201
    except Exception as e:
        connection.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()

def format_decimal(value):
    """将浮点数格式化为数据库所需的decimal(10,6)格式"""
    return format(value, ".6f")
@disaster_bp.route('/disaster-list/<int:id>', methods=['PUT'])
def update_disaster(id):
    data = request.get_json()
    location_name = data.get('location_name')
    disaster_type = data.get('disaster_type')
    description = data.get('description')
    timestamp = data.get('timestamp')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    image_path = data.get('image_path')

    if not location_name or not disaster_type or not description or not timestamp or not latitude or not longitude:
        return jsonify({"status": "error", "message": "缺少必填字段"}), 400

    try:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE disaster_locations
            SET location_name = %s, disaster_type = %s, description = %s, timestamp = %s, latitude = %s, longitude = %s, image_path = %s
            WHERE id = %s
            """,
            (location_name, disaster_type, description, timestamp, latitude, longitude, image_path, id)
        )
        connection.commit()
        return jsonify({
            "status": "success",
            "message": "受灾地点信息已更新"
        }), 200
    except Exception as e:
        connection.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()

@disaster_bp.route('/disaster-list/<int:disaster_id>', methods=['DELETE'])
def delete_disaster(disaster_id):
    try:
        connection = get_db()
        cursor = connection.cursor()
        # 执行删除操作
        cursor.execute(
            """
            DELETE FROM disaster_locations
            WHERE id = %s
            """,
            (disaster_id,)
        )
        # 提交事务
        connection.commit()
        # 检查是否有行被删除
        if cursor.rowcount == 0:
            return jsonify({"status": "error", "message": "受灾地点不存在"}), 404
        # 如果删除成功，返回成功信息
        return jsonify({
            "status": "success",
            "message": "受灾地点已删除"
        }), 200
    except Exception as e:
        # 如果发生异常，回滚事务
        connection.rollback()
        # 返回错误信息
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        # 关闭游标
        cursor.close()




# 获取所有避难所信息
@shelter_bp.route('/shelter-list', methods=['GET'])
def get_shelter_list():
    cursor = None
    try:
        conn = get_db()
        if not conn:
            return jsonify({"status": "error", "message": "无法连接数据库"}), 500

        cursor = conn.cursor(MySQLdb.cursors.DictCursor)

        # 添加调试信息
        print("尝试执行SQL查询")

        cursor.execute("""
            SELECT 
                shelter_id AS id,
                shelter_name AS name,
                address,
                capacity,
                shelter_type AS type,
                contact_number AS contact,
                latitude,
                longitude,
                is_accessible AS `accessible`,
                description,
                created_at AS created,
                updated_at AS updated
            FROM emergency_shelter
        """)

        data = cursor.fetchall()
        print(f"获取到 {len(data)} 条记录")

        # 确保时间可序列化
        for item in data:
            if 'created' in item and item['created']:
                item['created'] = item['created'].isoformat()
            if 'updated' in item and item['updated']:
                item['updated'] = item['updated'].isoformat()

        return jsonify({
            "status": "success",
            "data": data,
            "count": len(data)
        })

    except MySQLdb.OperationalError as e:
        print(f"数据库操作错误: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Database connection failed",
            "detail": str(e)
        }), 500
    except Exception as e:
        print(f"未知错误: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Server error",
            "detail": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()

# 添加避难所信息
@shelter_bp.route('/shelter-list', methods=['POST'])
def add_shelter():
    data = request.get_json()
    shelter_name = data.get('name')
    address = data.get('address')
    capacity = data.get('capacity')
    shelter_type = data.get('type')
    contact_number = data.get('contact')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    is_accessible = data.get('accessible', False)
    description = data.get('description')

    if not shelter_name or not address or capacity is None:
        return jsonify({"status": "error", "message": "缺少必填字段"}), 400

    try:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO emergency_shelter (shelter_name, address, capacity, shelter_type, contact_number, latitude, longitude, is_accessible, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (shelter_name, address, capacity, shelter_type, contact_number, latitude, longitude, is_accessible, description)
        )
        connection.commit()
        return jsonify({
            "status": "success",
            "message": "避难所信息已添加"
        }), 201
    except Exception as e:
        connection.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()

# 更新避难所信息
@shelter_bp.route('/shelter-list/<int:id>', methods=['PUT'])
def update_shelter(id):
    data = request.get_json()
    shelter_name = data.get('name')
    address = data.get('address')
    capacity = data.get('capacity')
    shelter_type = data.get('type')
    contact_number = data.get('contact')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    is_accessible = data.get('accessible', False)
    description = data.get('description')

    if not shelter_name or not address or capacity is None:
        return jsonify({"status": "error", "message": "缺少必填字段"}), 400

    try:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE emergency_shelter
            SET shelter_name = %s, address = %s, capacity = %s, shelter_type = %s, contact_number = %s, latitude = %s, longitude = %s, is_accessible = %s, description = %s
            WHERE shelter_id = %s
            """,
            (shelter_name, address, capacity, shelter_type, contact_number, latitude, longitude, is_accessible, description, id)
        )
        connection.commit()
        return jsonify({
            "status": "success",
            "message": "避难所信息已更新"
        }), 200
    except Exception as e:
        connection.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()

# 删除避难所信息
@shelter_bp.route('/shelter-list/<int:shelter_id>', methods=['DELETE'])
def delete_shelter(shelter_id):
    try:
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute(
            """
            DELETE FROM emergency_shelter
            WHERE shelter_id = %s
            """,
            (shelter_id,)
        )
        if cursor.rowcount == 0:
            return jsonify({"status": "error", "message": "未找到指定的避难所"}), 404
        connection.commit()
        return jsonify({
            "status": "success",
            "message": "避难所信息已删除"
        }), 200
    except Exception as e:
        connection.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()