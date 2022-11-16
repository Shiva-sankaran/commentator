import string
import sys
import pymongo
from flask import Flask, jsonify, redirect, render_template, request, json, session, send_from_directory
from flask_session import Session
import pandas as pd

from passlib.hash import sha256_crypt
from functools import wraps
import json
import requests
from flask_cors import CORS, cross_origin
import os
import subprocess

# "ganeshkharad/gk-hinglish-sentiment"
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import TweetTokenizer
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch import nn
import torch.nn.functional as F
import pandas as pd
import codecs
from hindiwsd import wsd, lesks


app = Flask(__name__)

cors = CORS(app, resources={
            r"/register": {"origins": "*"}}, static_folder='../frontend/build')
app.config.from_pyfile('config.py')
Session(app)

sess = Session()
sess.init_app(app)

frontend = 'http://localhost:3000'
conn_str = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.0"

API_URL = "https://api-inference.huggingface.co/models/sagorsarker/codeswitch-hineng-ner-lince"
headers = {"Authorization": f"Bearer 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"}

client2 = pymongo.MongoClient(
    'mongodb+srv://root:sjjoshi@cluster0.5xthhz8.mongodb.net/test')
db = client2.hinglish

# set a 5-second connection timeout
try:
    client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)
    database = client['annotation_tool']

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
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
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
        sentId = 0
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


