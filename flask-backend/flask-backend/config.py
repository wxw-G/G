import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'wxw2004'
    MYSQL_DB = 'webgis'
    MYSQL_CURSORCLASS = 'DictCursor'