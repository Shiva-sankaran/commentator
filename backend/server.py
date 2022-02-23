from flask import Flask, jsonify, request, json, session
from flask_session import Session
# from flask_mysqldb import MySQL
import pymysql.cursors

from passlib.hash import sha256_crypt
from functools import wraps
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)

SECRET_KEY = 'annotation_key'
SESSION_TYPE = 'filesystem'

cors = CORS(app, resources={
            r"/register": {"origins": "http://127.0.0.1:5000"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_pyfile('config.py')
Session(app)

sess = Session()
app.secret_key = SECRET_KEY
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='annotation_sql',
                             cursorclass=pymysql.cursors.DictCursor)

# Signup


@app.route('/signup', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def register():
    cur = connection.cursor()
    requestdata = json.loads(request.data)
    requestdata = json.loads(requestdata['body'])
    # print(requestdata, type(requestdata))
    # print()
    # for elem in requestdata:
    #     print(elem)
    username = requestdata['username']
    password = sha256_crypt.encrypt(str(requestdata['password']))
    print(username, password)

    result = cur.execute(
        'SELECT username FROM users WHERE username=%s', [username])
    if result > 0:
        return jsonify({"error_message": "The username has already been taken"})
    else:
        cur.execute("INSERT INTO users(username, password) VALUES( %s, %s)",
                    (username, password))
        connection.commit()

        result = {
            'username': username,
            'password': password,
            'message': "Your account has been created.Please Login!!"
        }
        cur.close()
        return jsonify({'result': result})
    # return jsonify({'result': requestdata})


@app.route('/login', methods=['POST'])
def login():
    cur = connection.cursor()
    requestdata = json.loads(request.data)
    requestdata = json.loads(requestdata['body'])
    # print(requestdata, type(requestdata))
    # print()
    # for elem in requestdata:
    #     print(elem)
    username = requestdata['username']
    # username = requestdata['username']
    # password = sha256_crypt.hash(str(requestdata['password']))
    password = str(requestdata['password'])
    print(username, password)

    result = cur.execute("SELECT * FROM Users WHERE username = %s", [username])
    sentId = 0
    if result > 0:
        data = cur.fetchone()
        print(data['password'])
        sentId = data['sentId']
        print(data['sentId'])
        print(sha256_crypt.verify(password, data['password']))
        # userID = data['id']
        # role = data['role']

        if sha256_crypt.verify(password, data['password']):
            session['logged_in'] = True
            session['username'] = username
            # session['role'] = role
            # session['user_id'] = userID

            # return jsonify({ 'response': 'Login successful' })
        else:
            error = 'Invalid Password'
            return jsonify({'error': error})
        cur.close()

    else:
        error = 'Username not found'
        return jsonify({'error': error})

    returning = {
        # 'userId': session['user_id'],
        'username': session['username'],
        'sentId': sentId
    }
    return jsonify({'success': returning})


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return jsonify({'message': "You are not logged in!"})
    return wrap


@app.route('/logout', methods=['POST'])
@is_logged_in
def logout():
    session.clear()
    return jsonify({'message': "You are logged out"})


@app.route('/get-sentence', methods=['POST'])
# @is_logged_in
def get_sentence():
    cur = connection.cursor()
    requestdata = json.loads(request.data)
    print(requestdata)
    return requestdata


if __name__ == '__main__':
    app.run(debug=True)
