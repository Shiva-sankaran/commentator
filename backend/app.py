import string
import sys
import pymongo
from flask import Flask, jsonify, redirect, render_template, request, json, session, send_from_directory
from flask_session import Session
import pandas as pd

from passlib.hash import sha256_crypt
from functools import wraps
import json
from flask_cors import CORS, cross_origin
import os
import subprocess

app = Flask(__name__)

cors = CORS(app, resources={
            r"/register": {"origins": "*"}}, static_folder='../frontend/build')
app.config.from_pyfile('config.py')
Session(app)

sess = Session()
sess.init_app(app)

frontend = 'http://localhost:3000'
# conn_str = os.environ.get("DATABASE_URL")
conn_str = "mongodb+srv://annotation_user:pwKzLUGrQxpd3UnD@annotation.lamba.mongodb.net/annotation_tool?retryWrites=true&w=majority"

# set a 5-second connection timeout
client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
database = client['annotation_tool']
try:
    print("\nConnected to the db.\n")
except Exception:
    print("Unable to connect to the server.")


@app.route('/test', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def test():
    return jsonify({'result': 'Hello World'})


@app.route('/signup', methods=['GET', 'POST'])
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
            {'username': username, 'password': password, 'sentId': 0, 'admin': False, 'sentTag': []})

        result = {
            'username': username,
            'password': password,
            'message': "Your account has been created. Please Login!"
        }
        return jsonify({'result': result})
    # return jsonify({'result': requestdata})


@app.route('/login', methods=['GET', 'POST'])
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
        admin = data['admin'] if data['admin'] else False
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
        'sentId': sentId,
        'admin': admin
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

    # os.system("/LID_tool/getLanguage.py sampleinp.txt")

    result = {
        'sentence': sentence,
        'sentId': sentId,
        'message': "Sentence Fetched Successfully."
    }
    return jsonify({'result': result})


@app.route('/get-lid-data', methods=['POST'])
def lid_tag():
    # from LID_tool.getLanguage import langIdentify

    requestdata = json.loads(request.data)
    print(requestdata)
    requestdata = json.loads(requestdata['body'])

    sid = requestdata['sentId']
    print('SENTENCE = ', sid)

    # lang = langIdentify(sentence, 'classifiers/HiEn.classifier')
    # tags = []
    # print(lang)
    # for elem in lang:
    #     inter = [elem[0]]
    #     for i in range(1, len(elem)):
    #         if elem[i] is '1':
    #             inter.append(elem[i-1][0])
    #     if len(inter) == 1:
    #         inter.append('u')
    #     tags.append(inter)

    # print('LANGUAGE TAG = ', tags)
    lid_collection = database.get_collection('lid')
    prev = lid_collection.find()
    prev = list(prev)
    print(prev)
    tags = prev[int(sid)-1]['tags']
    return jsonify({'result': tags})


@app.route('/admin-file-upload', methods=['POST'])
def admin_file_upload():
    # requestdata = json.loads(request.data)
    # print(requestdata)
    print(request.files['file'])
    file = request.files['file']
    file.save('uploads/{}'.format(file.filename))
    # requestdata = json.loads(requestdata['body'])

    # file = requestdata['file']
    # print('FILE = ', file)
    import pandas as pd
    # os.system('db.py 1 {}'.format(file.filename))
    sentences_collection = database.get_collection('sentences')

    filename = file.filename
    df = pd.read_csv('uploads/{}'.format(filename), header=None)
    df = df.iloc[:, 0]
    print(df)

    last_row_id = 0
    print(last_row_id)
    prev = sentences_collection.find()
    prev = list(prev)
    if len(prev) > 0:
        prev = prev[-1]
        print(prev['sid'])
        last_row_id = prev['sid']

    for sent in range(len(df)):
        last_row_id += 1

        print(df[sent])
        sentences_collection.insert_one({
            'sentence': df[sent],
            'sid': last_row_id
        })

    print('Task Finished')

    # os.system('LID_execute.py 1 {}'.format(file.filename))
    from LID_tool.getLanguage import langIdentify
    lid_collection = database.get_collection('lid')

    sentences_collection = database.get_collection('sentences')
    prev_sent = sentences_collection.find()
    prev_sent = list(prev_sent)
    total_num_of_sent = len(prev_sent)

    last_row_id = 0
    print(last_row_id)
    prev = lid_collection.find()
    prev = list(prev)
    if len(prev) > 0:
        prev = prev[-1]
        print(prev['tag_id'])
        last_row_id = prev['tag_id']

    sentence_details = prev_sent[last_row_id]
    sentence = sentence_details['sentence']
    start_index = sentence_details['sid']
    print('SENTENCE = ', sentence)
    print(total_num_of_sent)
    print(prev_sent[start_index-1])

    for i in range(start_index-1, total_num_of_sent):
        sentence = prev_sent[i]['sentence']
        lang = langIdentify(sentence, 'classifiers/HiEn.classifier')
        tags = []

        print(lang)
        for elem in lang:
            inter = [elem[0]]
            for i in range(1, len(elem)):
                if elem[i] is '1':
                    inter.append(elem[i-1][0])
            if len(inter) == 1:
                inter.append('u')
            tags.append(inter)

        print('LANGUAGE TAG = ', tags)
        lid_collection.insert_one({
            'tags': tags,
            'tag_id': last_row_id + 1
        })
        last_row_id = last_row_id + 1

    return redirect('{}/admin'.format(frontend))