@app.route('/logout', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
# @is_logged_in
def logout():
    session.clear()
    return jsonify({'message': "You are logged out"})


@app.route('/get-sentence', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type'])
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


@app.route('/get-lid-data', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
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


@app.route('/get-sentiment-data', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def sentiment_tag():
    # from LID_tool.getLanguage import langIdentify
    print("SENTIMENT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n\n")
    requestdata = json.loads(request.data)
    print(requestdata)
    requestdata = json.loads(requestdata['body'])

    sid = requestdata['sentId']
    print('SENTENCE = ', sid)

    sentiment_collection = database.get_collection('sentiment')
    prev = sentiment_collection.find()
    prev = list(prev)
    # print(prev)
    print(prev[int(sid)-1])
    sentence_tag = prev[int(sid)-1]['sentence_tag']
    word_tags = prev[int(sid)-1]['word_tags']
    print("RETURNNING SENTIMENT DATA FROM BACKEND\n\n")
    print(sentence_tag)
    print(word_tags)
    # print(jsonify({'sentence_tag': sentence_tag,'word_tags':word_tags}))
    return jsonify({'result': [sentence_tag, word_tags]})


def load_hindi_nets(HWN, HWSN):
    Hindi_wordnet = {}
    Hindi_sentinet = {}

    HW_mapping = {'01': 'n', '02': 'a', '03': 'v', '04': 'r'}
    with open(HWN, 'r') as fp:
        line_to_start = 633
        for i, line in enumerate(fp):
            # print(i,line)
            # read line 4 and 7
            if i >= line_to_start:
                temp = line.split(" ")
                # if(i == 54352):
                #     print(temp)
                for j in range(6, len(temp)):
                    # print(temp[j],len(temp[j]))
                    # print(len(temp[j]) =="9")
                    if (len(temp[j]) == 8):
                        ID = temp[j]
                        break
                    elif (len(temp[j]) == 9 and temp[j][-1] == '\n'):
                        ID = temp[j][:-1]
                        break
                # print((temp[0],HW_mapping[temp[1]]) )
                try:
                    Hindi_wordnet[temp[0]].append([HW_mapping[temp[1]], ID])
                except:
                    Hindi_wordnet[temp[0]] = [[HW_mapping[temp[1]], ID]]

    data = pd.read_csv(HWSN, delimiter=' ')
    fields = ['POS_TAG', 'ID', 'POS', 'NEG', 'LIST_OF_WORDS']

    for i in data.index:
        try:
            Hindi_sentinet[data[fields[1]][i]].append(
                [data[fields[0]][i], data[fields[2]][i], data[fields[3]][i]])
        except:
            Hindi_sentinet[data[fields[1]][i]] = [
                [data[fields[0]][i], data[fields[2]][i], data[fields[3]][i]]]

    return Hindi_wordnet, Hindi_sentinet


def helper_hindi_senti(Hwordnet_items, Hsentinet):
    print("word net item", Hwordnet_items)
    # print(IDS)
    for pos, ID in Hwordnet_items:
        ID = int(ID)
        print(ID, pos)
        if (ID in Hsentinet.keys()):
            print("present {} times in hindi sentinet".format(
                len(Hsentinet[ID])))
            print("sentinet item", Hsentinet[ID])
            for entry in Hsentinet[ID]:
                if (entry[0] == pos):
                    if (entry[1] > entry[2]):
                        return 'p'
                    elif (entry[1] < entry[2]):
                        return 'n'
                    else:
                        return 'b'

    return 'i'


def load_custom_senti_file(file_path):
    data = {}
    print("LOADDING\n\n")
    with open(file_path, 'r') as fp:
        for i, line in enumerate(fp):
            temp = line.split(" ")
            print(temp)

            data[temp[0]] = temp[1][0]

    return data


def get_def_eng_senti(word, word_polarity_scores):
    if (word in word_polarity_scores.keys()):
        if (word_polarity_scores[word] < -0.5):
            return 'n'
        elif (word_polarity_scores[word] > 0.5):
            return "p"
        else:
            return "b"
    else:
        return 'i'


def get_def_hinglish_senti(word, Hwordnet, Hsentinet):
    hinglish, hindi_word = wsd.preprocess_transliterate(word)
    if (hindi_word in Hwordnet.keys()):
        return helper_hindi_senti(Hwordnet[hindi_word], Hsentinet)
    else:
        print("word not present in hindi")
        return "i"


def get_eng_senti(word, word_polarity_scores, custom_dict):
    if (custom_dict != {}):
        if (word in custom_dict.keys()):
            return custom_dict[word]
        else:
            return get_def_eng_senti(word, word_polarity_scores)
    else:
        return get_def_eng_senti(word, word_polarity_scores)


def get_hinglish_senti(word, Hwordnet, Hsentinet, custom_dict):
    if (custom_dict != {}):
        if (word in custom_dict.keys()):
            return custom_dict[word]
        else:
            return get_def_hinglish_senti(word, Hwordnet, Hsentinet)
    else:
        return get_def_hinglish_senti(word, Hwordnet, Hsentinet)


def sentiment_engine(request, prev_sent, start_index, last_row_id):
    total_num_of_sent = len(prev_sent)
    print("\n\n\n ----Running sentiment engine-----")

    CUSTOM_MODEL = False
    tk = TweetTokenizer(preserve_case=False)
    sentiment_collection = database.get_collection('sentiment')
    mapping = ['n', 'i', 'p']
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
    model_url = request.form.getlist('text')[0]
    eng_senti_file = request.files['file1']
    heng_senti_file = request.files['file2']
    english_senti_dict = {}
    hinglish_senti_dict = {}
    print("Loading default nltk VADER")
    sia = SentimentIntensityAnalyzer()
    word_polarity_scores = sia.lexicon
    CUSTOM_WORD_ENGLISH_SENT_FILE = False
    print("Loading default hindi word net and hindi word senti net to provide suggestions")
    HWN = "/home/shivasankaran/HindiWN_1_5/database/index_txt"
    HWSN = "/home/shivasankaran/gk-hinglish-sentiment/hindi_dict.txt"
    Hwordnet, Hsentinet = load_hindi_nets(HWN, HWSN)
    CUSTOM_WORD_HINGLISH_SENT_FILE = False

    if (eng_senti_file.filename != ''):
        print("Custom english sentiment file is uploaded")
        eng_senti_file.save(
            'uploads/{}_eng_senti'.format(eng_senti_file.filename))
        english_senti_dict = load_custom_senti_file(
            'uploads/{}_eng_senti'.format(eng_senti_file.filename))
        CUSTOM_WORD_ENGLISH_SENT_FILE = True

    if (heng_senti_file.filename != ''):
        print("Custom hinglish sentiment file is uploaded")
        heng_senti_file.save(
            'uploads/{}_hinglish_senti'.format(heng_senti_file.filename))
        hinglish_senti_dict = load_custom_senti_file(
            'uploads/{}_hinglish_senti'.format(heng_senti_file.filename))
        CUSTOM_WORD_HINGLISH_SENT_FILE = True

    if (model_url == ''):
        model_url = "ganeshkharad/gk-hinglish-sentiment"
    # if(model_url != ''):
    print("Loading CUSTOM MODEL at: ", model_url)
    tokenizer = AutoTokenizer.from_pretrained(model_url)
    model = AutoModelForSequenceClassification.from_pretrained(model_url)
    print("Model loaded")
    CUSTOM_MODEL = True

    for i in range(start_index-1, total_num_of_sent):
        sentence = prev_sent[i]['sentence']

        # if(CUSTOM_MODEL == False):
        #     scores = sia.polarity_scores(sentence)
        #     predicted_label = mapping[np.array(list(scores.values())[:-1]).argmax()]

        # else:
        encoded_input = tokenizer(sentence, return_tensors='pt')
        output = model(**encoded_input)
        scores = F.softmax(output.logits, dim=1).detach().cpu().numpy()[0]
        predicted_label = mapping[scores.argmax()]

        print(predicted_label)

    flag = 1
    for i in range(start_index-1, total_num_of_sent):
        sentence = prev_sent[i]['sentence']
        # indivudal words
        word_emotions = []
        for word in tk.tokenize(sentence):
            emo = get_eng_senti(word, word_polarity_scores, english_senti_dict)
            if (emo == 'i'):
                emo = get_hinglish_senti(
                    word, Hwordnet, Hsentinet, hinglish_senti_dict)
            word_emotions.append([word, emo])
        print("!!!!!!!!!!!!!!!!!!!!!>>>>>>>>>>>>>>.")
        print(word_emotions)

        ###
        sentiment_collection.insert_one({
            'sentence_tag': predicted_label,
            'word_tags': word_emotions,
            'tag_id': last_row_id + 1
        })
        last_row_id = last_row_id + 1
        print("\n\n\n##############\n\n\n{}\n\n\n\###########\n\n\n".format(flag))

    print("----RUN success-----")


@app.route('/admin-file-upload', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
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

    ##
    sentiment_engine(request, prev_sent, start_index, last_row_id)
    ##

    for i in range(start_index-1, total_num_of_sent):
        sentence = prev_sent[i]['sentence']
        lang = langIdentify(sentence, 'classifiers/HiEn.classifier')
        tags = []

        print(lang)
        for elem in lang:
            inter = [elem[0]]
            for i in range(1, len(elem)):
                if elem[i] == '1':
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


@app.route('/sentence-schema-creation', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def sentence_schema_creation():
    try:
        database.create_collection('users')
    except:
        print(" users Already exists")

    try:
        database.create_collection('sentences')
    except:
        print(" sentences Already exists")

    try:
        database.create_collection('lid')
    except:
        print(" lid Already exists")
    try:
        database.create_collection('sentiment')
    except:
        print("sentiment Already exists")

    print('Schemas Created')
    return redirect('{}/admin'.format(frontend))


@app.route('/fetch-users-list', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
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


@app.route('/csv-download', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def csv_download():
    from flask import send_file

    username = request.form.get('username')
    cmi = request.form.get('cmi')
    # os.system('db_to_csv.py {}'.format(username))
    import csv
    users_collection = database.get_collection('users')

    print('username = ', username)
    if (username != 'ALL'):
        user = users_collection.find({'username': username})
        user = list(user)
        print(user)
        sentTag = user[0]['sentTag']

        with open('csv/{}.csv'.format(username), 'w', encoding='utf-8', newline="") as f:
            writer = csv.writer(f)

            writer.writerow(['grammar', 'date', 'tag', 'link',
                            'hashtag', 'time', 'CMI Score'])

            for sentence in sentTag:
                # print(sentence)
                grammar = sentence[0]
                date = sentence[1]
                tag = sentence[2]
                link = sentence[3]
                hashtag = sentence[4] if sentence[4] else []
                time = sentence[5]
                row = [grammar, date, tag, link, hashtag, time]

                en_count = 0
                hi_count = 0
                token_count = 0
                lang_ind_count = 0

                for i in range(len(tag)):
                    if (tag[i]['value'] == 'e'):
                        en_count += 1
                    elif (tag[i]['value'] == 'h'):
                        hi_count += 1
                    elif (tag[i]['value'] == 'u'):
                        lang_ind_count += 1
                    token_count += 1

                max_w = max(en_count, hi_count)

                cmi_score = 0
                if (token_count > lang_ind_count):
                    cmi_score = 100 * \
                        (1 - (max_w / (token_count - lang_ind_count)))
                else:
                    cmi_score = 0

                if (cmi_score >= float(cmi)):
                    row.append(cmi_score)
                    writer.writerow(row)
                # break

        return send_file('csv/{}.csv'.format(username), as_attachment=True)
    else:
        user = users_collection.find()
        user = list(user)
        print(username['username'] for username in user)
        with open('csv/all.csv', 'w', encoding='utf-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['User', 'grammar', 'date', 'tag', 'link',
                                     'hashtag', 'time', 'CMI Score'])

            for single_user in user:
                sentTag = single_user['sentTag']
                for sentence in sentTag:
                    # print(sentence)
                    grammar = sentence[0]
                    date = sentence[1]
                    tag = sentence[2]
                    link = sentence[3]
                    hashtag = sentence[4] if sentence[4] else []
                    time = sentence[5]
                    row = [single_user['username'], grammar, date,
                           tag, link, hashtag, time]

                    en_count = 0
                    hi_count = 0
                    token_count = 0
                    lang_ind_count = 0

                    for i in range(len(tag)):
                        if (tag[i]['value'] == 'e'):
                            en_count += 1
                        elif (tag[i]['value'] == 'h'):
                            hi_count += 1
                        elif (tag[i]['value'] == 'u'):
                            lang_ind_count += 1
                        token_count += 1

                    max_w = max(en_count, hi_count)

                    cmi_score = 0
                    if (token_count > lang_ind_count):
                        cmi_score = 100 * \
                            (1 - (max_w / (token_count - lang_ind_count)))
                    else:
                        cmi_score = 0

                    if (cmi_score >= float(cmi)):
                        row.append(cmi_score)
                        if (single_user['admin'] is False):
                            writer.writerow(row)
                    # break

        return send_file('csv/all.csv', as_attachment=True)

    # print(username)
    # return jsonify({'result': 'Done'})

    # return redirect('{}/admin'.format(frontend))
    return


@app.route('/compare-annotators', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def compare_annotators():
    from flask import send_file

    username1 = request.form.get('username1')
    username2 = request.form.get('username2')
    kappa = request.form.get('kappa')
    print(username1, username2, kappa)

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

    counter = min(int(user1[0]['sentId']), int(user2[0]['sentId']))
    print(counter)

    sentTag1 = user1[0]['sentTag']
    sentTag2 = user2[0]['sentTag']

    with open('csv/compare.csv', 'w', encoding='utf-8', newline="") as f:
        writer = csv.writer(f)

        writer.writerow(['grammar_{}'.format(username1_name), 'date_{}'.format(username1_name), 'tag_{}'.format(username1_name), 'link_{}'.format(username1_name), 'hashtag_{}'.format(username1_name), 'time_{}'.format(username1_name), '', 'grammar_{}'.format(username2_name), 'date_{}'.format(username2_name), 'tag_{}'.format(username2_name), 'link_{}'.format(username2_name), 'hashtag_{}'.format(username2_name),
                        'time_{}'.format(username2_name), '', 'grammer_same', 'words_with_similar_annotation', 'total_words', 'Cohen Kappa Score'])

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

            from sklearn.metrics import cohen_kappa_score
            ann1_tags = [elem['value'] for elem in tag_1]
            ann2_tags = [elem['value'] for elem in tag_2]
            kappa_score = cohen_kappa_score(
                ann1_tags, ann2_tags, labels=None, weights=None)

            row = [grammar_1, date_1, tag_1, link_1, hashtag_1, time_1,
                   empty, grammar_2, date_2, tag_2, link_2, hashtag_2, time_2, empty, grammer_same, words_with_similar_annotation, total_words, kappa_score]

            print(kappa_score, type(kappa_score))
            if (float(str(kappa_score)) >= float(kappa)):
                writer.writerow(row)
            counter -= 1
            # break

    # return 'Good'
    return send_file('csv/compare.csv', as_attachment=True)


@app.route('/submit-sentence', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
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

@app.route('/get-edit-sentence', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
# @is_logged_in
def get_edit_sentence():
    user_collection = database.get_collection('users')
    requestdata = json.loads(request.data)
    print(requestdata)
    requestdata = json.loads(requestdata['body'])

    sentId = requestdata['id']
    username = requestdata['logged_in_user']

    user = user_collection.find({'username': username})
    user = list(user)
    user = user[0]
    userTags = user['sentTag'][sentId-1]

    # user_collection.update_one({'username': username}, {
    #     '$set': {'sentTag[{sentId}]'.format(sentId=sentId-1): lst},
    # })

    return jsonify({'result': userTags})


@app.route('/submit-edit-sentence', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
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
    hashtags = requestdata['hashtags']
    timeDifference = requestdata['timeDifference']

    lst = [selected, date, tag, hypertext, hashtags, timeDifference]

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


@app.route('/all-sentences', methods=['GET', 'POST'])
# @is_logged_in
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
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


@app.route('/getWordFreqeucy', methods=['GET'])
@cross_origin()
def api_getWordFrequency():
    word = request.args.get("word")

    col1 = db.Frequency
    docs = col1.find({'Word': word})
    l = []
    for d in docs:
        del d['_id']
        l.append(d)
    return jsonify(json.loads(json.dumps(l)))


@app.route('/saveFrequency', methods=['POST'])
@cross_origin()
def update_whitelisting():
    if request.method == 'POST':
        data = request.json
        collection = db.Frequency
        col1 = db.Words

        for i in data:
            word = i['Word']
            tag = i['Tag']
            # print(word)
            # print(tag)
            docs = col1.find({'Word': word})
            curr = list(docs)
            if len(curr) == 0:
                dict = {
                    'Word': word,
                    'Tag': {
                        "person": 0,
                        "orgnz": 0,
                        "product": 0,
                        "date": 0,
                        "place": 0,
                        "slang": 0,
                        "none": 0,
                    }
                }
                # print(dict)

                dict1 = {'Word': word}
                x = col1.insert_one(dict1)
                z = collection.insert_one(dict)
            docs = collection.find({'Word': word})
            for d in docs:
                # print(d)
                dict2 = d["Tag"]
                # print(dict2)
                dict2[tag] += 1
                myquery = {'Word': word}
                newvalues = {"$set": {'Tag': dict2}}
                collection.update_one(myquery, newvalues)

        return jsonify({"msg": "successful"})


@app.route('/initialTagging', methods=['GET', 'POST'])
@cross_origin()
def api_initialtagging():
    if request.method == 'POST':
        # text = request.args.get("word")
        # ner_model = pipeline('ner', model=model, tokenizer=tokenizer)
        # x = ner_model(text)
        text = str(request.json["data"])
        payload = {
            "inputs": text
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        # print(response.json())
        return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    client2.close()
