import os

DEBUG = True
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = os.getenv('MYSQL_PWD')
MYSQL_DB = 'annotation_sql'
MYSQL_CURSORCLASS = 'DictCursor'
SECRET_KEY = 'your_secret_key'