@app.route('/sentence-schema-creation', methods=['POST'])
def sentence_schema_creation():
    try:
        database.create_collection('users')
    except:
        print("Already exists")

    try:
        database.create_collection('sentences')
    except:
        print("Already exists")

    try:
        database.create_collection('lid')
    except:
        print("Already exists")

    print('Schemas Created')
    return redirect('{}/admin'.format(frontend))


@app.route('/fetch-users-list', methods=['POST'])
def fetch_users_list():
    user_collection = database.get_collection('users')
    user_list = user_collection.find({})
    user_list = list(user_list)

    users_list = []
    for user in user_list:
        users_list.append(user['username'])
    print(users_list)
    # user_list = list(user_collection)
    # print(user_list)

    return jsonify({'result': users_list})


@app.route('/csv-download', methods=['POST'])
def csv_download():
    from flask import send_file

    username = request.form.get('username')
    # os.system('db_to_csv.py {}'.format(username))
    import csv
    users_collection = database.get_collection('users')

    print('username = ', username)

    user = users_collection.find({'username': username})
    user = list(user)
    print(user)
    sentTag = user[0]['sentTag']

    with open('./csv/data.csv', 'w', encoding='utf-8', newline="") as f:
        writer = csv.writer(f)

        writer.writerow(['grammar', 'date', 'tag', 'link', 'hashtag', 'time'])

        for sentence in sentTag:
            # print(sentence)
            grammar = sentence[0]
            date = sentence[1]
            tag = sentence[2]
            link = sentence[3]
            hashtag = sentence[4] if sentence[4] else []
            time = sentence[5]
            row = [grammar, date, tag, link, hashtag, time]

            writer.writerow(row)
            # break

    return send_file('csv/data.csv', as_attachment=True)

    # print(username)
    # return jsonify({'result': 'Done'})

    # return redirect('{}/admin'.format(frontend))
    return


