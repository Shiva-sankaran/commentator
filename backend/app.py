import pymongo
from flask import Flask, jsonify, render_template, request, json, session, send_from_directory
from flask_session import Session

from passlib.hash import sha256_crypt
from functools import wraps
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)

cors = CORS(app, resources={
            r"/register": {"origins": "http://127.0.0.1:5000"}}, static_folder='../frontend/build')
app.config.from_pyfile('config.py')
Session(app)

sess = Session()
sess.init_app(app)


# conn_str = "mongodb+srv://annotation_user:pwKzLUGrQxpd3UnD@annotation.lamba.mongodb.net/test"
conn_str = "mongodb+srv://annotation_user:pwKzLUGrQxpd3UnD@annotation.lamba.mongodb.net/annotation_tool?retryWrites=true&w=majority"
# set a 5-second connection timeout
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
database = client['annotation_tool']
try:
    print("\nConnected to the db.\n")
except Exception:
    print("Unable to connect to the server.")


@app.route('/signup', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def register():
    user_collection = database.get_collection('users')
    requestdata = json.loads(request.data)
    requestdata = json.loads(requestdata['body'])
    # print(requestdata, type(requestdata))
    # print()
    # for elem in requestdata:
    #     print(elem)
    username = requestdata['username']
    password = sha256_crypt.encrypt(str(requestdata['password']))
    print(username, password)

    result = user_collection.find({'username': username})
    res = list(result)
    print('Res: ', res, '\tType: ', type(res))
    print(res.__len__())
    if res.__len__() > 0:
        return jsonify({"error_message": "The username has already been taken"})
    else:
        user_collection.insert_one(
            {'username': username, 'password': password, 'sentId': 0, 'sentTag': []})

        result = {
            'username': username,
            'password': password,
            'message': "Your account has been created. Please Login!"
        }
        return jsonify({'result': result})
    # return jsonify({'result': requestdata})


@app.route('/login', methods=['POST'])
def login():
    user_collection = database.get_collection('users')

    requestdata = json.loads(request.data)
    requestdata = json.loads(requestdata['body'])

    username = requestdata['username']
    password = str(requestdata['password'])
    print(username, password)

    result = user_collection.find({'username': username})
    res = list(result)
    print('Res: ', res, '\tType: ', type(res))
    print(res.__len__())
    if res.__len__() > 0:
        data = res[0]
        print(data['password'])
        sentId = data['sentId']
        print(sentId)
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
    sentences_collection = database.get_collection('sentences')
    requestdata = json.loads(request.data)
    print(requestdata)
    requestdata = json.loads(requestdata['body'])

    sentId = requestdata['id']
    print(sentId)
    result = sentences_collection.find({'sid': sentId})
    data = list(result)
    data = data[0]
    sentence = data['sentence']
    result = {
        'sentence': sentence,
        'sentId': sentId,
        'message': "Sentence Fetched Successfully."
    }
    return jsonify({'result': result})


@app.route('/submit-sentence', methods=['POST'])
# @is_logged_in
def submit_sentence():
    user_collection = database.get_collection('users')
    requestdata = json.loads(request.data)
    print(requestdata)
    requestdata = json.loads(requestdata['body'])

    sentId = requestdata['sentId']
    selected = requestdata['selected']
    tag = requestdata['tag']
    username = requestdata['username']
    date = requestdata['date']

    lst = [selected, date, tag]
    print(lst)

    print(sentId, selected, tag, username)

    user_collection.update_one({'username': username}, {
        '$set': {'sentId': sentId},
        '$push': {'sentTag': lst}
    })

    return jsonify({'result': 'Message Stored Successfully'})


@app.route('/submit-edit-sentence', methods=['POST'])
# @is_logged_in
def submit_edit_sentence():
    user_collection = database.get_collection('users')
    requestdata = json.loads(request.data)
    print(requestdata)
    requestdata = json.loads(requestdata['body'])

    sentId = requestdata['sentId']
    selected = requestdata['selected']
    tag = requestdata['tag']
    username = requestdata['username']
    date = requestdata['date']

    lst = [selected, date, tag]
    print(lst)

    print(sentId, selected, tag, username)

    user_collection.update_one({'username': username, 'sentTag[0]': ''}, {
        '$set': {'sentId': sentId},
        '$push': {'sentTag': lst}
    })

    return jsonify({'result': 'Message Stored Successfully'})


@app.route('/all-sentences', methods=['POST'])
# @is_logged_in
def all_sentence():
    user_collection = database.get_collection('users')
    requestdata = json.loads(request.data)
    print(requestdata)
    requestdata = json.loads(requestdata['body'])

    username = json.loads(requestdata['username'])

    print('username: ', username)

    result = user_collection.find({'username': username})
    print(result)
    res = list(result)
    res = res[0]
    print(res)

    return jsonify({'result': res['sentTag']})


if __name__ == '__main__':
    app.run(debug=True)