@app.route('/compare-annotators', methods=['POST'])
def compare_annotators():
    from flask import send_file

    username1 = request.form.get('username1')
    username2 = request.form.get('username2')
    print(username1, username2)

    # return jsonify({'result': 'true'})
    # os.system('compare.py {} {}'.format(username1, username2))
    import csv
    username1_name = username1
    username2_name = username2
    print('username1 = ', username1_name)
    print('username2 = ', username2_name)

    user_collection = database.get_collection('users')
    username1 = user_collection.find({'username': username1_name})
    username2 = user_collection.find({'username': username2_name})

    user1 = list(username1)
    user2 = list(username2)

    print('USER 1 = ', user1)
    print('USER 2 = ', user2)

    counter = min(user1[0]['sentId'], user2[0]['sentId'])
    print(counter)

    sentTag1 = user1[0]['sentTag']
    sentTag2 = user2[0]['sentTag']

    with open('./csv/compare.csv', 'w', encoding='utf-8', newline="") as f:
        writer = csv.writer(f)

        writer.writerow(['grammar_{}'.format(username1_name), 'date_{}'.format(username1_name), 'tag_{}'.format(username1_name), 'link_{}'.format(username1_name), 'hashtag_{}'.format(username1_name), 'time_{}'.format(username1_name), '', 'grammar_{}'.format(username2_name), 'date_{}'.format(username2_name), 'tag_{}'.format(username2_name), 'link_{}'.format(username2_name), 'hashtag_{}'.format(username2_name),
                        'time_{}'.format(username2_name), '', 'grammer_same', 'words_with_similar_annotation', 'total_words', 'Similarity Index'])

        for count in reversed(range(counter)):
            # print(sentence)
            grammar_1 = sentTag1[count][0]
            date_1 = sentTag1[count][1]
            tag_1 = sentTag1[count][2]
            link_1 = sentTag1[count][3]
            hashtag_1 = sentTag1[count][4] if sentTag1[count][4] else []
            time_1 = sentTag1[count][5]

            empty = ''

            grammar_2 = sentTag2[count][0]
            date_2 = sentTag2[count][1]
            tag_2 = sentTag2[count][2]
            link_2 = sentTag2[count][3]
            hashtag_2 = sentTag2[count][4] if sentTag2[count][4] else []
            time_2 = sentTag2[count][5]

            grammer_same = 0
            if grammar_1 == grammar_2:
                grammer_same = 1

            words_with_similar_annotation = 0
            total_words = 0
            for index in range(len(tag_1)):
                if tag_1[index]['value'] == tag_2[index]['value']:
                    words_with_similar_annotation += 1
                total_words += 1

            similar_to_total_ratio = words_with_similar_annotation / total_words

            row = [grammar_1, date_1, tag_1, link_1, hashtag_1, time_1,
                   empty, grammar_2, date_2, tag_2, link_2, hashtag_2, time_2, empty, grammer_same, words_with_similar_annotation, total_words, similar_to_total_ratio]

            writer.writerow(row)
            counter -= 1
            # break

    return send_file('csv/compare.csv', as_attachment=True)


@app.route('/submit-sentence', methods=['POST'])
# @is_logged_in
def submit_sentence():
    user_collection = database.get_collection('users')
    requestdata = json.loads(request.data)
    print(requestdata)
    requestdata = json.loads(requestdata['body'])
    print(requestdata)

    sentId = requestdata['sentId']
    selected = requestdata['selected']
    tag = requestdata['tag']
    username = requestdata['username']
    date = requestdata['date']
    hypertext = requestdata['hypertext']
    hashtags = requestdata['hashtags']
    timeDifference = requestdata['timeDifference']

    lst = [selected, date, tag, hypertext, hashtags, timeDifference]
    print(lst)

    print(sentId, selected, tag, username)

    user_collection.update_one({'username': username}, {
        '$set': {'sentId': sentId},
        '$push': {'sentTag': lst}
    })

    return jsonify({'result': 'Message Stored Successfully'})


# @app.route('/tokenize-en', methods=['POST'])
# # @is_logged_in
# def tokenize_en():
#     sentences_collection = database.get_collection('sentences')
#     requestdata = json.loads(request.data)
#     print(requestdata)
#     requestdata = json.loads(requestdata['body'])

#     sentId = requestdata['id']
#     print(sentId)
#     result = sentences_collection.find({'sid': sentId})
#     data = list(result)
#     data = data[0]
#     sentence = data['sentence']
#     print(sentence)

#     return jsonify({'result': 'Message Stored Successfully'})

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
    hypertext = requestdata['hypertext']

    lst = [selected, date, tag, hypertext]

    print(lst)

    print(sentId, selected, tag, username)

    user = user_collection.find({'username': username})
    user = list(user)
    sentTag = user[0]['sentTag']
    sentTag[sentId - 1] = lst

    user_collection.update_one({'username': username}, {
        '$set': {'sentTag': sentTag}
    })

    # user_collection.update_one({'username': username}, {
    #     '$set': {'sentTag[{sentId}]'.format(sentId=sentId-1): lst},
    # })

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
    app.run(debug=True, host='0.0.0.0', port=5000)
